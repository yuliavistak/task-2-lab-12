"""
File: linkedbst.py
Author: Ken Lambert
"""

from math import log
from random import sample, shuffle
from time import time
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
# from linkedqueue import LinkedQueue

class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    def right(self, node: BSTNode):
        """
        Returns right child
        """
        return node.right

    def left(self, node: BSTNode):
        """
        Returns left child
        """
        return node.left

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            symb = ""
            if node is not None:
                symb += recurse(node.right, level + 1)
                symb += "| " * level
                symb += str(node.data) + "\n"
                symb += recurse(node.left, level + 1)
            return symb

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = []

        def recurse(node):
            if node is not None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) is not None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        # def recurse(node):
        #     if node is None:
        #         return None
        #     if item == node.data:
        #         return node.data
        #     if item < node.data:
        #         return recurse(node.left)
        #     return recurse(node.right)

        # return recurse(self._root)

        node = self._root
        while True:
            if node is None:
                break
            if item == node.data:
                break
            if item < node.data:
                node = node.left
            else:
                node = node.right

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        # def recurse(node):
        #     # New item is less, go left until spot is found
        #     if item < node.data:
        #         if node.left is None:
        #             node.left = BSTNode(item)
        #         else:
        #             recurse(node.left)
        #     # New item is greater or equal,
        #     # go right until spot is found
        #     elif node.right is None:
        #         node.right = BSTNode(item)
        #     else:
        #         recurse(node.right)
        #         # End of recurse

        # # Tree is empty, so new item goes at the root
        # if self.isEmpty():
        #     self._root = BSTNode(item)
        # # Otherwise, search for the item's spot
        # else:
        #     recurse(self._root)
        # self._size += 1

        if self.isEmpty():
            self._root = BSTNode(item)

        node = self._root
        while True:
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                    self._size += 1
                    break
                node = node.left
            elif node.right is None:
                node.right = BSTNode(item)
                self._size += 1
                break
            else:
                node = node.right

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentnode = top.left
            while not currentnode.right is None:
                parent = currentnode
                currentnode = currentnode.right
            top.data = currentnode.data
            if parent == top:
                top.left = currentnode.left
            else:
                parent.right = currentnode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        currentnode = self._root
        while not currentnode is None:
            if currentnode.data == item:
                item_removed = currentnode.data
                break
            parent = currentnode
            if currentnode.data > item:
                direction = 'L'
                currentnode = currentnode.left
            else:
                direction = 'R'
                currentnode = currentnode.right

        # Return None if the item is absent
        if item_removed is None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentnode.left is None \
                and not currentnode.right is None:
            lift_max_in_left_subtree_to_top(currentnode)
        else:

            # Case 2: The node has no left child
            if currentnode.left is None:
                new_child = currentnode.right

                # Case 3: The node has no right child
            else:
                new_child = currentnode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with new_item and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            if probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top: BSTNode):
            '''
            Helper function
            :param top:
            :return:
            '''
            if not top:
                return 0
            return 1 + max(height1(c) for c in (top.left, top.right))

        return height1(self._root) - 1

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        return self.height() < 2 * log(self._size + 1) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        nodes = list(self.inorder())
        index_low = nodes.index(low)
        index_high = nodes.index(high)
        return nodes[index_low:index_high+1]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        lst_nodes = list(self.inorder())
        self.clear()


        def rebalance1(nodes):
            if not nodes:
                return None
            mid = BSTNode(nodes[len(nodes)//2])
            if self.isEmpty():
                self._root = mid
            self._size += 1
            mid.left = rebalance1(nodes[:(len(nodes)//2)])
            mid.right = rebalance1(nodes[(len(nodes)//2 + 1):])

            return mid

        return rebalance1(lst_nodes)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        visited = None
        for i in self:
            if i > item:
                if visited is None:
                    visited = i
                elif i < visited:
                    visited = i
        return visited

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        visited = None
        for i in self:
            if i < item:
                if visited is None:
                    visited = i
                elif i > visited:
                    visited = i
        return visited

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        def read_file(path: str):
            with open(path, 'r', encoding = 'utf-8') as file:
                content = file.read().splitlines()[:20000]
            return content

        dictionary_sorted = read_file(path)
        print(1)
        dictionary_unsorted = dictionary_sorted + []
        shuffle(dictionary_unsorted)
        need = sample(dictionary_sorted, 10000)
        print(0)
        tree_from_sorted = LinkedBST(dictionary_sorted)
        print(5)
        tree_from_unsorted = LinkedBST(dictionary_unsorted)


        def task_1():
            print('Search in sorted list of words...')
            start1 = time()
            for wrd in need:
                dictionary_sorted.index(wrd)
            end1 = time()
            print(f'It took {end1-start1} seconds\n')

        def task_2():
            print('Search in binary search tree that made from sorted list of words...')
            start2 = time()
            for wrd in need:
                tree_from_sorted.find(wrd)
            end2 = time()
            print(f'It took {end2 - start2} seconds\n')

        def task_3():
            print('Search in binary search tree that made from unsorted list of words...')
            start3 = time()
            for wrd in need:
                tree_from_unsorted.find(wrd)
            end3 = time()
            print(f'It took {end3 - start3} seconds\n')

        def task_4():
            print('Search in rebalanced binary search tree...')
            start4 = time()
            tree_from_unsorted.rebalance()
            for wrd in need:
                tree_from_unsorted.find(wrd)
            end4 = time()
            print(f'It took {end4 - start4} seconds')

        task_1()
        task_2()
        task_3()
        task_4()

if __name__ == '__main__':
    tree = LinkedBST()
    tree.demo_bst('D:/UCU/UCU_OP/Week 26/binary_search_tree-master/words.txt')
