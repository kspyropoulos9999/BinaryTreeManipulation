"""
This code defines classes for binary trees and 
implements various tree traversal methods along with tree manipulation operations like adding,
deleting, and replacing nodes. Additionally, it generates a random binary tree and 
performs traversals on it, including inorder, preorder, and postorder. 
It also calculates the number of levels in the generated binary tree and counts nodes with only one child."""
import random


class Tree:
    class Position:
        def element(self):
            raise NotImplementedError('must be implemented by subclass')

        def __eq__(self, other):
            raise NotImplementedError('must be implemented by sublcass')

        def __ne__(self, other):
            return not (self == other)

    def root(self):
        raise NotImplementedError('must be implemented by sublcass')

    def parent(self, p):
        raise NotImplementedError('must be implemented by sublcass')

    def num_children(self, p):
        raise NotImplementedError('must be implemented by sublcass')

    def children(self, p):
        raise NotImplementedError('must be implemented by sublcass')

    def __len__(self):
        raise NotImplementedError('must be implemented by sublcass')

    def is_leaf(self):
        return len(self) == 0

    def is_empty(self):
        return len(self) == 0

    def is_root(self, p):
        return self.root == p

    def depth(self, p):
        if self.is_root(p):
            return 0
        else:
            return 1 + self.depth(self.parent(p))

    def _height1(self):
        return max(self.depth(p) for p in self.positions() if self.is_leaf(p))

    def _height2(self, p):
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self._height2(c) for c in self.children(p))

    def height(self, p=None):
        if p is None:
            p = self.root()
        return self._height2(p)

    def __iter__(self):
        for p in self.positions():
            yield p.element()

    def preorder(self):
        if not self.is_empty():
            for p in self._subtree_preorder(self.root()):
                yield p

    def _subtree_preorder(self, p):
        yield p
        for c in self.children(p):
            for other in self._subtree_preorder(c):
                yield other

    def positions(self):
        return self.preorder()

    def postorder(self):
        if not self.is_empty():
            for p in self._subtree_postorder(self.root()):
                yield p

    def _subtree_postorder(self, p):
        for c in self.children(p):
            for other in self._subtree_postorder(c):
                yield other
        yield p

    def breadthfirst(self):
        if not self.is_empty():
            fringe = LinkedQueue()
            fringe.enqueue(self.root())
            while not fringe.is_empty():
                p = fringe.dequeue()
                yield p
                for c in self.children(p):
                    fringe.enqueue(c)

    def inorder(self):
        if not self.is_empty():
            for p in self._subtree_inorder(self.root()):
                yield p

    def _subtree_inorder(self, p):
        if self.left(p) is not None:
            for other in self._subtree_inorder(self.left(p)):
                yield other
        yield p
        if self.right(p) is not None:
            for other in self._subtree_inorder(self.right(p)):
                yield other

    def positions(self):
        return self.inorder()


class BinaryTree(Tree):

    def left(self, p):
        raise NotImplementedError('must be implemented by sublclass')

    def right(self, p):
        raise NotImplementedError('must be implemented by sublclass')

    def sibling(self, p):
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p):
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)


class LinkedBinaryTree(BinaryTree):
    class _Node:
        __slots__ = '_element', '_parent', '_left', '_right'

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(BinaryTree.Position):
        def __init__(self, container, node):
            self._container = container
            self._node = node

        def element(self):
            return self._node._element

        def __eq__(self, other):
            return type(other) is type(self) and other._node is self._node

    def _validate(self, p):
        if not isinstance(p, self.Position):
            raise TypeError('p mist be proper Position type')
        if p._container is not self:
            raise ValueError('p does not belong to this container')
        if p._node._parent is p._node:
            raise ValueError('p is no longer valid')
        return p._node

    def _make_position(self, node):
        return self.Position(self, node) if node is not None else None

    def __init__(self):
        self._root = None
        self._size = 0

    def __len__(self):
        return self._size

    def root(self):
        return self._make_position(self._root)

    def parent(self, p):
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p):
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p):
        node = self._validate(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count

    def _add_root(self, e):
        if self._root is not None: raise ValueError('Root exists')
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_left(self, p, e):
        node = self._validate(p)
        if node._left is not None: raise ValueError('Left child exists')
        self._size += 1
        node._left = self._Node(e, node)
        return self._make_position(node._left)

    def _add_right(self, p, e):
        node = self._validate(p)
        if node._right is not None: raise ValueError('Right child exists')
        self._size += 1
        node._right = self._Node(e, node)
        return self._make_position(node._right)

    def _replace(self, p, e):
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self, p):
        node = self._validate(p)
        if self.num_children(p) == 2: raise ValueError('p has two children')
        child = node._left if node._left else node._right
        if child is not None:
            child._parent = node._parent
        if node is self._root:
            self._root = child
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node
        return node._element

    def _attach(self, p, t1, t2):
        node = self._validate(p)
        if not self.is_leaf(p): raise ValueError('position must be leaf')
        if not type(self) is type(t1) is type(t2):
            raise TypeError('Tree types must match')
        self._size += len(t1) + len(t2)
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1.root
            t1.root = None
            t1._size = 0
        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._root = None
            t2._size = 0

# enter input to start program
enterInput = input('Enter any key to start')

while enterInput != '0':
    # create binary tree
    tree = LinkedBinaryTree()

    # create random number
    randomNum = random.randint(1, 1000)

    # random number added as the root
    root_position = tree._add_root(randomNum)

    # add 50 numbers from 1 to 1000 to the binary tree
    for i in range(49):

        # pick random position to add the number
        random_position = random.choice(list(tree.positions()))

        # if left position of the random position is empty, put a node to the left
        if tree.left(random_position) is None:
            randomNum = random.randint(1, 1000)
            tree._add_left(random_position, randomNum)

        # if right position of the random position is empty, put a node to the right
        elif tree.right(random_position) is None:
            randomNum = random.randint(1, 1000)
            tree._add_right(random_position, randomNum)


    # print inorder traversal
    print("Inorder Traversal:")
    for position in tree.inorder():
        print(position.element())
    print()

    # print preorder traversal
    print("Preorder Traversal:")
    for position in tree.preorder():
        print(position.element())
    print()

    # print postorder traversal
    print("Postorder Traversal:")
    for position in tree.postorder():
        print(position.element())
    print()

    # print one child nodes count
    count = 0
    for position in tree.inorder():
        if tree.num_children(position) == 1:
            count += 1
    print('Count of one child nodes: ' + str(count))


    # calculate level of the tree
    def findLevel(tree, position, level):
        # if no more nodes are found, return the level
        if position is None:
            return level
        # if node is present, keep traversing nodes to get the level count
        elif position is not None:
            leftPosition = tree.left(position)
            rightPosition = tree.right(position)

            leftLevel = findLevel(tree, leftPosition, level + 1)
            rightLevel = findLevel(tree, rightPosition, level + 1)

            return max(leftLevel, rightLevel)


    print("Number of Levels in the Tree: ", findLevel(tree, tree.root(), -1))

    # ask user to calculate another random binary trree
    enterInput = input('Enter 0 to stop or ant key to continue')

