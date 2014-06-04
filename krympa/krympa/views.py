from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound, HTTPFound

from urllib.parse import urlparse
from string import ascii_letters, digits
import random

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

@view_defaults(renderer='jsonp')
class API(object):
    def __init__(self, request):
        self.request = request
        self.status = 'error'
        self.errmsg = ''
        self.response = {}

    def finish(self):
        if self.status is 'error':
            self.response['errmsg'] = self.errmsg
        return {'status': self.status, 'response': self.response}

    @view_config(route_name='api', request_method='POST')
    def set(self):
        try:
            url = urlparse(self.request.params['url'])
        except KeyError:
            self.errmsg = 'Required paraneter "url" not set.'
        else:
            if url.scheme in ['http', 'https']:
                shortened = RedisBacked.get_code(url.geturl(), self.request)
                if not shortened:
                    shortened = ''.join(random.choice(ascii_letters + digits) for x in range(5))
                    RedisBacked.set(shortened, url.geturl(), self.request)
                self.status = 'success'
                self.response['short'] = self.request.route_url('redirect', shortened=shortened)
                self.response['url'] = url.geturl()
            else:
                self.errmsg = 'Not an allowed scheme'

        return self.finish()

    @view_config(route_name='api', request_method='GET')
    def get(self):
        try:
            shortened = self.request.params['shortened']
        except KeyError:
            self.errmsg = 'Required parameter "shortened" not set.'
        else:
            url = RedisBacked.get_url(shortened)
            if not url:
                self.errmsg = 'Not in use.'
            else:
                self.status = 'success'
                self.response['url'] = url.decode('utf-8')

        return self.finish()
