from enum import Enum, unique
from typing import Callable, TypeAlias


@unique
class Direction(Enum):
    """
    If you want custom directions, like `"skipE": (0, 2)`, this is the
    place to monkey-patch them in.

    Tuples are listed in (∂row, ∂col) pairs, presumably b/c that makes
    it easier to use with the Puzzle = list[list[chr]] format
    """

    # is there a better way to specify typing here?
    # without hints here, the linter gets upset with my definitions of r/c_move
    N: tuple[int, int] = (-1, 0)  # type: ignore
    NE: tuple[int, int] = (-1, 1)  # type: ignore
    E: tuple[int, int] = (0, 1)  # type: ignore
    SE: tuple[int, int] = (1, 1)  # type: ignore
    S: tuple[int, int] = (1, 0)  # type: ignore
    SW: tuple[int, int] = (1, -1)  # type: ignore
    W: tuple[int, int] = (0, -1)  # type: ignore
    NW: tuple[int, int] = (-1, -1)  # type: ignore

    @property
    def r_move(self) -> int:
        return self.value[0]

    @property
    def c_move(self) -> int:
        return self.value[1]

    @property
    def opposite(self) -> "Direction":
        return Direction((-self.r_move, -self.c_move))

    @property
    def is_diagonal(self) -> bool:
        return self.r_move != 0 and self.c_move != 0

    @property
    def is_cardinal(self) -> bool:
        return not self.is_diagonal


DirectionSet: TypeAlias = set[Direction] | frozenset[Direction]
ALL_DIRECTIONS = frozenset(Direction.__members__.values())


def ds_not(ds: DirectionSet, freeze: bool = False) -> DirectionSet:
    """Essentially DirectionSet.__not__()"""
    s: Callable[..., DirectionSet] = frozenset if freeze else set
    return s(ALL_DIRECTIONS - ds)


toggle_ds = ds_not


def flip_dirs(ds: DirectionSet, freeze: bool = False) -> DirectionSet:
    """a.k.a. opposite_dirs()"""
    s: Callable[..., DirectionSet] = frozenset if freeze else set
    return s(d.opposite for d in ds)
