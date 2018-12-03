class TreeNode:

    def __init__(self, parent=None, answer_list=[], children=[], decision=None, tree_branch=None, split_title=None, split_index=None):
        self.parent = parent
        self.answers = answer_list
        self.children = children
        self.decision = decision
        self.tree_branch = tree_branch
        self.split_title = split_title
        self.split_index = split_index

    def set_answers(self, answer_list):
        self.answers = answer_list

    def add_child(self, child):
        self.children.append(child)

    def find_child(self, answer):
        for child in self.children:
            if child[1] == answer:
                return child
