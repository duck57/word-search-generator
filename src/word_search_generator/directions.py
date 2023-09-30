from .direction import ALL_DIRECTIONS, Direction, ds_not

ALL = ALL_DIRECTIONS
ANY = ALL
NONE = ds_not(ALL, True)
ZERO = NONE
DIAGONAL = frozenset(d for d in ALL if d.is_diagonal)
CARDINAL = ds_not(DIAGONAL, True)
FORWARD = frozenset(
    {
        Direction.NE,
        Direction.E,
        Direction.SE,
        Direction.S,
    }
)
BACKWARD = ds_not(FORWARD, True)
