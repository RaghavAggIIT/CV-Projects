from avl import AVLTree
from object import Object
from exceptions import NoBinFoundException

class Bin: 
    def __init__(self, bin_id, capacity=0):
        self.bin_id = bin_id
        self.capacity = capacity
        self.id_tree = AVLTree(self.object_comparator) 

    def object_comparator(self, node1, node2):
        if node1.element.object_id > node2.element.object_id:
            return 1
        elif node1.element.object_id < node2.element.object_id:
            return -1
        else:
            return 0

    def add_object(self, obj):
        """Add an object to the bin and reduce capacity."""
        if obj.size > self.capacity:
            raise NoBinFoundException()
        self.id_tree.insert(obj)
        self.capacity -= obj.size
        obj.bin_id = self.bin_id

    def remove_object(self, object_id):
        """Remove an object from the bin and increase capacity."""
        obj_to_remove = self.id_tree.find(Object(object_id, 0, None))
        if obj_to_remove is None:
            return None
        self.id_tree.delete(obj_to_remove)
        self.capacity += obj_to_remove.size

    def objects_inorder(self):
        res=[]
        for i in self.id_tree.inorder_list():
            res.append(i.object_id)
        return res
