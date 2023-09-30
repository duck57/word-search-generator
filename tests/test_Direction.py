import word_search_generator.directions as d
from word_search_generator.direction import Direction, flip_dirs, toggle_ds


def test_opposite():
    assert Direction.N.opposite is Direction.S


def test_is_cardinal():
    assert Direction.S.is_cardinal


def test_ds_toggle():
    assert toggle_ds(d.ALL) == set()


def test_flip_ds():
    assert flip_dirs(d.FORWARD) == d.BACKWARD
