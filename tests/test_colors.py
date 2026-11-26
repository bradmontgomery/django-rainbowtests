"""Tests for rainbowtests.colors."""

import pytest

from rainbowtests import colors

STYLERS = [colors.blue, colors.cyan, colors.green, colors.magenta, colors.red, colors.white]
STYLERS.append(colors.yellow)


@pytest.mark.parametrize("styler", STYLERS)
def test_wraps_text_in_ansi_codes(styler) -> None:
    result = styler("test")
    assert result.startswith("\x1b[")
    assert "test" in result
    assert result.endswith("\x1b[0m")


def test_colors_differ() -> None:
    assert colors.red("x") != colors.green("x")


def test_empty_string_returns_empty() -> None:
    assert colors.green("") == ""


def test_multiline_string_keeps_lines() -> None:
    result = colors.green("line1\nline2")
    assert "line1" in result
    assert "line2" in result
