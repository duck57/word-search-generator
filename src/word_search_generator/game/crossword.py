from typing import Iterable, TypeAlias

from .. import utils
from ..config import max_puzzle_words, min_puzzle_words
from ..formatter.word_search_formatter import WordSearchFormatter
from ..generator import CrosswordGenerator
from ..utils import get_random_words
from ..validator import NoPunctuation, NoSingleLetterWords
from ..word import Direction, Word, WordSet
from . import Game

Puzzle: TypeAlias = list[list[str]]



class Crossword(Game):
    DEFAULT_GENERATOR = CrosswordGenerator()
    DEFAULT_VALIDATORS = [NoPunctuation(), NoSingleLetterWords()]
    DEFAULT_FORMATTER = WordSearchFormatter()

    def cleanup_input(self, words: str, secret: bool = False) -> WordSet:
        """The expected format of a Crossword input is one word per line."""
        return {self.new_word(w) for w in words.splitlines()}

    @staticmethod
    def new_word(w: str) -> Word:
        """
        Creates a crossword Word from a tab-delimited string with the following fields:

        1. The word to include on the search
        2. The hint to display
        3. Optionally, a priority for building
        4. Any further fields are ignored (use them as developer comments or something)

        Word.description is used for the hint.
        """
        word, hint, *priority = w.split("\t")
        return Word(
            word, False, int(priority[0]) if priority else 2, {ACROSS, DOWN}, hint
        )

    @property
    def words_across(self) -> WordSet:
        return {w for w in self._words if w.direction == ACROSS}

    @property
    def words_down(self) -> WordSet:
        return {w for w in self._words if w.direction == DOWN}

    def random_words(self, w: int) -> None:
        """Generates a Crossword with w random words,
        each word used as its own hint.  For testing."""
        if not isinstance(w, int):
            raise TypeError("Size must be an integer.")
        if not min_puzzle_words <= w <= max_puzzle_words:
            raise ValueError(
                f"Requested random words must be >= {min_puzzle_words}"
                + f" and <= {max_puzzle_words}."
            )
        self.replace_words("\n".join(f"{word}\t{word}" for word in get_random_words(w)))
