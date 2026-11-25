"""Rainbow test runners for Django."""

import sys
from typing import TYPE_CHECKING, Any
from unittest import TestResult, TestSuite, TextTestResult

from django.conf import settings
from django.test.runner import DiscoverRunner

from rainbowtests import messages
from rainbowtests.test.core import ColorfulOut, RainbowTextTestResult

if TYPE_CHECKING:
    from coverage import Coverage


class RainbowDiscoverRunner(DiscoverRunner):
    """Drop-in replacement for Django's DiscoverRunner with colorful output."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.show_messages: bool = getattr(settings, "RAINBOWTESTS_SHOW_MESSAGES", True)

    def get_resultclass(self) -> type[TextTestResult]:
        # Django returns a result class only for --pdb / --debug-sql; let those win.
        return super().get_resultclass() or RainbowTextTestResult

    def run_suite(self, suite: TestSuite, **kwargs: Any) -> TestResult:
        result = super().run_suite(suite, **kwargs)
        if self.show_messages:
            # unittest's TextTestRunner writes to stderr by default.
            sys.stderr.write(messages.random(result.wasSuccessful()) + "\n")
        return result


def _start_coverage() -> "Coverage | None":
    """Start and return a ``coverage.Coverage`` object, or None if not installed."""
    try:
        import coverage
    except ImportError:
        return None
    cov = coverage.Coverage()
    cov.start()
    return cov


class RainbowDiscoverCoverageRunner(RainbowDiscoverRunner):
    """RainbowDiscoverRunner that also prints a coverage report, if coverage is installed."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._cov = _start_coverage()

    def suite_result(self, suite: TestSuite, result: TestResult, **kwargs: Any) -> int:
        failures = super().suite_result(suite, result, **kwargs)
        if self._cov is not None:
            self._cov.stop()
            self._cov.report(file=ColorfulOut())
        return failures
