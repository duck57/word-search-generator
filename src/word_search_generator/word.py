from typing import Iterable, Literal, NamedTuple, TypeAlias, TypedDict

from . import directions as _dirs
from .direction import Direction, DirectionSet, ds_not, flip_dirs
from .validator import Validator


class Position(NamedTuple):
    row: int | None
    column: int | None


class KeyInfo(TypedDict):
    start: Position | None
    direction: Direction | None
    secret: bool


class KeyInfoJson(TypedDict):
    start_row: int | None
    start_col: int | None
    direction: str | None
    secret: bool


class Word:
    """This class represents a Word within a WordSearch puzzle."""

    def __init__(
        self,
        text: str,
        secret: bool = False,
        priority: int = 3,
        allowed_directions: DirectionSet = _dirs.FORWARD,
    ) -> None:
        """Initialize a Word Search puzzle Word."""
        self.text = text.upper().strip()
        self.start_row: int | None = None
        self.start_column: int | None = None
        self.coordinates: list[tuple[int, int]] = []
        self.direction: Direction | None = None
        self.secret = secret
        self.priority = priority
        self._allowed_directions = allowed_directions

    @property
    def allowed_directions(self) -> DirectionSet:
        return self._allowed_directions

    @allowed_directions.setter
    def allowed_directions(self, d: DirectionSet) -> None:
        self._allowed_directions = d

    def validate(
        self, validators: Iterable[Validator], placed_words: list[str]
    ) -> bool:
        """Validate the word against a list of validators.

        Args:
            validators (list[Validator]): Validators to test.
            placed_words (list[str]): Words already on the board

        Raises:
            TypeError: Incorrect validator type provided.

        Returns:
            bool: Word passes all validators.
        """
        for validator in validators:
            if not isinstance(validator, Validator):
                raise TypeError(f"Invalid validator: {validator}.")
            if not validator.validate(self.text, placed_words=placed_words):
                return False
        return True

    @property
    def placed(self) -> bool:
        """Is the word currently placed in a puzzle.

        Note: Used `is not None` since 0 vals for start_row/column are not truthy
        """
        return all(
            (
                self.start_column is not None,
                self.start_row is not None,
                self.direction is not None,
            )
        )

    @property
    def position(self) -> Position:
        """Current start position of the word in the puzzle
        as (start_row, start_column)."""
        return Position(self.start_row, self.start_column)

    @position.setter
    def position(self, value: Position) -> None:
        """Set the start position of the Word in the puzzle.

        Args:
            value (Position): Tuple of (row, column)
        """
        self.start_row = value.row
        self.start_column = value.column

    @property
    def position_xy(self) -> Position:
        """Returns the word position with 1-based indexing
        and a familiar (x, y) coordinate system"""
        return Position(
            self.start_row + 1 if self.start_row is not None else self.start_row,
            self.start_column + 1
            if self.start_column is not None
            else self.start_column,
        )

    @property
    def key_info(self) -> KeyInfo:
        """Returns the Word placement information formatted
        correctly for a WordSearch puzzle key."""
        return {
            "start": self.position,
            "direction": self.direction,
            "secret": self.secret,
        }

    @property
    def key_info_json(self) -> KeyInfoJson:
        """Returns the Word placement information formatted
        correctly for a WordSearch puzzle key used in the JSON property."""
        return {
            "start_row": self.start_row,
            "start_col": self.start_column,
            "direction": self.direction.name if self.direction else None,
            "secret": self.secret,
        }

    def key_string(self, bbox: tuple[tuple[int, int], tuple[int, int]]) -> str:
        """Returns a string representation of the Word placement
        information formatted correctly for a WordSearch puzzle key
        when the WordSearch object it output using the `print()` or
        `.show()` method.

        Args:
            bbox (tuple[tuple[int, int], tuple[int, int]]): The current
                puzzle bounding box. Used to offset the coordinates when
                the puzzle has been masked and is no longer it's original
                size.
        """
        if self.placed:
            col, row = self.offset_position_xy(bbox)
            return (
                f"{'*' if self.secret else ''}{self.text} "
                + f"{self.direction.name if self.direction else self.direction}"
                + f" @ {(col, row)}"
            )
        return ""

    def offset_position_xy(
        self, bbox: tuple[tuple[int, int], tuple[int, int]]
    ) -> Position:
        """Returns a string representation of the word position with
        1-based indexing and a familiar (x, y) coordinate system. The
        position will be offset by the puzzle bounding box when a puzzle
        has been masked.

        Args:
            bbox (tuple[tuple[int, int], tuple[int, int]]): The current
                puzzle bounding box.
        """
        return Position(
            self.start_column + 1 - bbox[0][0]
            if self.start_column is not None
            else self.start_column,
            self.start_row + 1 - bbox[0][1]
            if self.start_row is not None
            else self.start_row,
        )

    def offset_coordinates(
        self, bbox: tuple[tuple[int, int], tuple[int, int]]
    ) -> list[Position]:
        """Returns a list of the Word letter coordinates, offset
        by the puzzle bounding box.

        Args:
            bbox (tuple[tuple[int, int], tuple[int, int]]): The current
                puzzle bounding box.
        """
        return [
            Position(
                x + 1 - bbox[0][0] if x is not None else x,
                y + 1 - bbox[0][1] if y is not None else y,
            )
            for y, x in self.coordinates
        ]

    def remove_from_puzzle(self) -> None:
        """Remove word placement details when a puzzle is reset."""
        self.start_row = None
        self.start_column = None
        self.coordinates = []
        self.direction = None

    def flip_allowed_dirs(self) -> None:
        self._allowed_directions = flip_dirs(self._allowed_directions)

    def toggle_allowed_dirs(self) -> None:
        """Switches which directions are allows and which as invalid."""
        self._allowed_directions = ds_not(self._allowed_directions)

    def merge(
        self, w2: "Word", method: Literal["|", "&", "^", "and", "or"] = "|"
    ) -> "Word":
        """Merges identical Words."""
        return merge_words(self, w2, method=method)

    def __and__(self, other: "Word") -> "Word":
        return self.merge(other, "&")

    def __bool__(self) -> bool:
        """Returns the truthiness of a word.
        Should always return true, except for the null word."""
        return bool(self.text)

    def __eq__(self, __o: object) -> bool:
        """Returns True if both instances have the text."""
        if not isinstance(__o, Word):
            return False
        return self.text == __o.text

    def equivalent_settings(self, __o: "Word") -> bool:
        return (
            self == __o
            and self.secret == __o.secret
            and self.priority == __o.priority
            and self.allowed_directions == __o.allowed_directions
        )

    def __hash__(self) -> int:
        """Returns the hashes value of the word text."""
        return hash(self.text)

    def __len__(self) -> int:
        """Returns the length of the word text."""
        return len(self.text)

    def __lt__(self, other: "Word") -> bool:
        """
        Sort. The lesser word sort first in a list.

        1. Lowest priority
        2. Shortest length
        3. Secrets go last
        4. All else equal, alphabetical
        """
        if self.priority == other.priority:
            if len(self) == len(other):
                if self.secret == other.secret:
                    return self.text < other.text  # alphabetical as last resort
                return not self.secret  # Secret words sort last as tiebreak
            return len(self) > len(other)
        return self.priority < other.priority

    def __or__(self, other: "Word") -> "Word":
        return self.merge(other)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('{self.text}', " + f"{self.secret})"

    def __str__(self) -> str:
        return self.text

    def __xor__(self, other) -> "Word":
        return self.merge(other, "^")


def merge_words(
    *words: Word, method: Literal["|", "&", "^", "and", "or"] = "|"
) -> Word:
    if len(words) == 1:
        return words[0]
    t = ""
    p = 2048
    d = set()
    s = True

    # all this to avoid looping through the list with four separate comprehensions
    for w in words:
        if w.text != t:
            if not w:
                continue  # skip empties
            if t:
                raise ValueError(
                    "Words must have identical text to merge.\n\t" + f"{w} != {t}"
                )
            else:
                t = w.text  # set the prototype
        s = s and w.secret
        p = min(p, w.priority)
        # there has to be a better way for d
        d = eval(f"d {method} w.allowed_directions")
    if not t:  # no word has text
        return NULL_WORD  # or raise ValueError?
    return Word(t, s, p, d)


WordSet: TypeAlias = set[Word]
WordList: TypeAlias = list[Word]
NULL_WORD = Word("", True, 999, _dirs.NONE)
