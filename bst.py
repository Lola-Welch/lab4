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
    

def comes_before(num1 : int, num2 : int) -> bool:
    return num1 > num2

def comes_before(char1 : str, char2 : str) -> bool:
    return ord(char1) > ord(char2)
    



@dataclass (frozen=True)
class BinarySearchTree(Self):
    comes_before : Callable[[Any, Any], bool]
    tree : BinTree
    
#check this  : why is iit only allowing one argument for a BST?
# determine whether a BST is empty or not
def is_empty(bst : BinarySearchTree) -> bool:
    match bst:
        case None:
            return True
        case BinarySearchTree(_):
            return False




def insert (bst : BinarySearchTree, value : Any) -> BinarySearchTree:

    bst = BinarySearchTree( bst.comes_before, None) # change
    insert_recurse(bst.tree, value)
    
    
    
    def insert_recurse(node : BinTree, value : Any) -> BinTree:
        if(bst.comes_before(value, node.elt)):
            if(node.left is None):
                return node
            return insert_recurse(value, node.left)
        else:
            if(node.right is None):
                return node
            return insert_recurse(value, node.right)
        
    def makeNewTree
        
        