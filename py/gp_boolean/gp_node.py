"""
Node class for Genetic Programming of Boolean Expressions
"""

# encode don't care
X = 'X'
# create and gate
def and_gate(input_a, input_b):
    if (input_a == X) & (input_b == X):
        return X
    elif (input_a == 0) | (input_b == 0):
        return 0
    elif (input_a == X) | (input_b == X):
        return X
    else:
        return 1
# create or gate
def or_gate(input_a, input_b):
    if (input_a == 1) | (input_b == 1):
        return 1
    elif (input_a == 0) & (input_b == 0):
        return 0
    else:
        return X
# define list of function types
function_types = [and_gate, or_gate]
# create node data structure for tree
class GP_Node():
    """
    Data structure for gp tree nodes
    """

    def __init__(self, fn_type, terminal, complement):
        self.fn_type = fn_type # if interior node
        self.terminal = terminal # if leaf node
        self.complement = complement # for NOT gate
        self.left = None
        self.right = None

    def evaluate(self, inputs):
        if self.fn_type is None:
            # determine which input value to use
            input_val = inputs[self.terminal]
            # check if input_val is don't care
            if input_val == X:
                # return don't care
                return X
            else:
                # return leaf output value
                return (input_val ^ self.complement)
        else:
            # get the value of first child
            left_val = self.left.evaluate(inputs)
            # get value of second child
            right_val = self.right.evaluate(inputs)
            # get value of gate
            gate_val = self.fn_type(left_val, right_val)
            # check if gate_val is don't care
            if gate_val == X:
                # return don't care
                return X
            else:
                # return output value
                return (gate_val ^ self.complement)