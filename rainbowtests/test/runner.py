#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from django.conf import settings
from django.test.runner import DiscoverRunner

from rainbowtests import messages
from rainbowtests.test.core import ColorfulOut, RainbowTextTestResult

try:
    import coverage
except ImportError:
    coverage = None


class RainbowDiscoverRunner(DiscoverRunner):
    """Replacement for Django's DiscoverRunner"""

    def __init__(self, *args, **kwargs):
        super(RainbowDiscoverRunner, self).__init__(*args, **kwargs)
        self._set_messages_display()

    def _set_messages_display(self):
        """Don't show messages if the user doesn't want them"""
        try:
            self.show_messages = settings.RAINBOWTESTS_SHOW_MESSAGES
        except AttributeError:
            self.show_messages = True

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

        if self.show_messages:
            runner.stream.writeln(messages.random(result.wasSuccessful()))
        return result


class RainbowDiscoverCoverageRunner(RainbowDiscoverRunner):
    """Replacement for Django's DiscoverRunner with coverage support"""

    def __init__(self, *args, **kwargs):
        super(RainbowDiscoverCoverageRunner, self).__init__(*args, **kwargs)
        self._cov = None
        if coverage:
            self._cov = coverage.coverage()
            self._cov.start()

    def suite_result(self, suite, result, **kwargs):
        result = super(RainbowDiscoverCoverageRunner, self).suite_result(
            suite, result, **kwargs
        )
        if coverage and self._cov:
            self._cov.stop()
            self._cov.report(file=ColorfulOut())
        return result
