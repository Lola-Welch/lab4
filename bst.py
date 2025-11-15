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

# determine whether a value is stored in a given BinarySearchTree
def lookup(bst : BinarySearchTree, x : Any) -> bool:
    return looks(bst.comes_before, bst.tree, x)

# helper function for lookup : finds if a value is in a BST   
def looks(cmp : Callable[[Any, Any], bool], t : BinTree, x : Any) -> bool:
    match t:
        case None:
            return False
        case Node(v, l, r):
            if (not cmp(x, v)) and (not cmp(v, x)):
                return True
            elif cmp(x, v):
                return looks(cmp, l, x)
            else:
                return looks(cmp, r, x)
            

#
def delete(bst : BinarySearchTree, x : Any) -> BinarySearchTree:
    return delete(bst.comes_before, bst.tree, x)

def d1(cmp : Callable[[Any, Any], bool], t : BinTree, x : Any)
    match t:
        case None:
            return BinarySearchTree(cmp, None)
        case Node(v, l, r):
            if cmp(x, v):
                return d1(cmp, l, x) 
            elif cmp(v, x):
                return d1(cmp, r, x)
            elif (not cmp(x, v)) and (not cmp(v, x)):
                