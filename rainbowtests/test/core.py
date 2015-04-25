#!/usr/bin/env python
# -*- coding: utf-8 -*-

import django
import sys
import unittest

from inspect import getfile
from os.path import dirname

from rainbowtests import colors


class ColorfulOut:
    """Wrapper around sys.sdout to make it's output colorful"""

    def write(self, arg, **kwargs):
        return sys.stdout.write(colors.blue(arg), **kwargs)


class RainbowTextTestResult(unittest.runner.TextTestResult):
    """The color-enhanced Text output for a test run."""

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
        """Print colorful test output:

        * Error and Failure headers are in Red.
        * The First/Last lines (Traceback heading and Exception) are Cyan.
        # Non-Django lines are Yellow.

        """

        # Find the path where django is installed.
        django_path = dirname(getfile(django))

        for test, err in errors:
            self.stream.writeln(colors.red(self.separator1))
            out = "{0}: {1}".format(flavour, self.getDescription(test))
            self.stream.writeln(colors.red(out))
            self.stream.writeln(colors.red(self.separator2))
            tb = "{0}".format(err)
            lines = tb.strip().split("\n")

            # Temporarily remove the first & last lines of the Traceback.
            if len(lines) > 2:
                first_line = colors.cyan(lines.pop(0))  # Traceback header
                last_line = colors.cyan(lines.pop(-1))  # The Exception
            else:
                first_line, last_line = ('', '')

            # The traceback is organized into pairs; a path and a line of code,
            # and the pair looks something like this:
            #
            # >>> File "/path/to/module.py", line 123, in method_name
            # >>>     some_line_of_code
            #
            # So, we'll group every two lines of the traceback, and highlight
            # the pertinent parts

            i = 0  # remember which line of the Traceback we're highlighting.
            groups = zip(*[lines[x::2] for x in range(2)])
            for path, line_of_code in groups:
                if django_path not in path:
                    lines[i] = colors.yellow(path)
                    lines[i + 1] = colors.yellow(line_of_code)
                i += 2

            lines.insert(0, first_line)
            lines.append(last_line)
            self.stream.writeln("\n".join(lines))
