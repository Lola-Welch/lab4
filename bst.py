import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

BinTree : TypeAlias = Union["Node", None]

@dataclass (frozen = True)
class Node:
    value : Any
    left : BinTree
    right : BinTree
    


@dataclass (frozen=True)
class BinarySearchTree():
    comes_before = Callable[[Any, Any], bool]
    tree : BinTree
    

# determine whether a BST is empty or not
def is_empty(bst : BinarySearchTree) -> bool:
    match bst.tree:
        case Node(_,_,_):
            return False
        case None:
            return True


# sort through a BST to find where an accepted value should go (helper function for insert)
def insert_into_tree(c : Callable[[Any, Any], bool], t : BinTree, x : Any) -> BinTree:
    match t:
        case None:
            return Node(x, None, None)
        case Node(value, left, right):
            if c(x, value): # go to left
                return Node(value, insert_into_tree(c, left, x), right)
            else: 
                return Node(value, left, insert_into_tree(c, right, x))

#adds a value to a BinarySearchTree in the correct place
def insert (bst : BinarySearchTree, x : Any) -> BinarySearchTree:
    new_root = insert_into_tree(bst.comes_before, bst.tree, x)
    return BinarySearchTree(bst.comes_before, new_root)

#
def lookup(bst : BinarySearchTree, x : Any) -> bool:
    match bst.tree:
        case None:
            return False
        case Node(v, l, r):
            if x < v:
                return lookup()
            
def looks(t : BinTree, )