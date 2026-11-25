"""OR-tree search result."""

class OrResult:
    def __init__(self, outcome, assignment) -> None:
        self.outcome = outcome
        if outcome == "SUCCESS":
            self.assignment = assignment
        else:
            # Keep assignment as None for failure and timeout makes sense
            self.assignment = None
