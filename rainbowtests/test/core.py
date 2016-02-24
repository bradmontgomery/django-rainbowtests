#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import unittest
from inspect import getfile
from os.path import dirname

import django
from django.conf import settings

from rainbowtests import colors


class ColorfulOut:
    """Wrapper around sys.sdout to make it's output colorful"""

    def write(self, arg, **kwargs):
        return sys.stdout.write(colors.blue(arg), **kwargs)


class RainbowTextTestResult(unittest.runner.TextTestResult):
    """The color-enhanced Text output for a test run."""

    def __init__(self, *args, **kwargs):
        super(RainbowTextTestResult, self).__init__(*args, **kwargs)
        self._set_highlight_path()

    def _set_highlight_path(self):
        """Determine what path to code we should highlight in a Traceback."""
        try:
            self.highlight_path = settings.RAINBOWTESTS_HIGHLIGHT_PATH
        except AttributeError:
            # Highlight packages installed alongside django
            self.highlight_path = dirname(getfile(django))

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

            # Python 2 tracebacks are organized into pairs of lines--a path and
            # a line of code that looks something like this:
            #
            # >>> File "/path/to/module.py", line 123, in method_name
            # >>>     some_line_of_code
            #
            # Python 3 tracebacks, however, may start with several lines of
            # output, e.g.:
            #
            # -----------------------------------------------------------------
            # Traceback (most recent call last):
            # File "/usr/lib/python/unittest/mock.py", line 1, in _whatever
            #   return getattr(thing, comp)
            # AttributeError: 'module' object has no attribute 'something'
            #
            # During handling of the above exception, another exception occurred
            #
            # -----------------------------------------------------------------
            #
            # So, rather than trying to group every two lines (like this code
            # used to do), just inspect each line and if we watch a given
            # path, highlight it and the next line of the traceback.

            i = 0
            while i < len(lines) - 1:
                if self.highlight_path in lines[i]:
                    lines[i] = colors.yellow(lines[i])
                    lines[i + 1] = colors.yellow(lines[i + 1])
                i += 1

            lines.insert(0, first_line)
            lines.append(last_line)
            self.stream.writeln("\n".join(lines))
