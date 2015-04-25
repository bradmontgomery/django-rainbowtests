django-rainbowtests
===================

|version| |license|

This is a custom test runner for Django that gives you *really* colorful test
output.

How do I use this?
------------------

Install the latest release with::

    pip install django-rainbowtests

Then, add one of the following settings. For the ``DiscoverRunner`` behavior
that was introduced with Django 1.6, use the following::

    TEST_RUNNER = 'rainbowtests.test.runner.RainbowDiscoverRunner'

If you want the *old-style* behavior (Django 1.5 or older), use::

    TEST_RUNNER = 'rainbowtests.test.simple.RainbowTestSuiteRunner'

Then run your tests!


Python/Django Compatibility
---------------------------

This code *should* work with Django 1.4 - 1.8, Python 2.7 and Python 3.4. If you
find otherwise, please open an Issue.


Coverage
--------

As of version 0.3.0, there is (experimental) support for `coverage <http://nedbatchelder.com/code/coverage/>`_.

Run your tests as normal (``python manage.py test <whatever>``), and if you
have coverage installed, you should see a report when your tests complete.
Make sure you have a ``.coveragerc`` file, though!


License
-------

This code is distributed under the terms of the MIT license. See the
``LICENSE`` file.


.. |version| image:: http://img.shields.io/pypi/v/django-rainbowtests.svg?style=flat-square
    :alt: Current Release
    :target: https://pypi.python.org/pypi/django-rainbowtests/

.. |license| image:: http://img.shields.io/pypi/l/django-rainbowtests.svg?style=flat-square
    :alt: License
    :target: https://pypi.python.org/pypi/django-rainbowtests/
