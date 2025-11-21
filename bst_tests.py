import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)
from bst import *
from bst import BinarySearchTree, insert, lookup, delete, is_empty


# --- Simple 2D point class for distance comparator ---
class Point2:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    def __repr__(self) -> str:
        return f"Point2({self.x}, {self.y})"


# comparators

#ints
def cmp_num(a: int, b: int) -> bool:
    return a < b


#strs
def cmp_str(a: str, b: str) -> bool:
    return a < b

# Compare by squared Euclidean distance to (0,0)
def cmp_point(p1: Point2, p2: Point2) -> bool:
    d1 = p1.x * p1.x + p1.y * p1.y
    d2 = p2.x * p2.x + p2.y * p2.y
    return d1 < d2


class BSTTests(unittest.TestCase):
    def test_numeric_ordering(self):
        bst = BinarySearchTree(comes_before=cmp_num, tree=None)
        self.assertTrue(is_empty(bst))

        bst = insert(bst, 5)
        bst = insert(bst, 2)
        bst = insert(bst, 8)

        self.assertTrue(lookup(bst, 5))
        self.assertTrue(lookup(bst, 2))
        self.assertFalse(lookup(bst, 10))

        bst = delete(bst, 2)
        self.assertFalse(lookup(bst, 2))

    def test_string_ordering(self):
        bst = BinarySearchTree(comes_before=cmp_str, tree=None)

        bst = insert(bst, "banana")
        bst = insert(bst, "apple")
        bst = insert(bst, "cherry")

        self.assertTrue(lookup(bst, "banana"))
        self.assertTrue(lookup(bst, "apple"))
        self.assertFalse(lookup(bst, "date"))

        bst = delete(bst, "apple")
        self.assertFalse(lookup(bst, "apple"))

    def test_point2_distance_ordering(self):
        bst = BinarySearchTree(comes_before=cmp_point, tree=None)

        p_close = Point2(1, 1)   # sqrt(2)
        p_mid   = Point2(2, 2)   # sqrt(8)
        p_far   = Point2(3, 0)   # 3

        bst = insert(bst, p_mid)
        bst = insert(bst, p_close)
        bst = insert(bst, p_far)

        self.assertTrue(lookup(bst, p_close))
        self.assertTrue(lookup(bst, p_far))
        self.assertFalse(lookup(bst, Point2(4, 4)))

        bst = delete(bst, p_close)
        self.assertFalse(lookup(bst, p_close))


if __name__ == "__main__":
    unittest.main()
