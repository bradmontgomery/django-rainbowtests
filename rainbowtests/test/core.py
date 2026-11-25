"""Core test result and output classes for rainbowtests."""

import io
import sys
from collections.abc import Iterable
from inspect import getfile
from os.path import dirname
from types import TracebackType
from unittest import TestCase, TestResult, TextTestResult

import django
from django.conf import settings

from rainbowtests import colors

# Mirrors typeshed's ``OptExcInfo`` used by ``unittest.TestResult``.
ExcInfo = tuple[type[BaseException], BaseException, TracebackType] | tuple[None, None, None]


def colorize_traceback(traceback: str, highlight_path: str) -> str:
    """Colorize a formatted traceback.

    * The first line (traceback header) and last line (the exception) are cyan.
    * Any line containing ``highlight_path`` -- plus the line after it, which is
      usually the source code for that frame -- is yellow.
    """
    lines = traceback.strip().split("\n")
    if len(lines) > 2:
        first_line = colors.cyan(lines.pop(0))
        last_line = colors.cyan(lines.pop(-1))
    else:
        first_line, last_line = "", ""

    for i in range(len(lines) - 1):
        if highlight_path in lines[i]:
            lines[i] = colors.yellow(lines[i])
            lines[i + 1] = colors.yellow(lines[i + 1])

    return "\n".join([first_line, *lines, last_line])


class ColorfulOut(io.StringIO):
    """Write-only text stream that prints to ``sys.stdout`` in blue."""

    def write(self, s: str, /) -> int:
        return sys.stdout.write(colors.blue(s))


class RainbowTextTestResult(TextTestResult):
    """The color-enhanced Text output for a test run."""

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # Default: highlight frames from packages installed alongside Django.
        default_path = dirname(getfile(django))
        self.highlight_path: str = getattr(settings, "RAINBOWTESTS_HIGHLIGHT_PATH", default_path)

    def _report(self, long: str, short: str) -> None:
        """Write a status: the long word when verbose, else a single character."""
        if self.showAll:
            self.stream.writeln(long)
        elif self.dots:
            self.stream.write(short)
            self.stream.flush()

    def addSuccess(self, test: TestCase) -> None:
        TestResult.addSuccess(self, test)
        self._report(colors.green("ok"), colors.green("."))

    def addError(self, test: TestCase, err: ExcInfo) -> None:
        TestResult.addError(self, test, err)
        self._report(colors.red("ERROR"), colors.red("E"))

    def addFailure(self, test: TestCase, err: ExcInfo) -> None:
        TestResult.addFailure(self, test, err)
        self._report(colors.red("FAIL"), colors.red("F"))

    def printErrorList(self, flavour: str, errors: Iterable[tuple[TestCase, str]]) -> None:
        """Print each error/failure with red headers and a colorized traceback."""
        for test, err in errors:
            self.stream.writeln(colors.red(self.separator1))
            self.stream.writeln(colors.red(f"{flavour}: {self.getDescription(test)}"))
            self.stream.writeln(colors.red(self.separator2))
            self.stream.writeln(colorize_traceback(str(err), self.highlight_path))
