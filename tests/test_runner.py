"""Tests for rainbowtests.test.runner module."""

import unittest

from rainbowtests.test.core import RainbowTextTestResult
from rainbowtests.test.runner import RainbowDiscoverRunner


class TestRainbowDiscoverRunner:
    """Test the RainbowDiscoverRunner class."""

    def test_runner_inherits_from_discover_runner(self):
        """Test that RainbowDiscoverRunner inherits from DiscoverRunner."""
        from django.test.runner import DiscoverRunner
        assert issubclass(RainbowDiscoverRunner, DiscoverRunner)

    def test_runner_can_be_instantiated(self):
        """Test that RainbowDiscoverRunner can be instantiated."""
        runner = RainbowDiscoverRunner(verbosity=0)
        assert runner is not None

    def test_runner_has_show_messages_attribute(self):
        """Test that the runner has show_messages attribute."""
        runner = RainbowDiscoverRunner(verbosity=0)
        assert hasattr(runner, "show_messages")
        # Default should be True
        assert runner.show_messages is True

    def test_run_suite_uses_rainbow_result_class(self):
        """Test that run_suite injects RainbowTextTestResult."""
        runner = RainbowDiscoverRunner(verbosity=0)

        # Create a simple test suite with one passing test
        class SimpleTest(unittest.TestCase):
            def test_pass(self):
                pass

        suite = unittest.TestSuite()
        suite.addTest(SimpleTest("test_pass"))

        # Run the suite - this should use RainbowTextTestResult
        result = runner.run_suite(suite)

        # Verify the result is the right type
        assert isinstance(result, RainbowTextTestResult)

    def test_run_suite_returns_result(self):
        """Test that run_suite returns a test result object."""
        runner = RainbowDiscoverRunner(verbosity=0)

        class SimpleTest(unittest.TestCase):
            def test_pass(self):
                pass

        suite = unittest.TestSuite()
        suite.addTest(SimpleTest("test_pass"))

        result = runner.run_suite(suite)

        assert hasattr(result, "wasSuccessful")
        assert result.wasSuccessful()
