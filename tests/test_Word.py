import pytest

from word_search_generator.word import (
    ANY_DIRECTION,
    NO_DIRECTION,
    NULL_WORD,
    Direction,
    Position,
    Word,
)


def test_empty_start_row():
    w = Word("test")
    assert not w.start_row


def test_empty_start_column():
    w = Word("test")
    assert not w.start_column


def test_empty_position():
    w = Word("test")
    assert w.position == Position(None, None)


def test_position_xy():
    w = Word("test")
    w.start_row = 1
    w.start_column = 1
    assert w.position_xy == Position(2, 2)


def test_empty_position_xy():
    w = Word("test")
    assert w.position_xy == Position(None, None)


def test_position_setter():
    p = Position(1, 2)
    w = Word("test")
    w.position = p
    assert w.start_row == p.row and w.start_column == p.column


def test_inequality():
    w = Word("test")
    assert w != "test"


def test_repr():
    w = Word("test")
    w.direction = Direction.S
    w.position = Position(1, 2)
    assert eval(repr(w)) == w


def test_str():
    w = Word("test")
    assert str(w) == "test".upper()


def test_empty_key_string():
    w = Word("test")
    assert w.key_string(((0, 0), (10, 10))) == ""


def test_offset_empty_position_xy():
    w = Word("test")
    assert w.offset_position_xy(((0, 0), (10, 10))) == Position(None, None)


def test_word_length():
    w = Word("test")
    assert len(w) == 4


def test_word_bool_true():
    w = Word("test")
    assert w


def test_word_bool_false():
    w = Word("")
    assert not w


def test_set_directions():
    w = Word("test")
    w.allowed_directions = NO_DIRECTION
    w.toggle_allowed_dirs()
    w.flip_allowed_dirs()
    assert w.allowed_directions == ANY_DIRECTION


high_priority_secret = Word("test", True, 1, NO_DIRECTION)
low_priority_word = Word("test", False, 93, ANY_DIRECTION)


def test_successful_merge():
    w = low_priority_word ^ high_priority_secret
    assert w.allowed_directions == ANY_DIRECTION
    assert w.secret is False
    assert w.priority == 1


def test_word_and_merge():
    assert high_priority_secret.equivalent_settings(high_priority_secret & NULL_WORD)


def test_word_xor_merge():
    assert low_priority_word.equivalent_settings(NULL_WORD ^ low_priority_word)


def test_invalid_merge():
    with pytest.raises(ValueError):
        high_priority_secret | Word("nope.")
