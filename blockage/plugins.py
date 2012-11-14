import httplib
import logging
import os

from nose.plugins.base import Plugin

log = logging.getLogger(__name__)


class MockHTTPCall(Exception):
    # If you don't mock out http calls in your tests, we'll raise an error
    # for you so you'll remember to do it next time.
    pass


class NoseBlockage(Plugin):
    name = 'blockage'
    default_http_whitelist = '127.0.0.1,localhost'

    def options(self, parser, env=os.environ):
        super(NoseBlockage, self).options(parser, env=env)
        parser.add_option('--http-whitelist', action='store',
                          default=env.get('HTTP_WHITELIST',
                                          self.default_http_whitelist),
                          dest='http_whitelist')

    def configure(self, options, conf):
        self.options = options
        super(NoseBlockage, self).configure(options, conf)
        self.http_whitelist = [s.strip() for s in
                               self.options.http_whitelist.split(',')]

    def begin(self):
        http_whitelist = self.http_whitelist

        def whitelisted(self, host, *args, **kwargs):
            if isinstance(host, basestring) and host not in http_whitelist:
                log.warning('Denied HTTP connection to: %s' % host)
                raise MockHTTPCall(host)
            log.debug('Allowed HTTP connection to: %s' % host)
            return self.old(host, *args, **kwargs)

        whitelisted.blockage = True

        if not getattr(httplib.HTTPConnection, 'blockage', False):
            log.debug('Monkey patching httplib')
            httplib.HTTPConnection.old = httplib.HTTPConnection.__init__
            httplib.HTTPConnection.__init__ = whitelisted
