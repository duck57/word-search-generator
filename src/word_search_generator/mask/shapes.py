import inspect
import math
import sys
from typing import Tuple

from ..config import ACTIVE
from . import CompoundMask, Mask
from .ellipse import Ellipse
from .polygon import Rectangle, RegularPolygon, Star


def get_shape_objects():
    """Return all built-in shape objects from this file"""
    # {key:value for (key,value) in dictonary.items()}
    return [
        name
        for name, obj in inspect.getmembers(sys.modules[__name__], inspect.isclass)
        if obj.__module__ is __name__
    ]


class Circle(Ellipse):
    def __init__(self) -> None:
        super().__init__()


class Diamond(RegularPolygon):
    def __init__(self) -> None:
        super().__init__(vertices=4, angle=90)


class Donut(CompoundMask):
    def __init__(self) -> None:
        super().__init__()

    def generate(self, puzzle_size: int) -> None:
        self.puzzle_size = puzzle_size
        self._mask = Mask.build_mask(puzzle_size, ACTIVE)
        donut, hole = Donut.calculate_golden_donut_ratio(self.puzzle_size)
        self.masks = [
            Ellipse(donut, donut),
            Ellipse(hole, hole, method=3),
        ]
        for mask in self.masks:
            mask.generate(self.puzzle_size)
            self._apply_mask(mask)

    @staticmethod
    def calculate_golden_donut_ratio(puzzle_size: int) -> Tuple[int, int]:
        donut = puzzle_size - 1 if puzzle_size % 2 == 0 else puzzle_size
        hole = int(math.pow(puzzle_size - 2, 2) // (3 * (puzzle_size - 1)))
        if hole % 2 == 0:
            hole += 1
        return donut, hole


class Hexagon(RegularPolygon):
    def __init__(self) -> None:
        super().__init__(vertices=6, angle=90)


class Octagon(RegularPolygon):
    def __init__(self) -> None:
        super().__init__(vertices=8, angle=22.5)


class Pentagon(RegularPolygon):
    def __init__(self) -> None:
        super().__init__(vertices=5)


class Star5(Star):
    def __init__(self) -> None:
        super().__init__()


class Star6(CompoundMask):
    def __init__(self) -> None:
        super().__init__()
        self.masks = [
            (RegularPolygon()),
            (RegularPolygon(angle=180, method=2)),
        ]


class Star8(Star):
    def __init__(self) -> None:
        super().__init__(outer_vertices=8)


class Tree(CompoundMask):
    def __init__(self) -> None:
        super().__init__()

    def generate(self, puzzle_size: int) -> None:
        self.puzzle_size = puzzle_size
        self._mask = Mask.build_mask(puzzle_size, ACTIVE)
        # build the tree top
        tree_top = RegularPolygon(vertices=3)
        tree_top.generate(self.puzzle_size)
        tree_top_width = tree_top.points[2][0] - tree_top.points[1][0] + 1
        # calculate the tree trunk size and position
        tree_trunk_width = (
            tree_top_width // 4 + 1
            if tree_top_width // 4 % 2 == 0
            else tree_top_width // 4
        )
        tree_trunk_height = self.puzzle_size - tree_top.points[1][1]
        tree_trunk_position_x = (
            self.puzzle_size // 2 - tree_trunk_width // 2 - 1
            if self.puzzle_size % 2 == 0
            else self.puzzle_size // 2 - tree_trunk_width // 2
        )
        tree_trunk_position_y = tree_top.points[1][1]
        # build the tree trunk
        tree_trunk = Rectangle(
            width=tree_trunk_width,
            height=tree_trunk_height,
            origin=(
                tree_trunk_position_x,
                tree_trunk_position_y,
            ),
            method=2,
        )
        tree_trunk.generate(self.puzzle_size)
        self.masks = [tree_top, tree_trunk]
        for mask in self.masks:
            self._apply_mask(mask)


class Triangle(RegularPolygon):
    def __init__(self) -> None:
        super().__init__(vertices=3)


BUILTIN_SHAPES = get_shape_objects()
