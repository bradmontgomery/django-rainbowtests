#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from django.test.runner import DiscoverRunner
from rainbowtests.test.core import RainbowTextTestResult
from rainbowtests import messages


class RainbowDiscoverRunner(DiscoverRunner):
    """Replacement for Django's DiscoverRunner"""

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
