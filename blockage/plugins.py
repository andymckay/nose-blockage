import httplib
import logging
import os
import smtplib

from nose.plugins.base import Plugin

log = logging.getLogger(__name__)


class MockHTTPCall(Exception):
    # If you don't mock out http calls in your tests, we'll raise an error
    # for you so you'll remember to do it next time.
    pass

class MockSMTPCall(Exception):
    # If you don't mock out smtp calls in your tests, we'll raise an error
    # for you so you'll remember to do it next time.
    pass


class NoseBlockage(Plugin):
    name = 'blockage'
    default_http_whitelist = '127.0.0.1,localhost'
    default_smtp_whitelist = ''

    def options(self, parser, env=os.environ):
        super(NoseBlockage, self).options(parser, env=env)
        parser.add_option('--http-whitelist', action='store',
                          default=env.get('HTTP_WHITELIST',
                                          self.default_http_whitelist),
                          dest='http_whitelist')
        parser.add_option('--smtp-whitelist', action='store',
                          default=env.get('SMTP_WHITELIST',
                                          self.default_smtp_whitelist),
                          dest='smtp_whitelist')

    def configure(self, options, conf):
        self.options = options
        super(NoseBlockage, self).configure(options, conf)
        self.whitelists = {}
        for name, option in (['http', 'http_whitelist'],
                             ['smtp', 'smtp_whitelist']):
            self.whitelists[name] = [s.strip() for s in
                                     getattr(self.options, option).split(',')]

    def begin(self):
        self.do_http()
        self.do_smtp()

    def do_http(self):
        http_whitelist = self.whitelists['http']

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

    def do_smtp(self):
        smtp_whitelist = self.whitelists['smtp']

        def whitelisted(self, host, *args, **kwargs):
            if isinstance(host, basestring) and host not in smtp_whitelist:
                log.warning('Denied SMTP connection to: %s' % host)
                raise MockSMTPCall(host)
            log.debug('Allowed SMTP connection to: %s' % host)
            return self.old(host, *args, **kwargs)

        whitelisted.blockage = True

        if not getattr(smtplib.SMTP, 'blockage', False):
            log.debug('Monkey patching smtplib')
            smtplib.SMTP.old = smtplib.SMTP.__init__
            smtplib.SMTP.__init__ = whitelisted
