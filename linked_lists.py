""" Linked-node based implementation of List ADT. """
import node
from abstract_list import List, T


__author__ = 'Maria Garcia de la Banda and Brendon Taylor. Modified by Alexey Ignatiev'
__docformat__ = 'reStructuredText'

class LinkedList(List[T]):
    """ List ADT implemented with linked nodes. """
    def __init__(self, dummy_capacity=1) -> None:
        """ Linked-list object initialiser. """
        super(LinkedList, self).__init__()
        self.head = None

    def clear(self):
        """ Clear the list. """
        # first call clear() for the base class
        super(LinkedList, self).clear()
        self.head = None

    def __setitem__(self, index: int, item: T) -> None:
        """ Magic method. Insert the item at a given position. """
        node_at_index = self.__get_node_at_index(index)
        node_at_index.item = item

    def __getitem__(self, index: int) -> T:
        """ Magic method. Return the element at a given position. """
        node_at_index = self.__get_node_at_index(index)
        return node_at_index.item

    def index(self, item: T) -> int:
        """ Find the position of a given item in the list. """
        return node.index(self.head, item)

    def __get_node_at_index(self, index: int) -> node.Node[T]:
        """ Get node object at a given position. """
        if 0 <= index and index < len(self):
            return node.get_node_at_index(self.head, index)
        else:
            raise ValueError('Index out of bounds')

    def delete_at_index(self, index: int) -> T:
        """ Delete item at a given position. """
        try:
            previous_node = self.__get_node_at_index(index-1)
        except ValueError as e:
            if self.is_empty():
                raise ValueError('List is empty')
            elif index == 0:
                item = self.head.item
                self.head = self.head.next
            else:
                raise e
        else:
            item = previous_node.next.item
            previous_node.next = previous_node.next.next
        self.length -= 1
        return item

    def insert(self, index: int, item: T) -> None:
        """ Insert an item at a given position. """
        new_node = node.Node(item)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            previous_node = self.__get_node_at_index(index - 1)
            new_node.next = previous_node.next
            previous_node.next = new_node
        self.length += 1

    def __iter__(self):
        return LinkedListIterator(self.head)

class LinkedListIterator:
    """ an iterator for the the linked list 
    attributes:
        current (Node) - the current node of the item which was just returned
        prev (Node) - the node of the item which was returned in the previous iter
        is_first_it (bool) - used to display the first node instead of skipping it

    complexity:
        unless otherwise stated all methods have a complexity of O(1)
    """

    def __init__(self, node:node.Node) -> None:
        """ initialises class attributes"""
        self.current = node
        self.prev = None
        self.is_first_it = True
        
    def __iter__(self):
        return self 

    def __next__(self):
        """ iterates through the linked nodes, stoping when the current node is none"""
        if self.is_first_it:
            self.is_first_it = False
            return self.current.item
        
        self.prev = self.current
        self.current = self.current.next
        if self.current is None:
            raise StopIteration
        else:
            return self.current.item


    def get_current_node(self):
        """ returns the current item's node """
        return self.current
    
    def get_prev_node(self):
        """ returns the previous' item's node """
        return self.prev

    def change_next(self, node1 :node.Node, node2: node.Node):
        """ changes one node's next to point to another """
        node1.next = node2

    

        



