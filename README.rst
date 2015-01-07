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

Then, add one of the following settings. For the ``DiscoverRunner`` behavior
that was introduced with Django 1.6, use the following::

    TEST_RUNNER = 'rainbowtests.test.runner.RainbowDiscoverRunner'

If you want the *old-style* behavior (Django 1.5 or older), use::

    TEST_RUNNER = 'rainbowtests.test.simple.RainbowTestSuiteRunner'

Then run your tests!


Python/Django Compatibility
--------------------

This code *should* work with Django 1.7, Python 2.7, and Python 3.4. If you
find otherwise, please open an Issue.

License
-------

This code is distributed under the terms of the MIT license. See the
``LICENSE`` file.
