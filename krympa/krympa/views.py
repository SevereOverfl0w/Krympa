from pyramid.view import view_config, view_defaults
from pyramid.httpexceptions import HTTPNotFound, HTTPFound

from urllib.parse import urlparse
from string import ascii_letters, digits
import random

@view_config(route_name='home', renderer='templates/index.mako')
def home(request):
    return {'project': 'Krympa'}

@view_config(route_name='redirect')
def redirect(request):
    shortened = request.matchdict['shortened']
    url = request.redis.get('short-url:%s' % shortened)
    if url:
        return HTTPFound(location=url.decode('utf-8'))
    else:
        return HTTPNotFound()

class RedisBacked(object)
    def set(self, code, url):
        self.request.redis.set('short-url:%s' % shortened, url.geturl())
        self.request.redis.set('reverse-url:%s' % url.geturl(), shortened)
    def get_url(self, code):
        return request.redis.get('short-url:%s' % shortened)
    def get_code(self, url):
        return self.request.redis.get('reverse-url:%s' % url.geturl())

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
                shortened = self.request.redis.get('reverse-url:%s' % url.geturl())
                if not shortened:
                    shortened = ''.join(random.choice(ascii_letters + digits) for x in range(5))
                    self.request.redis.set('short-url:%s' % shortened, url.geturl())
                    self.request.redis.set('reverse-url:%s' % url.geturl(), shortened)
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
            url = self.request.redis.get('short-url:%s' % shortened)
            if not url:
                self.errmsg = 'Not in use.'
            else:
                self.status = 'success'
                self.response['url'] = url.decode('utf-8')

        return self.finish()
