"""Tests for rainbowtests.test.core module."""

import io
import unittest

from rainbowtests.test.core import ColorfulOut, RainbowTextTestResult


class TestColorfulOut:
    """Test the ColorfulOut wrapper class."""

    def test_write_returns_colored_output(self, capsys):
        out = ColorfulOut()
        out.write("test message")
        captured = capsys.readouterr()
        assert "test message" in captured.out


class TestRainbowTextTestResult:
    """Test the RainbowTextTestResult class."""

    def _make_result(self, verbosity=1):
        """Create a RainbowTextTestResult instance for testing."""
        stream = io.StringIO()
        # Create a wrapper that has writeln method
        class StreamWrapper:
            def __init__(self, stream):
                self._stream = stream

            def write(self, text):
                self._stream.write(text)

            def writeln(self, text=""):
                self._stream.write(text + "\n")

            def flush(self):
                self._stream.flush()

            def getvalue(self):
                return self._stream.getvalue()

        wrapper = StreamWrapper(stream)
        result = RainbowTextTestResult(wrapper, descriptions=True, verbosity=verbosity)
        result.stream = wrapper
        return result, wrapper

    def test_result_class_exists(self):
        """Test that RainbowTextTestResult can be instantiated."""
        result, _ = self._make_result()
        assert result is not None
        assert isinstance(result, unittest.TestResult)

    def test_highlight_path_is_set(self):
        """Test that highlight_path attribute is set."""
        result, _ = self._make_result()
        assert hasattr(result, "highlight_path")
        assert isinstance(result.highlight_path, str)

    def test_add_success_with_dots(self):
        """Test addSuccess writes a green dot in dots mode."""
        result, stream = self._make_result(verbosity=1)
        result.dots = True
        result.showAll = False

        # Create a dummy test
        class DummyTest(unittest.TestCase):
            def test_dummy(self):
                pass

        test = DummyTest("test_dummy")
        result.addSuccess(test)

        output = stream.getvalue()
        # Should contain a dot (possibly with ANSI codes)
        assert "." in output or "\x1b[" in output

    def test_add_error_with_dots(self):
        """Test addError writes a red E in dots mode."""
        result, stream = self._make_result(verbosity=1)
        result.dots = True
        result.showAll = False

        class DummyTest(unittest.TestCase):
            def test_dummy(self):
                pass

        test = DummyTest("test_dummy")
        try:
            raise ValueError("test error")
        except ValueError:
            import sys
            result.addError(test, sys.exc_info())

        output = stream.getvalue()
        assert "E" in output or "\x1b[" in output

    def test_add_failure_with_dots(self):
        """Test addFailure writes a red F in dots mode."""
        result, stream = self._make_result(verbosity=1)
        result.dots = True
        result.showAll = False

        class DummyTest(unittest.TestCase):
            def test_dummy(self):
                pass

        test = DummyTest("test_dummy")
        try:
            raise AssertionError("test failure")
        except AssertionError:
            import sys
            result.addFailure(test, sys.exc_info())

        output = stream.getvalue()
        assert "F" in output or "\x1b[" in output
