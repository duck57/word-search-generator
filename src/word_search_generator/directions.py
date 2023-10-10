from .direction import ALL_DIRECTIONS, Direction, ds_not

ALL = ALL_DIRECTIONS
ANY = ALL
NONE = ds_not(ALL, True)
ZERO = NONE
DIAGONAL = Direction.matching_dirs("is_diagonal")
CARDINAL = Direction.matching_dirs("is_cardinal")
FORWARD = Direction.matching_dirs("is_forward")
BACKWARD = Direction.matching_dirs("is_backward")
LEFTWARD = Direction.matching_dirs("goes_left")
RIGHTWARD = Direction.matching_dirs("goes_right")
UPWARD = Direction.matching_dirs("goes_up")
DOWNWARD = Direction.matching_dirs("goes_down")
CROSSWORD = CARDINAL & FORWARD  # E or S
