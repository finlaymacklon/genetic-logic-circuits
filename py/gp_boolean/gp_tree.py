r"""
Tree class for Genetic Programming of Boolean Expressions
"""

from numpy.random import random
from numpy.random import randint
from copy import deepcopy
from gp_boolean.gp_node import GP_Node, and_gate, or_gate

# TODO if the number correct = 0, then try complementing at the root of the tree

# TODO simplify expressions; e.g. (A ∩ A = A), (A ∪ A = A), (A ∩ A" = 0), (A ∪ A" = 1)
# (encapsulation?)

# TODO simiplify expressions; e.g. (A ∩ B") ∪ (B" ∩ A) = 1

# TODO simplify expressions; pull complements up

# TODO permuation; permute gate type, terminal type, complement

# create binary tree data structure (genetic programs)
class Genetic_Program():
    """
    Data structure for genetic program binary trees
    """

    # define probablity of creating node with NOT gate
    P_COMPLEMENT = 1/3

    def __init__(self, max_depth, functions, terminals, threshold=0.5):
        # create GP using ramped creation method with given threshold
        self.max_depth = max_depth
        self.functions = functions
        self.terminals = terminals
        self.threshold = threshold
        self.root = self.create_gp_ramped(max_depth)

    def add_child(self, parent, d, creation_method):
        """
        parent: parent node
        d: maximum depth
        creation_method: function to use for creating new nodes
        """

        if parent.left is None:
            parent.left = creation_method(d)
        elif parent.right is None:
            parent.right = creation_method(d)

    def create_gp_ramped(self, max_depth):
        """
        max_depth: maximum depth
        """

        # randomly decide to create with grow or full
        if random() < self.threshold:
            return self.create_gp_grow(max_depth)
        else:
            return self.create_gp_full(max_depth)

    def create_gp_full(self, max_depth):
        """
        max_depth: maximum depth
        """

        # randomly determine the complement value (NOT gate)
        if random() < self.P_COMPLEMENT:
            complement = 1
        else:
            complement = 0
        # check if we are adding a terminal (leaf)
        if max_depth > 1:
            # select function type at random
            idx_random = randint(0, len(self.functions))
            fn_type = self.functions[idx_random]
            # create parent node
            node = GP_Node(fn_type, None, complement)
            # add 2 children
            for i in range(2):
                self.add_child(
                    node,
                    max_depth - 1,
                    self.create_gp_full
                )
        # otherwise we have reached a leaf node
        else:
            # select terminal type at random
            idx_random = randint(0, len(self.terminals))
            terminal_type = self.terminals[idx_random]
            # create the leaf
            node = GP_Node(None, terminal_type, complement)
        # return the node
        return node

    def create_gp_grow(self, max_depth):
        """
        max_depth: maximum depth
        """

        # randomly determine the complement value (NOT gate)
        if random() < self.P_COMPLEMENT:
            complement = 1
        else:
            complement = 0
        # check if we are adding a terminal (leaf)
        if max_depth > 1:
            # randomly decide between gate and signal
            if random() < 0.5:
                idx_random = randint(0, len(self.functions))
                fn_type = self.functions[idx_random]
                # create parent node
                node = GP_Node(fn_type, None, complement)
                # add 2 children
                for i in range(2):
                    self.add_child(
                        node,
                        max_depth - 1,
                        self.create_gp_grow
                    )
            else:
                idx_random = randint(0, len(self.terminals))
                terminal = self.terminals[idx_random]
                # create the leaf
                node = GP_Node(None, terminal, complement)
        # otherwise we have reached a leaf-only node
        else:
            # select terminal type at random
            idx_random = randint(0, len(self.terminals))
            terminal_type = self.terminals[idx_random]
            # create the leaf
            node = GP_Node(None, terminal_type, complement)
        # return the node
        return node

    def select_node(self):
        """
        Uniformly select a node from the tree
        """

        # initialize selection as root
        selected = self.root
        # initialize tree depth level as root level
        level = 1
        # initialize flag
        done_selection = False
        while not done_selection:
            node_weight = self.find_node_weight(selected)
            weight = node_weight * random()
            if weight >= (node_weight - 1):
                done_selection = True
            else:
                for child in [selected.left, selected.right]:
                    weight = weight - self.find_node_weight(child)
                    if weight < 0:
                        selected = child
                        level += 1
                        break
        # return the final node selected
        return selected, level

    def find_node_weight(self, node, count=1):
        """
        Count number of children in node
        """

        # count left child
        if node.left is not None:
            count = self.find_node_weight(node.left, count + 1)
        # count right child
        if node.right is not None:
            count = self.find_node_weight(node.right, count + 1)
        # return count
        return count

    def find_subtree_depth(self, node=None, depth=0):
        """
        Determine depth of subtree starting from given node
        """
        
        # check if node is None
        if node is None:
            node = self.root
        # increase depth counter
        depth += 1
        # check if we reached a leaf node
        if node.fn_type is None:
            return depth
        else:
            left_depth = self.find_subtree_depth(node.left, depth)
            right_depth = self.find_subtree_depth(node.right, depth)
            return max(left_depth, right_depth)

    def mutate_gp(self):
        """
        Mutate a genetic program: replace subtree at a node's child
        """

        # check if we have any children
        if (self.root.fn_type is None):
            # just mutate the root
            self.root = self.create_gp_ramped(self.max_depth)
            # return reference to mutated node
            return self.root
        # select an initial node
        node, level = self.select_node()
        # check if this node has children
        while (node.left is None) and (node.right is None):
            # if not, try selecting again
            node, level = self.select_node()
        # determine max level of new mutation
        max_depth = self.max_depth - level
        # randomly choose to mutate the left or right child
        if random() < 0.5:
            # mutate right child
            node.right = self.create_gp_ramped(max_depth)
        else:
            # mutate left child
            node.left = self.create_gp_ramped(max_depth)
        # return reference to mutated node
        return node

    def recombine(self, other):
        """
        Swap subtrees at selected nodes for this GP and another GP
        """

        # check if we have any children
        if (self.root.fn_type is None):
            # cannot recombine, return reference to mutated node
            return self.root
        # select an initial node from self
        node_self, level_self = self.select_node()
        # check if this node has children
        while (node_self.fn_type is None):
            # if not, try selecting again
            node_self, level_self = self.select_node()
        # determine max level of new mutation
        max_depth = self.max_depth - level_self
        # select an initial node from other
        node_other, level_other = other.select_node()
        # check if this node goes deeper than allowed
        while (other.find_subtree_depth(node_other)) > max_depth:
            # if not, try selecting again
            node_other, level_other = other.select_node()
        # randomly choose to replace the left or right child
        if random() < 0.5:
            # recombine right child (don't alter other GP)
            node_self.right = deepcopy(node_other)
        else:
            # recombine left child (don't alter other GP)
            node_self.left = deepcopy(node_other)
        # return reference to changed node
        return node_self

    def permutate_gp(self):
        """
        ...
        """

        return None

    def edit_gp(self):
        """
        ...
        """

        return None

    def encapsulate(self):
        """
        ...
        """

        return None

    def wrap_node(self):
        """
        ...
        """

        return None

    def lift_node(self):
        """
        ...
        """

        return None

    def evaluate(self, inputs, correct_output):
        """
        Evaluate the tree with given inputs
        Return whether or not we got correct
        """

        # evaluate root node (evaluates entire tree)
        output = self.root.evaluate(inputs)
        # return value is added to counter
        return 1 if output == correct_output else 0
    
    def find_size(self, node=None, count=0):
        """
        Go through the tree and determine the number of 
        gates and inputs
        """
        
        # if node is none, start at root
        if node is None:
            node = self.root
        # add this node's complement to count
        if node.complement:
            count += 1
        # if at signal, add NOT gate, self, and return
        if node.fn_type is None:
            return count
        # else keep recursing
        else:
            count += 1
            count = self.find_size(node.left, count)
            count = self.find_size(node.right, count)
        # return count at this node
        return count

    def print_tree(self, node=None):
        """
        Recursively print tree
        """

        # default to printing whole tree
        if node is None:
            node = self.root
        # check if leaf node
        if node.fn_type is not None:
            # open bracket
            print('(', end='')
            # print left side
            self.print_tree(node.left)
            # print gate type
            if node.fn_type is and_gate:
                print(u' \u2229 ', end='')
            elif node.fn_type is or_gate:
                print(u' \u222A ', end='')
            # print right side
            self.print_tree(node.right)
            # close bracket
            print(')', end='')
        else:
            print(node.terminal, end='')
        # show complement if present
        if node.complement:
            print('"', end='')
        # if root end print
        if node is self.root:
            print('', end='\n')