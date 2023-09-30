from . import directions as _d
from .direction import Direction, DirectionSet

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
level_dirs: dict[int, DirectionSet] = {
    -1: _d.NONE,
    1: _d.CARDINAL & _d.FORWARD,  # E or S, easy
    2: _d.FORWARD,
    3: _d.ALL,
    4: (_d.ALL - {Direction.S, Direction.E}),  # no E or S for better hiding
    5: _d.ALL - {Direction.E},  # anything but E
    7: _d.DIAGONAL,
    8: _d.CARDINAL,
    10: _d.BACKWARD,
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
