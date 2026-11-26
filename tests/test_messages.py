"""Tests for rainbowtests.messages."""

from rainbowtests import colors, messages


def test_message_lists_not_empty() -> None:
    assert messages.happy_messages
    assert messages.sad_messages


def test_random_happy_is_green_happy_message() -> None:
    assert messages.random_happy() in {colors.green(m) for m in messages.happy_messages}


def test_random_sad_is_red_sad_message() -> None:
    assert messages.random_sad() in {colors.red(m) for m in messages.sad_messages}


def test_random_picks_by_success() -> None:
    assert messages.random(True) in {colors.green(m) for m in messages.happy_messages}
    assert messages.random(False) in {colors.red(m) for m in messages.sad_messages}
