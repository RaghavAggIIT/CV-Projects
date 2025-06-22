from bin import Bin
from avl import AVLTree
from object import *
from exceptions import NoBinFoundException
 
class GCMS:
    def __init__(self):
        self.capacity_tree = AVLTree(self.capacity_compare) # bins by capacity
        self.bins_id = AVLTree(self.bin_id_compare) # bins by ID
        self.id_tree = AVLTree(self.object_comparator) # objects tree

    def capacity_compare(self, node1, node2):
        bin1 = node1.element
        bin2 = node2.element
        if bin1.capacity > bin2.capacity:
            return 1
        elif bin1.capacity < bin2.capacity:
            return -1
        else:
            if bin1.bin_id > bin2.bin_id:
                return 1    
            elif bin1.bin_id < bin2.bin_id:
                return -1
            else:
                return 0

    def bin_id_compare(self, node1, node2):
        bin1 = node1.element
        bin2 = node2.element
        if bin1.bin_id > bin2.bin_id:
            return 1
        elif bin1.bin_id < bin2.bin_id:
            return -1
        else:
            return 0

    def object_comparator(self, node1, node2):
        if node1.element.object_id > node2.element.object_id:
            return 1
        elif node1.element.object_id < node2.element.object_id:
            return -1
        else:
            return 0

    def add_bin(self, bin_id, capacity):
        new_bin = Bin(bin_id, capacity)
        self.insert_update(new_bin)

    def add_object(self, object_id, size, color):
        new_object = Object(object_id, size, color)
        my_bin = self.find_bin(new_object)
        if my_bin is None:
            raise NoBinFoundException()
        self.delete_update(my_bin)
        my_bin.add_object(new_object)
        self.id_tree.insert(new_object)
        self.insert_update(my_bin)

    def delete_update(self, my_bin):
        self.capacity_tree.delete(my_bin)
        self.bins_id.delete(my_bin)

    def insert_update(self, my_bin):
        self.capacity_tree.insert(my_bin)
        self.bins_id.insert(my_bin)

    def delete_object(self, object_id):
        obj = self.id_tree.find(Object(object_id))
        if obj is None:
            return None
        obj_bin = self.bins_id.find(Bin(obj.bin_id))
        if obj_bin is None:
            return None

        self.id_tree.delete(obj)
        self.delete_update(obj_bin)
        obj_bin.remove_object(object_id)
        self.insert_update(obj_bin)

    def object_info(self, object_id):
        obj = self.id_tree.find(Object(object_id))
        if obj is None:
            return None
        return obj.bin_id

    def bin_info(self, bin_id):
        new_bin = Bin(bin_id)
        bin = self.bins_id.find(new_bin)
        if bin is None:
            return None
        return bin.capacity,bin.objects_inorder()

    def yellow_cargo(self, obj):
        size = obj.size
        my_bin = None
        current = self.capacity_tree.root
        while current is not None:
            if current.element.capacity >= size:
                my_bin = current.element
                current = current.left
            else:
                current = current.right
        if my_bin is None:
            return None

        cap = my_bin.capacity
        current = self.capacity_tree.root
        while current is not None:
            if current.element.capacity == cap:
                my_bin = current.element
                current = current.right
            elif current.element.capacity > cap:
                current = current.left
            else:
                current = current.right
        return my_bin

    def blue_cargo(self, obj):
        size = obj.size
        my_bin = None
        current = self.capacity_tree.root
        while current is not None:
            if current.element.capacity >= size:
                my_bin = current.element
                current = current.left
            else:
                current = current.right
        
        if my_bin is None:
            return None
        cap = my_bin.capacity
        current = self.capacity_tree.root
        while current is not None:
            if current.element.capacity == cap:
                my_bin = current.element
                current = current.left
            elif current.element.capacity > cap:
                current = current.left
            else:
                current = current.right
        return my_bin

    def red_cargo(self, obj):
        size = obj.size
        my_bin = None
        current = self.capacity_tree.root
        while current.right is not None:
            current = current.right
        if current.element.capacity >= size:
            my_bin = current.element
        if my_bin is None:
            return None

        cap = my_bin.capacity
        current = self.capacity_tree.root
        while current is not None:
            if current.element.capacity == cap:
                my_bin = current.element
                current = current.left
            elif current.element.capacity < cap:
                current = current.right
            else:
                current = current.left
        return my_bin

    def green_cargo(self, obj):
        size = obj.size
        my_bin = None
        current = self.capacity_tree.root
        while current.right is not None:
            current = current.right
        if current.element.capacity >= size:
            my_bin = current.element
        
        if my_bin is None:
            return None
        cap = my_bin.capacity
        current = self.capacity_tree.root
        while current is not None:
            if current.element.capacity == cap:
                my_bin = current.element
                current = current.right
            elif current.element.capacity < cap:
                current = current.right
            else:
                current = current.left
        return my_bin

    def find_bin(self, new_object):
        my_bin = None
        color = new_object.color
        if color == Color.RED:
            my_bin=self.red_cargo(new_object)
        elif color == Color.YELLOW:
            my_bin=self.yellow_cargo(new_object)
        elif color == Color.GREEN:
            my_bin=self.green_cargo(new_object)
        elif color == Color.BLUE:
            my_bin=self.blue_cargo(new_object)
        return my_bin
