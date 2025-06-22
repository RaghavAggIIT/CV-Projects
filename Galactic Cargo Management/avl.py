from node import Node

class AVLTree: 
    def __init__(self, comparator):
        self.root = None
        self.size = 0
        self.compare_function = comparator

    def compare_nodes(self, node1, node2):
        """Compare two nodes using the provided comparison function."""
        return self.compare_function(node1, node2)

    def insert(self, element):
        self.root = self.insert_iterative(self.root, element)
        self.size += 1

    def insert_iterative(self, root, element):
        if root is None:
            return Node(element)
        current = root
        parent_stack = []
        new_node = Node(element)
        while current is not None:
            parent_stack.append(current)
            comparison = self.compare_nodes(new_node, current)
            if comparison < 0:
                current = current.left
            else:
                current = current.right
        parent = parent_stack[-1]
        if self.compare_nodes(new_node, parent) < 0:
            parent.left = new_node
        else:
            parent.right = new_node
        while parent_stack:
            current = parent_stack.pop()
            current = self._balance(current)
            if parent_stack:
                parent = parent_stack[-1]
                if self.compare_nodes(current, parent) < 0:
                    parent.left = current
                else:
                    parent.right = current
            else:
                root = current
        return root

    def delete(self, element):
        self.root = self.delete_iterative(self.root, element)
        if self.root is not None:
            self.size -= 1

    def delete_iterative(self, root, element):
        if root is None:
            return root
        current = root
        parent_stack = []
        node_to_delete = None
        while current is not None:
            comparison = self.compare_nodes(Node(element), current)
            parent_stack.append(current)
            if comparison < 0:
                current = current.left
            elif comparison > 0:
                current = current.right
            else:
                node_to_delete = current
                break
        if node_to_delete is None:
            return root
        if not node_to_delete.left or not node_to_delete.right:
            replacement = node_to_delete.left if node_to_delete.left else node_to_delete.right
            if parent_stack:
                parent_stack.pop()
                if parent_stack:
                    parent = parent_stack[-1]
                    if parent.left == node_to_delete:
                        parent.left = replacement
                    else:
                        parent.right = replacement
                else:
                    root = replacement
        else:
            successor = node_to_delete.right
            successor_parent = node_to_delete
            while successor.left is not None:
                successor_parent = successor
                successor = successor.left
            node_to_delete.element = successor.element
            if successor_parent.left == successor:
                successor_parent.left = successor.right
            else:
                successor_parent.right = successor.right
        while parent_stack:
            current = parent_stack.pop()
            current = self._balance(current)
            if parent_stack:
                parent = parent_stack[-1]             
                if parent.left == current or self.compare_nodes(current, parent) < 0:
                    parent.left = current
                else:
                    parent.right = current
            else:
                root = current
        return root

    def find(self, element):
        node = Node(element)
        return self._find_recursive(self.root, node)

    def find_for_bin(self, element):
        return self._find_recursive(self.root, element).element

    def _find_recursive(self, node, element):
        if node is None:
            return None           
        comparison = self.compare_nodes(element, node)
        if comparison < 0:
            return self._find_recursive(node.left, element)
        elif comparison > 0:
            return self._find_recursive(node.right, element)
        return node.element

    def _balance(self, current):
        if not current:
            return None
        self.change_height(current)
        balance_factor = self.getbal(current)
        if balance_factor > 1:
            if self.getbal(current.left) < 0:
                current.left = self._left_rotate(current.left)
            return self._right_rotate(current)
        if balance_factor < -1:
            if self.getbal(current.right) > 0:
                current.right = self._right_rotate(current.right)
            return self._left_rotate(current)
        return current

    def _left_rotate(self, node):
        right_child = node.right
        node.right = right_child.left
        right_child.left = node
        self.change_height(node)
        self.change_height(right_child)
        return right_child

    def _right_rotate(self, node):
        left_child = node.left
        node.left = left_child.right
        left_child.right = node
        self.change_height(node)
        self.change_height(left_child)
        return left_child

    def change_height(self, node):
        node.height = 1 + max(self.geth(node.left), self.geth(node.right))

    def geth(self, node):
        return node.height if node else 0

    def getbal(self, node):
        return self.geth(node.left) - self.geth(node.right)

    def leftmost(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def inorder_list(self):
        return self._inorder(self.root)

    def _inorder(self, node):
        if node:
            yield from self._inorder(node.left)
            yield node.element
            yield from self._inorder(node.right)



        

    
