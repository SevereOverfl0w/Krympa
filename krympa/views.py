from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound, HTTPFound

from urllib.parse import urlparse
from string import ascii_letters, digits
import random
import colander

@view_config(route_name='home', renderer='templates/index.mako')
def home(request):
    return {'project': 'Krympa'}

class RedisBacked(object):
    short_url = 'short-url:%s'
    reverse_url = 'reverse-url:%s'
    @classmethod
    def set(self, code, url, request):
        request.redis.set(self.short_url % code, url)
        request.redis.set(self.reverse_url % url, code)
    @classmethod
    def get_url(self, code, request):
        return request.redis.get(self.short_url % code)
    @classmethod
    def get_code(self, url, request):
        return request.redis.get(self.reverse_url % url)

@view_config(route_name='redirect')
def redirect(request):
    shortened = request.matchdict['shortened']
    url = RedisBacked.get_url(shortened, request)
    if url:
        return HTTPFound(location=url.decode('utf-8'))
    else:
        return HTTPNotFound()

class URLParam(colander.MappingSchema):
    url = colander.SchemaNode(colander.String(),
                              validator=colander.url)

class CodeParam(colander.MappingSchema):
    shortened = colander.SchemaNode(colander.String())

    def validator(self, node, data):
        request = node.bindings.get('request')
        url = RedisBacked.get_url(data["shortened"], request)
        if url is None:
            raise colander.Invalid(node["shortened"], 'Code is not associated with an URL')
        data['shortened_url'] = url


@view_defaults(renderer='jsonp')
class API(object):
    def __init__(self, request):
        self.request = request
        self.status = 'error'
        self.errmsg = ''
        self.response = {}

    def error_msg(self, msg):
        self.errmsg = msg
        self.status = 'error'
        return self.finish()

    def finish(self):
        if self.status is 'error':
            self.response['errmsg'] = self.errmsg
        return {'status': self.status, 'response': self.response}

    @view_config(route_name='api', request_method='POST')
    def set(self):
        schema = URLParam().bind(request=self.request)
        try:
            valid = schema.deserialize(self.request.params)
        except colander.Invalid as e:
            return self.error_msg(e.asdict())

        url = valid['url']
        shortened = RedisBacked.get_code(url, self.request)
        if not shortened:
            shortened = ''.join(random.choice(ascii_letters + digits) for x in range(5))
            RedisBacked.set(shortened, url, self.request)
        self.status = 'success'
        self.response['short'] = self.request.route_url('redirect', shortened=shortened)
        self.response['url'] = url

        return self.finish()

    @view_config(route_name='api', request_method='GET')
    def get(self):
        schema = CodeParam().bind(request=self.request)
        try:
            valid = schema.deserialize(self.request.params)
        except colander.Invalid as e:
            return self.error_msg(e.asdict())

        self.status = 'success'
        self.response['url'] = valid['shortened_url'].decode('utf-8')
        return self.finish()
