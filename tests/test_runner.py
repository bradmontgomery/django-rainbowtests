"""Tests for rainbowtests.test.runner."""

import sys
import unittest
from unittest import mock

import pytest
from django.test.runner import DebugSQLTextTestResult, DiscoverRunner, PDBDebugResult
from django.test.utils import override_settings

from rainbowtests import colors, messages
from rainbowtests.test.core import ColorfulOut, RainbowTextTestResult
from rainbowtests.test.runner import RainbowDiscoverCoverageRunner, RainbowDiscoverRunner
from tests.conftest import Sample

HAPPY = {colors.green(m) for m in messages.happy_messages}
SAD = {colors.red(m) for m in messages.sad_messages}


def _suite(*names: str) -> unittest.TestSuite:
    return unittest.TestSuite(Sample(n) for n in names)


def test_is_a_discover_runner() -> None:
    assert issubclass(RainbowDiscoverRunner, DiscoverRunner)


class TestShowMessages:
    def test_defaults_to_true(self) -> None:
        assert RainbowDiscoverRunner(verbosity=0).show_messages is True

    @override_settings(RAINBOWTESTS_SHOW_MESSAGES=False)
    def test_uses_setting(self) -> None:
        assert RainbowDiscoverRunner(verbosity=0).show_messages is False


class TestResultClass:
    def test_default_is_rainbow(self) -> None:
        assert RainbowDiscoverRunner().get_resultclass() is RainbowTextTestResult

    def test_pdb_wins(self) -> None:
        assert RainbowDiscoverRunner(pdb=True).get_resultclass() is PDBDebugResult

    def test_debug_sql_wins(self) -> None:
        assert RainbowDiscoverRunner(debug_sql=True).get_resultclass() is DebugSQLTextTestResult

    def test_runner_kwargs_keep_django_flags(self) -> None:
        kwargs = RainbowDiscoverRunner(buffer=True, failfast=True).get_test_runner_kwargs()
        assert kwargs["buffer"] is True
        assert kwargs["failfast"] is True
        assert kwargs["resultclass"] is RainbowTextTestResult


class TestRunSuite:
    def test_success_prints_happy_message(self, capsys) -> None:
        result = RainbowDiscoverRunner(verbosity=0).run_suite(_suite("test_pass"))
        assert isinstance(result, RainbowTextTestResult)
        assert result.wasSuccessful()
        err = capsys.readouterr().err
        assert any(m in err for m in HAPPY)

    def test_failure_prints_sad_message(self, capsys) -> None:
        result = RainbowDiscoverRunner(verbosity=0).run_suite(_suite("test_fail"))
        assert not result.wasSuccessful()
        err = capsys.readouterr().err
        assert any(m in err for m in SAD)

    @override_settings(RAINBOWTESTS_SHOW_MESSAGES=False)
    def test_messages_can_be_disabled(self, capsys) -> None:
        RainbowDiscoverRunner(verbosity=0).run_suite(_suite("test_pass"))
        err = capsys.readouterr().err
        assert not any(m in err for m in HAPPY)

    def test_buffer_flag_is_honored(self, capsys) -> None:
        RainbowDiscoverRunner(verbosity=0, buffer=True).run_suite(_suite("test_noisy"))
        assert "noisy-output" not in capsys.readouterr().out


class TestCoverageRunner:
    def test_starts_and_reports_coverage(self) -> None:
        with mock.patch("coverage.Coverage") as cov_cls:
            runner = RainbowDiscoverCoverageRunner(verbosity=0)
            cov = cov_cls.return_value
            cov.start.assert_called_once_with()
            result = unittest.TestResult()
            assert runner.suite_result(_suite(), result) == 0
        cov.stop.assert_called_once_with()
        (call,) = cov.report.call_args_list
        assert isinstance(call.kwargs["file"], ColorfulOut)

    def test_works_without_coverage_installed(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setitem(sys.modules, "coverage", None)
        runner = RainbowDiscoverCoverageRunner(verbosity=0)
        assert runner._cov is None
        assert runner.suite_result(_suite(), unittest.TestResult()) == 0
