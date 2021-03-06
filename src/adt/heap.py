
from __future__ import print_function

try:  # Python 2.x
    from collections import MutableMapping
except ImportError:  # Python 3.x
    from collections.abc import MutableMapping


class MinHeap(MutableMapping):

    def __init__(self):
        self._heap = []
        self._heap_index = {}

    def __setitem__(self, key, priority):
        if key in self._heap_index:
            self.update(key, priority)
        else:
            self.add(key, priority)

    def __getitem__(self, key):
        index = self._heap_index[key]
        return self._heap[index][0]

    def __delitem__(self, key):
        raise NotImplementedError('Cannot delete arbitrary element from heap')

    def __len__(self):
        return len(self._heap)

    def __str__(self):  # noqa
        level = 0
        i = 0
        for node in self._heap:
            print('{}'.format(node), end='')
            i += 1
            if i >= 2 ** level:
                level += 1
                i = 0
                print()

    def __iter__(self):  # Python 2.x
        return self

    def __next__(self):  # Python 3.x
        return self.next()

    @property
    def last_index(self):
        return len(self) - 1

    @property
    def root(self):
        return self._heap[0]

    def swap(self, i, j):
        # Swapping in Pythonic way
        self._heap[i], self._heap[j] = self._heap[j], self._heap[i]

        value_i = self._heap[i][1]
        self._heap_index[value_i] = i

        value_j = self._heap[j][1]
        self._heap_index[value_j] = j

    def next(self):
        if not self._heap:
            raise StopIteration

        self.swap(0, self.last_index)
        popped = self._heap.pop(self.last_index)
        del self._heap_index[popped[1]]

        if self._heap:
            self.bubble_down()

        return popped

    def add(self, value, priority):
        self._heap.append((priority, value))
        self._heap_index[value] = self.last_index
        self.bubble_up()

    def index(self, value):
        return self._heap_index[value]

    def update(self, value, priority):
        index = self.index(value)
        current_priority = self._heap[index][0]
        self._heap[index] = (priority, value)

        if priority > current_priority:
            self.bubble_down(index)
        else:
            self.bubble_up(index)

    def bubble_up(self, current_index=None):
        if current_index is None:
            current_index = self.last_index

        current = self._heap[current_index]
        parent_index, parent = self._get_parent(current_index)

        while parent and parent[0] > current[0]:
            self.swap(parent_index, current_index)

            current_index = parent_index
            parent_index, parent = self._get_parent(current_index)

    def bubble_down(self, current_index=None):
        if current_index is None:
            current_index = 0

        current = self._heap[current_index]
        child_index, child = self._get_lowest_priority_child(current_index)

        while child and child[0] < current[0]:
            self.swap(child_index, current_index)

            current_index = child_index
            child_index, child = self._get_lowest_priority_child(current_index)

    def _get_parent_index(self, index):
        if index == 0:
            return None

        if index % 2 == 0:
            parent_index = (index // 2) - 1
        else:
            parent_index = index // 2

        return parent_index

    def _get_parent(self, index):
        parent_index = self._get_parent_index(index)

        if parent_index is None:
            return None, None

        return parent_index, self._heap[parent_index]

    def _get_children_index(self, index):
        left = index * 2 + 1
        if left > self.last_index:
            left = None

        right = index * 2 + 2
        if right > self.last_index:
            right = None

        return left, right

    def _get_children(self, index):
        left, right = self._get_children_index(index)
        if left:
            left_child = self._heap[left]
        else:
            left_child = None

        if right:
            right_child = self._heap[right]
        else:
            right_child = None

        return (left, left_child), (right, right_child)

    def _get_lowest_priority_child(self, index):
        children = self._get_children(index)
        (left_index, left_child), (right_index, right_child) = children

        if not any((left_child, right_child)):
            return None, None

        if not right_child or left_child[0] < right_child[0]:
            return left_index, left_child

        return right_index, right_child
