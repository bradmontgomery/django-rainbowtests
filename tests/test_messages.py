"""Tests for rainbowtests.messages module."""

from rainbowtests import messages


class TestMessages:
    """Test message functions."""

    def test_random_happy_returns_string(self):
        result = messages.random_happy()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_random_sad_returns_string(self):
        result = messages.random_sad()
        assert isinstance(result, str)
        assert len(result) > 0

    def test_random_success_returns_happy(self):
        result = messages.random(success=True)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_random_failure_returns_sad(self):
        result = messages.random(success=False)
        assert isinstance(result, str)
        assert len(result) > 0

    def test_happy_messages_list_not_empty(self):
        assert len(messages.happy_messages) > 0

    def test_sad_messages_list_not_empty(self):
        assert len(messages.sad_messages) > 0
