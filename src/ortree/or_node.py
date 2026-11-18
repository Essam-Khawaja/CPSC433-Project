"""OR-tree search node."""
from core.assignment import Assignment

class OrNode:
    # Constructor stores the assignment and set by reference.
    def __init__(self, assignment: Assignment, unassigned: set):
        self.assignment = assignment
        self.unassigned = unassigned
        self.children = []
        self.status = "?"
