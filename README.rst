django-rainbowtests
===================

|version| |license|

This is a custom test runner for Django that gives you *really* colorful test
output.

How do I use this?
------------------

Install the latest release with::

    pip install django-rainbowtests

*New in 0.5.0*: Add a settings for ``RAINBOWTESTS_HIGHLIGHT_PATH``. While
running your tests, any lines in your tracebacks that match this path will be
highlighted, making them easier to find and read. If you omit this setting,
the default is to use the path to your django installation (which probably
ends up highlighting more than you need or want).::

    RAINBOWTESTS_HIGHLIGHT_PATH = '/path/to/my/project/'

*New in 0.6.0* If the test output is too verbose and you just want a colorful
version of the standard Django test output, set ``RAINBOWTESTS_SHOW_MESSAGES``
to ``False``::

    RAINBOWTESTS_SHOW_MESSAGES = False

Django > 1.6: Set your test runner to the ``RainbowDiscoverRunner``::

    TEST_RUNNER = 'rainbowtests.test.runner.RainbowDiscoverRunner'

Django < 1.5: Set your test runner to the ``RainbowTestSuiteRunner``. This was
removed in django 1.8, so using this test runner on newer projects will fail::

    TEST_RUNNER = 'rainbowtests.test.simple.RainbowTestSuiteRunner'

Then run your tests!


Python/Django Compatibility
---------------------------

This code *should* work with Django 1.4 - 1.8, Python 2.7 and Python 3.4. If you
find otherwise, please open an Issue.


Coverage
--------

As of version 0.3.0, there is (experimental) support for `coverage <http://nedbatchelder.com/code/coverage/>`_,
and 0.4.0 cleaned it up by introducing a new test runner:

Use

    TEST_RUNNER = 'rainbowtests.test.runner.RainbowDiscoverCoverageRunner'

and run your tests as normal (``python manage.py test <whatever>``), and if you
have coverage installed, you should see a report when your tests complete.
You could also use ``coverage html`` and open ``htmlcov/index.html`` for a more fancy coverage report.
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
