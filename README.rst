An experimental nose plugin to block access to external services that you
really should not be accessing in your unit tests.

To use::

  pip install nose-blockage

Then add the following to your tests::

  --with-blockage

By default it whitelists `localhost` and `127.0.0.1`. To change the whitelist::

  --http-whitelist=some.site,some.other.site

If the code hits a http connection then instead of completing it will raise a
MockHTTPCall exception. Please go and mock your tests appropriately.

To come, maybe more libs.

