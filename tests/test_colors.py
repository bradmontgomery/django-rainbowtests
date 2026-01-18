"""Tests for rainbowtests.colors module."""

from rainbowtests import colors


class TestColorFunctions:
    """Test that color functions return ANSI-styled strings."""

    def test_green_returns_ansi_string(self):
        result = colors.green("test")
        assert "test" in result
        # Should contain ANSI escape sequences
        assert "\x1b[" in result or "\033[" in result

    def test_red_returns_ansi_string(self):
        result = colors.red("test")
        assert "test" in result
        assert "\x1b[" in result or "\033[" in result

    def test_blue_returns_ansi_string(self):
        result = colors.blue("test")
        assert "test" in result
        assert "\x1b[" in result or "\033[" in result

    def test_cyan_returns_ansi_string(self):
        result = colors.cyan("test")
        assert "test" in result
        assert "\x1b[" in result or "\033[" in result

    def test_yellow_returns_ansi_string(self):
        result = colors.yellow("test")
        assert "test" in result
        assert "\x1b[" in result or "\033[" in result

    def test_magenta_returns_ansi_string(self):
        result = colors.magenta("test")
        assert "test" in result
        assert "\x1b[" in result or "\033[" in result

    def test_white_returns_ansi_string(self):
        result = colors.white("test")
        assert "test" in result
        assert "\x1b[" in result or "\033[" in result

    def test_empty_string(self):
        result = colors.green("")
        # Should still return something (possibly just reset codes)
        assert isinstance(result, str)

    def test_multiline_string(self):
        result = colors.green("line1\nline2")
        assert "line1" in result
        assert "line2" in result
