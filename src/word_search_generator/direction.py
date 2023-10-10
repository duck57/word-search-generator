from enum import Enum, unique
from typing import Callable, TypeAlias

DirTuple: TypeAlias = tuple[int, int]
DirectionSet: TypeAlias = "set[Direction] | frozenset[Direction]"


@unique
class Direction(Enum):
    """
    If you want custom directions, like `"skipE": (0, 2)`, this is the
    place to monkey-patch them in.

    Tuples are listed in (∂row, ∂col, forward) triples
    """

    N: DirTuple = (-1, 0)
    NE: DirTuple = (-1, 1)
    E: DirTuple = (0, 1)
    SE: DirTuple = (1, 1)
    S: DirTuple = (1, 0)
    SW: DirTuple = (1, -1)
    W: DirTuple = (0, -1)
    NW: DirTuple = (-1, -1)

    @property
    def r_move(self) -> int:
        return self.value[0]

    @property
    def c_move(self) -> int:
        return self.value[1]

    @property
    def opposite(self) -> "Direction":
        # This may break with monkey-patched directions
        return Direction((-self.r_move, -self.c_move))

    @property
    def is_diagonal(self) -> bool:
        return self.r_move != 0 and self.c_move != 0

    @property
    def is_cardinal(self) -> bool:
        return not self.is_diagonal

    @property
    def goes_left(self) -> bool:
        return self.c_move < 0

    @property
    def goes_right(self) -> bool:
        return self.c_move > 0

    @property
    def goes_up(self) -> bool:
        return self.r_move < 0

    @property
    def goes_down(self) -> bool:
        return self.r_move > 0

    @property
    def is_forward(self) -> bool:
        return self.c_move >= 0 and self.r_move + self.c_move > -1

    @property
    def is_backward(self) -> bool:
        return self.c_move <= 0 and self.r_move + self.c_move < 1

    @classmethod
    def matching_dirs(cls, by_prop: str, reverse: bool = False) -> DirectionSet:
        return frozenset(
            d
            for d in cls.__members__.values()
            if (getattr(d, by_prop.lower().strip()) ^ reverse)
        )

    @classmethod
    def all(cls) -> DirectionSet:
        return frozenset(cls.__members__.values())


ALL_DIRECTIONS = Direction.all()
ACROSS = Direction.E
DOWN = Direction.S


def ds_not(ds: DirectionSet, freeze: bool = False) -> DirectionSet:
    """Essentially DirectionSet.__not__()"""
    s: Callable[..., DirectionSet] = frozenset if freeze else set
    return s(ALL_DIRECTIONS - ds)


toggle_ds = ds_not


def flip_dirs(ds: DirectionSet, freeze: bool = False) -> DirectionSet:
    """a.k.a. opposite_dirs()"""
    s: Callable[..., DirectionSet] = frozenset if freeze else set
    return s(d.opposite for d in ds)
