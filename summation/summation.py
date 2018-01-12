"""Expose the calculate_combinations function
which takes an input list and a target sum to evaluate each node.

The TreeNode class is used by the TreeBuilder class to build up a
binary tree, which can then be searhed for any nodes which sum up
to the given target.

Multiple example function calls are provided for standard usage.

It is assumed that in the input list is actually a list or 0 or more
integers and that the sum is also an integer.
"""


class TreeNode(object):
    """Build tree nodes according to a template."""
    def __init__(self, knapsack):
        self._used_keys = knapsack[0]
        self._used_vals = knapsack[1]
        self._unused_keys = knapsack[2]
        self._unused_vals = knapsack[3]
        self._left_child = None
        self._right_child = None

    def __str__(self):
        """Override the string output for object.
        Show the keys for the list items instead of values."""
        return str(self._used_keys)

    def set_left_child(self, node):
        self._left_child = node

    def set_right_child(self, node):
        self._right_child = node

    def get_left_child(self):
        return self._left_child

    def get_right_child(self):
        return self._right_child

    def get_used_keys(self):
        """Return the keys for the knapsack contents,
        if values meet eval criteria."""
        return self._used_keys

    def get_used_vals(self):
        """Return the values for the knapsack contents,
        to check eval criteria."""
        return self._used_vals

    def get_unused_keys(self):
        return self._unused_keys
        
    def get_unused_vals(self):
        return self._unused_vals


class TreeBuilder(object):
    """Build the tree for inputs using TreeNode class."""
    def __init__(self):
        self.tree = None
        self.matches = [] 
        self.eval_val = None

    def add_child_nodes(self, root):
        """Recursively build the tree."""
        # once no additional items are available to add to knapsack,
        # we have reached the leaf node and stop recurssion
        if len(root.get_unused_keys())==0:
            return root

        # left child takes the next item and puts it in the knapsack
        left_used_keys = root.get_used_keys() + root.get_unused_keys()[:1]
        left_used_vals = root.get_used_vals() + root.get_unused_vals()[:1]

        # right discards the next item instead.
        # explicitly setting used keys/vals for illustration
        right_used_keys = root.get_used_keys()
        right_used_vals = root.get_used_vals()

        # both left and right end up with one less item remaining.
        unused_keys = root.get_unused_keys()[1:]
        unused_vals = root.get_unused_vals()[1:]

        knapsack = (left_used_keys, left_used_vals, unused_keys, unused_vals)
        left_node = TreeNode(knapsack)
        left_rec_node = self.add_child_nodes(left_node)
        root.set_left_child(left_rec_node)

        # as a small optimization, once there is only one item left
        # we can skip the right leaf node, since items _in_ the 
        # knapsack are a duplicate of the root node.
        if len(root.get_unused_keys())>1:
            knapsack = (right_used_keys, right_used_vals, unused_keys, unused_vals)
            right_node = TreeNode(knapsack)
            right_rec_node = self.add_child_nodes(right_node)
            root.set_right_child(right_rec_node)
            
        return root

    def build_tree(self, input_list):
        """Create root node and initialize
        recursive tree population given the input list."""
        knapsack = ([], [], list(range(len(input_list))), input_list)
        root_node = TreeNode(knapsack)

        # build the full tree use left first depth first
        self.tree = self.add_child_nodes(root_node)

        # return the tree into local scope for optional fun
        return self.tree

    def scan_tree(self, node):
        """Traverse the tree, populate matches during ascension"""
        if node.get_left_child() is not None:
            self.scan_tree(node.get_left_child())
        if node.get_right_child() is not None:
            self.scan_tree(node.get_right_child())
        if sum(node.get_used_vals())==self.eval_val:
            # exclude duplicates that can be generated by right child
            if node.get_used_keys() not in self.matches \
                and len(node.get_used_keys())>0:
                self.matches.append(node.get_used_keys())

    def get_matches(self, eval_val):
        """Validate match parameters, kick off recursive scan,
        and return matches"""
        # validate eval_val is set, or raise an error
        if self.tree is None:
            raise ValueError\
                ('You must first build a tree before you search it.')

        # ensure instance variables are set
        self.eval_val = eval_val

        # populte matches via recursive tree traversal
        self.scan_tree(self.tree)

        # return the instance variable
        return self.matches

def calculate_combinations(input, target_sum):
    """Use the TreeBuilder class to populate and search a tree"""

    tree_builder = TreeBuilder()
    # This will raise a ValueError if the tree is not built now
    _ = tree_builder.build_tree(input)
    tree_builder.get_matches(target_sum)
    matches = tree_builder.matches
    return matches    

if __name__ == '__main__':
    """Run inline"""

    total_combinations = None

    print("Here are some preloaded examples:\n\n")

    # expose calculate combinations implementation
    # example 1
    print("example 1: {}".format('calculate_combinations([5,5,15,10], 15)'))
    total_combinations = calculate_combinations([5,5,15,10], 15)
    print(total_combinations, '\n')

    # example 2
    print("example 2: {}".format('calculate_combinations([1,2,3,4], 6)'))
    total_combinations = calculate_combinations([1,2,3,4], 6)
    print(total_combinations, '\n')

    # an example with just 1 distinct result which returned a dupe
    print("new example: calculate_combinations({})".format('[1,2,3,4], 2'))
    total_combinations = calculate_combinations([1,2,3,4], 2)
    print(total_combinations, '\n')


    # an example demonstrating negative numbers and zeros
    print("new example: calculate_combinations({})".format('[11,-1,-1,10,0,2], 10'))
    total_combinations = calculate_combinations([11,-1,-1,10,0,2], 10)
    print(total_combinations, '\n')
    
    # an example that sums to a negative int
    print("new example: calculate_combinations({})".format('[1,-2,-2,3], -4'))
    total_combinations = calculate_combinations([1,-2,-2,3], -4)
    print(total_combinations, '\n')
    
    # an example that sums to zero 
    print("new example: calculate_combinations({})".format('[1,-2,-2,2], 0'))
    total_combinations = calculate_combinations([1,-2,-2,2], 0)
    print(total_combinations, '\n')

