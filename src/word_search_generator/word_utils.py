#!/usr/bin/env python

import random

from .utils import get_random_words
from .word import Word, WordList


def hundred_random_words(n: int = 100, max_length: int = 0) -> WordList:
    """
    Same as above but formatted into Word objects.
    Randomly assigns priority & secret status.
    """
    return sorted(
        Word(w, random.choice((True, False)), random.randint(1, 4))
        for w in get_random_words(n, max_length)
    )


if __name__ == "__main__":  # pragma: no cover
    print(
        "\n".join(
            f"{w.priority}-{len(w)}-{w.secret}\t{w}"
            for w in hundred_random_words(max_length=8)
        )
    )
