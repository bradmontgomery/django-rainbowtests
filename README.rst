django-rainbowtests
===================

This is a custom test runner for Django that gives you *really* colorful test
output.

How do I use this?
------------------

Disclaimer: This isn't on pypi for a reason (it's probably not ready for
prime-time).

Install this app (put ``rainbowtests`` somewhere on your python path or 
pip-install it with::

    pip install -e git+git://github.com/bradmontgomery/django-rainbowtests.git#egg=django-rainbowtests

Then, add the following setting::
 
    TEST_RUNNER = 'rainbowtests.RainbowTestSuiteRunner'

Then run your tests!


License
-------

This code is distributed under the terms of the MIT license. See the
``LICENSE`` file.
