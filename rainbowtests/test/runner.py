#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from django.test.runner import DiscoverRunner
from rainbowtests.test.core import RainbowTextTestResult
from rainbowtests import messages


class RainbowDiscoverRunner(DiscoverRunner):
    """Replacement for Django's DiscoverRunner"""

    def run_suite(self, suite, **kwargs):
        # NOTE: This code is similar to that in the RainbowTestSuiteRunner,
        # which is a lot like the code in 1.6, but this has changed
        # significantly for 1.7
        runner = unittest.TextTestRunner(
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
