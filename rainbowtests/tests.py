#!/usr/bin/env python
# -*- coding: utf-8 -*-

import colors
import django
import unittest

from inspect import getfile
from os.path import dirname


class RainbowTextTestResult(unittest.runner.TextTestResult):

    def addSuccess(self, test):
        unittest.TestResult.addSuccess(self, test)
        if self.showAll:
            self.stream.writeln(colors.green("ok"))
        elif self.dots:
            self.stream.write(colors.green("."))
            self.stream.flush()

    def addError(self, test, err):
        unittest.TestResult.addError(self, test, err)
        if self.showAll:
            self.stream.writeln(colors.red("ERROR"))
        elif self.dots:
            self.stream.write(colors.red('E'))
            self.stream.flush()

    def addFailure(self, test, err):
        unittest.TestResult.addFailure(self, test, err)
        if self.showAll:
            self.stream.writeln(colors.red("FAIL"))
        elif self.dots:
            self.stream.write(colors.red('F'))
            self.stream.flush()

    def printErrorList(self, flavour, errors):
        """Print Error and Failure headers in Red"""

        # To find the path where django is installed. We highlight our own
        # files, but not Django's
        django_path = dirname(getfile(django))

        for test, err in errors:
            self.stream.writeln(colors.red(self.separator1))
            out = "{0}: {1}".format(flavour, self.getDescription(test))
            self.stream.writeln(colors.red(out))
            self.stream.writeln(colors.red(self.separator2))
            tb = "{0}".format(err)
            lines = tb.split("\n")
            i = 0
            for line in lines:
                if django_path not in lines:
                    lines[i] = colors.yellow(line)
                i += 1
            self.stream.writeln("\n".join(lines))


class RainbowTestSuiteRunner(django.test.simple.DjangoTestSuiteRunner):
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
