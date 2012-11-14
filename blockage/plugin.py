import httplib
import logging
import os
import urlparse

NOSE = False
try:
    from nose.plugins.base import Plugin
    NOSE = True
except ImportError:
    class Plugin:
        pass

log = logging.getLogger(__name__)


class MockHTTPCall(Exception):
    # If you don't mock out http calls in your tests, we'll raise an error
    # for you so you'll remember to do it next time.
    pass



class NoseBlockage(Plugin):
    name = 'blockage'

    def options(self, parse, env=os.environ):
        import pdb; pdb.set_trace()
        print parse
        super(NoseBlockage, self).options(parse, env=env)

    def configure(self, options, conf):
        import pdb; pdb.set_trace()
        print options, conf
        super(NoseBlockage, self).configure(options, conf)

    def begin(self):

        # These are the ES hosts.
        HTTP_DOMAINS = ['http://127.0.0.1:9200']
        HTTP_DOMAINS = [urlparse.urlparse(d).netloc for d in HTTP_DOMAINS]

        old = httplib.HTTPConnection
        def whitelisted(self, host, *args, **kwargs):
            if host not in HTTP_DOMAINS:
                print '-', host
                raise MockHTTPCall(host)
            print '+', host
            return old(self, host, *args, **kwargs)

        whitelisted.patched = True

        if not getattr(httplib.HTTPConnection.__init__, 'patched', None):
            httplib.HTTPConnection.__init__ = whitelisted

