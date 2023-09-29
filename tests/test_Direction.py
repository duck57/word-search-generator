from word_search_generator.word import (
    ANY_DIRECTION,
    BACKWARD_DIRS,
    FORWARD_DIRS,
    NO_DIRECTION,
    Direction,
    flip_dirs,
    toggle_ds,
)


def test_opposite():
    assert Direction.N.opposite is Direction.S


def test_is_cardinal():
    assert Direction.S.is_cardinal


def test_ds_toggle():
    assert toggle_ds(ANY_DIRECTION) == NO_DIRECTION


def test_flip_ds():
    assert flip_dirs(FORWARD_DIRS) == BACKWARD_DIRS
