django-rainbowtests
===================

This is a custom test runner for Django that gives you *really* colorful test
output.

How do I use this?
------------------

First install with::

    pip install django-rainbowtests

Or grab the development version from github::

    pip install -e git+git://github.com/bradmontgomery/django-rainbowtests.git#egg=django-rainbowtests

Then, add one of the following settings. For the behavior of Django 1.6's
``DiscoverRunner``, use the following::

    TEST_RUNNER = 'rainbowtests.test.runner.RainbowDiscoverRunner'

If you want the *old-style* behavior, use::

    TEST_RUNNER = 'rainbowtests.test.simple.RainbowTestSuiteRunner'

Then run your tests!


Python Compatibility
--------------------

This code *should* work with Python 2.7 and Python 3.4. If you find otherwise,
please submit a bug report.

License
-------

This code is distributed under the terms of the MIT license. See the
``LICENSE`` file.
