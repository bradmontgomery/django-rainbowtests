#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from django.test.runner import DiscoverRunner
from rainbowtests import colors
from rainbowtests.test.core import RainbowTextTestResult


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

        line = "---------------------------"
        if result.wasSuccessful():
            output = "\n\n{0}\nSucces! *high-five*\n{1}\n\n".format(line, line)
            runner.stream.writeln(colors.green(output))
        else:
            output = "\n\n{0}\nsigh :-(\n{1}\n\n".format(line, line)
            runner.stream.writeln(colors.red(output))
        return result
