import io
import unittest
from collections.abc import Callable
from unittest.runner import _WritelnDecorator

import django
import pytest
from django.conf import settings

from rainbowtests.test.core import RainbowTextTestResult


def pytest_configure() -> None:
    """Configure Django settings for tests."""
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                "default": {
                    "ENGINE": "django.db.backends.sqlite3",
                    "NAME": ":memory:",
                }
            },
            INSTALLED_APPS=[
                "django.contrib.contenttypes",
                "django.contrib.auth",
            ],
            SECRET_KEY="test-secret-key-for-rainbowtests",
            USE_TZ=True,
        )
        django.setup()


class Sample(unittest.TestCase):
    """Throwaway test case whose methods pass, fail, or error on purpose."""

    __test__ = False  # run explicitly by our tests, never collected by pytest

    def test_pass(self) -> None:
        pass

    def test_fail(self) -> None:
        self.fail("boom")

    def test_error(self) -> None:
        raise ValueError("kaboom")

    def test_noisy(self) -> None:
        print("noisy-output")


@pytest.fixture
def make_result() -> Callable[..., tuple[RainbowTextTestResult, io.StringIO]]:
    """Build a RainbowTextTestResult writing to an in-memory stream."""

    def _make(verbosity: int = 1) -> tuple[RainbowTextTestResult, io.StringIO]:
        buffer = io.StringIO()
        stream = _WritelnDecorator(buffer)
        return RainbowTextTestResult(stream, descriptions=True, verbosity=verbosity), buffer

    return _make
