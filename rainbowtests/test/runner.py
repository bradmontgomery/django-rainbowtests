#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from django.test.runner import DiscoverRunner
from rainbowtests.test.core import RainbowTextTestResult, ColorfulOut
from rainbowtests import messages

try:
    import coverage
except ImportError:
    coverage = None


class RainbowDiscoverRunner(DiscoverRunner):
    """Replacement for Django's DiscoverRunner"""

    def __init__(self, *args, **kwargs):
        super(RainbowDiscoverRunner, self).__init__(*args, **kwargs)
        self._cov = None
        if coverage:
            self._cov = coverage.coverage()
            self._cov.start()

    def run_suite(self, suite, **kwargs):
        if not hasattr(self, "test_runner"):
            # This was added as a clas attribute in Django 1.7
            self.test_runner = unittest.TextTestRunner

        runner = self.test_runner(
            verbosity=self.verbosity,
            failfast=self.failfast,
        )
        runner.resultclass = RainbowTextTestResult
        result = runner.run(suite)

        if result.wasSuccessful():
            runner.stream.writeln(messages.random_happy())
        else:
            runner.stream.writeln(messages.random_sad())
        return result

    def suite_result(self, suite, result, **kwargs):
        result = super(RainbowDiscoverRunner, self).suite_result(
            suite, result, **kwargs
        )
        if coverage and self._cov:
            self._cov.stop()
            self._cov.report(file=ColorfulOut())
        return result
