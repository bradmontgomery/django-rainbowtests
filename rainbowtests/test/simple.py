#!/usr/bin/env python
# -*- coding: utf-8 -*-

# NOTE: DjangoTestSuiteRunner was removed in Django 1.8
# We should remove it at some point?

import unittest

from django.test.simple import DjangoTestSuiteRunner

from rainbowtests import messages
from rainbowtests.test.core import RainbowTextTestResult


class RainbowTestSuiteRunner(DjangoTestSuiteRunner):
    """Replacement Test Suite Runner for Django."""
    def run_suite(self, suite, **kwargs):

        runner = unittest.TextTestRunner(
            verbosity=self.verbosity, failfast=self.failfast)
        runner.resultclass = RainbowTextTestResult
        result = runner.run(suite)

        if result.wasSuccessful():
            runner.stream.writeln(messages.random_happy())
        else:
            runner.stream.writeln(messages.random_sad())
        return result
