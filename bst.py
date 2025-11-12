import sys
import unittest
from typing import *
from dataclasses import dataclass
sys.setrecursionlimit(10**6)

BinTree : TypeAlias = Union["Node", None]

@dataclass (frozen = True)
class Node:
    elt : Any
    left : BinTree
    right : BinTree
    

def comes_before():
    p


@dataclass (frozen=True)
class BinarySearchTree(self):
    elt = comes_before(Self
    tree : BinTree
    
#check this  : why is iit only allowing one argument for a BST?
# determine whether a BST is empty or not
def is_empty(bst : BinarySearchTree) -> bool:
    match bst:
        case BinarySearchTree(None):
            return True
        case BinarySearchTree(_):
            return False





def insert (bst : BinarySearchTree, value : Any) -> BinarySearchTree:
    