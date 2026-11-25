"""Tests for rainbowtests.test.core."""

import sys
import unittest
from inspect import getfile
from os.path import dirname

import django
import pytest
from django.test import override_settings

from rainbowtests import colors
from rainbowtests.test.core import ColorfulOut, colorize_traceback
from tests.conftest import Sample


class TestColorizeTraceback:
    def test_highlights_matching_frame_and_next_line(self) -> None:
        tb = "\n".join(
            [
                "Traceback (most recent call last):",
                '  File "/app/mine.py", line 1, in f',
                "    do_thing()",
                '  File "/lib/other.py", line 2, in g',
                "    other()",
                "ValueError: bad",
            ]
        )
        lines = colorize_traceback(tb, "/app/").split("\n")
        assert lines[0] == colors.cyan("Traceback (most recent call last):")
        assert lines[1] == colors.yellow('  File "/app/mine.py", line 1, in f')
        assert lines[2] == colors.yellow("    do_thing()")
        assert lines[3] == '  File "/lib/other.py", line 2, in g'
        assert lines[4] == "    other()"
        assert lines[5] == colors.cyan("ValueError: bad")

    def test_match_on_last_frame_line_is_not_highlighted(self) -> None:
        # The loop pairs a path line with the line after it, so a match on the
        # final body line (with nothing after it) is left alone.
        tb = "Traceback:\nplain\n/app/ at end\nError"
        lines = colorize_traceback(tb, "/app/").split("\n")
        assert lines[1:3] == ["plain", "/app/ at end"]

    def test_short_traceback_has_no_header_or_footer(self) -> None:
        assert colorize_traceback("only line\n", "/app/") == "\nonly line\n"


def test_colorful_out_writes_blue_to_stdout(capsys) -> None:
    written = ColorfulOut().write("report")
    out = capsys.readouterr().out
    assert out == colors.blue("report")
    assert written == len(out)


class TestHighlightPath:
    def test_defaults_to_django_install_dir(self, make_result) -> None:
        result, _ = make_result()
        assert result.highlight_path == dirname(getfile(django))

    @override_settings(RAINBOWTESTS_HIGHLIGHT_PATH="/my/project/")
    def test_uses_setting(self, make_result) -> None:
        result, _ = make_result()
        assert result.highlight_path == "/my/project/"


def _exc_info(exc: BaseException):
    try:
        raise exc
    except BaseException:
        return sys.exc_info()


OUTCOMES = {
    "success": (lambda r, t: r.addSuccess(t), colors.green("ok"), colors.green(".")),
    "error": (
        lambda r, t: r.addError(t, _exc_info(ValueError())),
        colors.red("ERROR"),
        colors.red("E"),
    ),
    "failure": (
        lambda r, t: r.addFailure(t, _exc_info(AssertionError())),
        colors.red("FAIL"),
        colors.red("F"),
    ),
}


@pytest.mark.parametrize("outcome", OUTCOMES)
@pytest.mark.parametrize("verbosity", [0, 1, 2])
def test_status_output(make_result, outcome: str, verbosity: int) -> None:
    record, long, short = OUTCOMES[outcome]
    result, buffer = make_result(verbosity)
    test = Sample("test_pass")
    if verbosity == 2:
        result.startTest(test)
        buffer.truncate(0)
        buffer.seek(0)
    record(result, test)
    expected = {0: "", 1: short, 2: long + "\n"}[verbosity]
    assert buffer.getvalue() == expected


def test_outcomes_are_recorded(make_result) -> None:
    result, _ = make_result()
    OUTCOMES["error"][0](result, Sample("test_error"))
    OUTCOMES["failure"][0](result, Sample("test_fail"))
    assert len(result.errors) == 1
    assert len(result.failures) == 1


def test_print_errors_colorizes_report(make_result) -> None:
    result, buffer = make_result(verbosity=0)
    unittest.TestSuite([Sample("test_fail"), Sample("test_error")]).run(result)
    result.printErrors()
    out = buffer.getvalue()
    assert colors.red(result.separator1) in out
    assert colors.red(f"FAIL: {result.getDescription(Sample('test_fail'))}") in out
    assert colors.red(f"ERROR: {result.getDescription(Sample('test_error'))}") in out
    assert colors.cyan("AssertionError: boom") in out
    assert colors.cyan("ValueError: kaboom") in out
