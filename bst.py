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
    comes_before : Callable[[Any, Any], bool]
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
            

# find and remove one value from a BinarySearchTree and return a new tree without that value
def delete(bst : BinarySearchTree, x : Any) -> BinarySearchTree:
    new_root = d1(bst.comes_before, bst.tree, x)
    return BinarySearchTree(bst.comes_before, new_root)

def d1(cmp : Callable[[Any, Any], bool], t : BinTree, x : Any) -> BinTree:
    match t:
        case None:
            return None
        case Node(v, l, r):
            
            if(not cmp(x, v)) and (not cmp(v, x)):
                if l is None:
                    return r
                if r is None:
                    return l
                next_node = r

                while isinstance(next_node.left, Node):
                    next_node = next_node.left
                
                # remove value
                new_right = d1(cmp, r, next_node.value)
                return Node(next_node.value, l, new_right)
            elif cmp(x, v):
                return Node(v, d1(cmp, l, x), r) 
            elif cmp(v, x):
                return Node(v, r, d1(cmp, r, x))
            

class Testing(unittest.TestCase):
    def setUp(self) -> None:
        self.cmp : Callable[[Any, Any], bool] = lambda a, b : a < b
        self.empty_bst = BinarySearchTree(self.cmp, None)
    
    #HELPER FUNCTIONS
    #create a BST with values from a given list
    def _build(self, values: List[Any])-> BinarySearchTree:
        bst = self.empty_bst
        for v in values:
            bst = insert(bst, v)
        return bst
    
    #verify that the list is in order
    def _inorder(self, t: BinTree) -> List[Any]:
        match t:
            case None:
                return []
            case Node(value=v, left=l, right=r):
                return self._inorder(l) + [v] + self._inorder(r)
            case _:
                raise TypeError("Unexpected BinTree variant")

    # is_empty
    def test_is_empty_on_new_tree(self):
        self.assertTrue(is_empty(self.empty_bst))

    def test_is_empty_after_insert(self):
        bst = insert(self.empty_bst, 5)
        self.assertFalse(is_empty(bst))

    # insert
    def test_insert_basic_structure_inorder_sorted(self):
        values = [5, 2, 8, 1, 3, 7, 9]
        bst = self._build(values)
        self.assertEqual(self._inorder(bst.tree), sorted(values))

    def test_insert_duplicates_route_right(self):
        values = [5, 5, 5]
        bst = self._build(values)
        self.assertEqual(self._inorder(bst.tree), [5, 5, 5])

    # lookup
    def test_lookup_present(self):
        bst = self._build([5, 2, 8, 1, 3])
        self.assertTrue(lookup(bst, 3))
        self.assertTrue(lookup(bst, 5))
        self.assertTrue(lookup(bst, 1))

    def test_lookup_absent(self):
        bst = self._build([5, 2, 8, 1, 3])
        self.assertFalse(lookup(bst, 7))
        self.assertFalse(lookup(bst, 42))

    # delete
    def test_delete_leaf(self):
        bst = self._build([5, 2, 8, 1, 3])
        bst = delete(bst, 1)  # delete a leaf
        self.assertEqual(self._inorder(bst.tree), [2, 3, 5, 8])

    def test_delete_one_child(self):
        # 8 has one left child (7)
        bst = self._build([5, 2, 8, 7])
        bst = delete(bst, 8)
        self.assertEqual(self._inorder(bst.tree), [2, 5, 7])

    def test_delete_two_children(self):
        # root (5) has two children; successor should be 7
        values = [5, 2, 8, 1, 3, 7, 9]
        bst = self._build(values)
        bst = delete(bst, 5)
        expected = sorted(values)
        expected.remove(5)
        self.assertEqual(self._inorder(bst.tree), expected)
        self.assertFalse(lookup(bst, 5))

    def test_delete_duplicate_removes_single_occurrence(self):
        bst = self._build([5, 5, 5, 2])
        bst = delete(bst, 5)
        self.assertEqual(self._inorder(bst.tree), [2, 5, 5])
        bst = delete(bst, 5)
        self.assertEqual(self._inorder(bst.tree), [2, 5])

    def test_delete_nonexistent_no_change(self):
        values = [5, 2, 8]
        bst = self._build(values)
        bst2 = delete(bst, 42)
        self.assertEqual(self._inorder(bst2.tree), sorted(values))
        # original bst remains unchanged (immutability)
        self.assertEqual(self._inorder(bst.tree), sorted(values))

    def test_delete_until_empty(self):
        values = [4, 2, 6, 1, 3, 5, 7]
        bst = self._build(values)
        for v in values:
            bst = delete(bst, v)
        self.assertTrue(is_empty(bst))
        self.assertEqual(self._inorder(bst.tree), [])


if (__name__ == '__main__'):
    unittest.main()
