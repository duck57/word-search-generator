import word_search_generator.directions as d
from word_search_generator.direction import Direction, flip_dirs, toggle_ds


def test_opposite():
    assert Direction.N.opposite is Direction.S


def test_is_cardinal():
    assert Direction.S.is_cardinal and not Direction.NW.is_cardinal


def test_ds_toggle():
    assert toggle_ds(d.ALL) == set()


def test_flip_ds():
    assert flip_dirs(d.FORWARD) == d.BACKWARD


def test_direction_presets():
    assert d.NONE == set()
    assert d.CARDINAL & d.FORWARD == {Direction.E, Direction.S}
    assert len(d.ANY) == 8
    assert not (  # test exclusive pairs of presets
        (d.LEFTWARD & d.RIGHTWARD)
        | (d.UPWARD & d.DOWNWARD)
        | (d.FORWARD & d.BACKWARD)
        | (d.DIAGONAL & d.CARDINAL)
    )
