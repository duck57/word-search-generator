from .word import (
    ANY_DIRECTION,
    CARDINALS,
    DIAGONALS,
    FORWARD_DIRS,
    NO_DIRECTION,
    Direction,
)

# puzzle settings
min_puzzle_size = 5
max_puzzle_size = 50
min_puzzle_words = 1
max_puzzle_words = 100
max_fit_tries = 1000
hidden_word_priority = 2
secret_word_priority = 4

# puzzle grid settings
ACTIVE = "*"
INACTIVE = "#"

# puzzle difficulty levels
# should these all be frozen sets instead?
level_dirs = {
    -1: NO_DIRECTION,
    1: {  # right or down
        Direction.E,
        Direction.S,
    },
    2: FORWARD_DIRS,
    3: ANY_DIRECTION,
    4: {  # no E or S for better hiding
        # ANY_DIRECTION - {Direction.S, Direction.E}
        Direction.N,
        Direction.NE,
        Direction.SE,
        Direction.SW,
        Direction.W,
        Direction.NW,
    },
    5: {  # no E
        # ANY_DIRECTION - {Direction.E}
        Direction.N,
        Direction.NE,
        Direction.SE,
        Direction.S,
        Direction.SW,
        Direction.W,
        Direction.NW,
    },
    7: DIAGONALS,
    8: CARDINALS,
}

# pdf export settings
pdf_author = "Josh Duncan"
pdf_creator = "word-search @ joshbduncan.com"
pdf_title = "Word Search Puzzle"
pdf_font_size_XXL = 18
pdf_font_size_XL = 15
pdf_font_size_L = 12
pdf_font_size_M = 9
pdf_font_size_S = 5
pdf_puzzle_width = 7  # inches
