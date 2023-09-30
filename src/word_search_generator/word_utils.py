#!/usr/bin/env python

import random

from .utils import get_random_words, show_wl_stats
from .word import Word, WordList


def hundred_random_words(
    n: int = 100, max_length: int = 0, min_length: int = 4
) -> WordList:
    """
    Same as above but formatted into Word objects.
    Randomly assigns priority & secret status.
    """
    return sorted(
        Word(w, random.choice((True, False)), random.randint(1, 4))
        for w in get_random_words(n, max_length, min_length)
    )


def print_random_words():  # pragma: no cover
    print(
        "\n".join(
            f"{w.priority}-{len(w)}-{w.secret}\t{w}"
            for w in hundred_random_words(max_length=8)
        )
    )


if __name__ == "__main__":  # pragma: no cover
    print_random_words()
    print()
    show_wl_stats()
