from __future__ import annotations

import string
from abc import ABC, abstractmethod
from functools import wraps
from typing import TYPE_CHECKING, Iterable, TypeAlias

if TYPE_CHECKING:  # pragma: no cover
    from . import GameType
    from .game import Puzzle


Fit: TypeAlias = tuple[str, list[tuple[int, int]]]
Fits: TypeAlias = list[tuple[str, list[tuple[int, int]]]]

ALPHABET = list(string.ascii_uppercase)


class EmptyAlphabetError(Exception):
    """For when a `WordSearchGenerator` alphabet is empty."""

    def __init__(
        self, message="No valid alphabet characters provided to the generator."
    ):
        self.message = message
        super().__init__(self.message)


class WordFitError(Exception):
    pass


#  should this be moved to utils.py?
def retry(retries: int = 1000):
    """Custom retry decorator for retrying a function `retries` times.

    Args:
        retries (int, optional): Retry attempts. Defaults to 1000.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt > retries:
                        raise RuntimeError(
                            f"Tried {func.__name__} {retries} times without success"
                        ) from e
                    attempt += 1

        return wrapper

    return decorator


class Generator(ABC):
    """Base class for the puzzle generation algorithm.

    To implement your own `Generator`, subclass this class.

    Example:
        ```python
        class CoolGenerator(Generator):
            def generate(self,  *args, **kwargs) -> Puzzle:
                ...
        ```
    """

    def __init__(self, alphabet: str | Iterable[str] = ALPHABET) -> None:
        """Initialize a puzzle generator.

        Args:
            alphabet: Alphabet (letters) to use for the puzzle filler characters.
        """
        if alphabet:
            self.alphabet = list({c.upper() for c in alphabet if c.isalpha()})
        else:
            self.alphabet = ALPHABET

        if not self.alphabet:
            raise EmptyAlphabetError()

        self.puzzle: Puzzle = []

    @abstractmethod
    def generate(self, game: GameType) -> Puzzle:
        """Generate a puzzle.

        Args:
            game: The base `Game` object.

        Returns:
            The generated puzzle.
        """
