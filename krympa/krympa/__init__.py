from pyramid.config import Configurator
from pyramid.renderers import JSONP


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.add_renderer('jsonp', JSONP(param_name='callback'))
    config.include('pyramid_mako')
    config.include('pyramid_redis')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('api_set', '/set')
    config.add_route('api_get', '/get')
    config.add_route('redirect', '/{shortened}')
    config.scan()
    return config.make_wsgi_app()
