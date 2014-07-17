#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from django.test.simple import DjangoTestSuiteRunner
from rainbowtests import colors
from rainbowtests.test.core import RainbowTextTestResult


class RainbowTestSuiteRunner(DjangoTestSuiteRunner):
    """Replacement Test Suite Runner for Django."""
    def run_suite(self, suite, **kwargs):

        runner = unittest.TextTestRunner(
            verbosity=self.verbosity, failfast=self.failfast)
        runner.resultclass = RainbowTextTestResult
        result = runner.run(suite)

        line = "---------------------------"
        if result.wasSuccessful():
            output = "\n\n{0}\nSucces! *high-five*\n{1}\n\n".format(line, line)
            runner.stream.writeln(colors.green(output))
        else:
            output = "\n\n{0}\nsigh :-(\n{1}\n\n".format(line, line)
            runner.stream.writeln(colors.red(output))
        return result
