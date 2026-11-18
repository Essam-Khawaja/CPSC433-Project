"""Set-based search result."""

# PSEUDOCODE ONLY.
#
# CLASS SetResult
#
#     CONSTRUCTOR(outcome, assignment, score)
#         REQUIRE outcome is one of:
#             "ZERO_PENALTY"  - a valid assignment with globally minimal score 0
#             "LOCAL_OPTIMUM" - a full scan found no improving move or swap
#             "TIMEOUT"       - the budget expired before proving a stopping point
#
#         self.outcome <- outcome
#         self.assignment <- assignment
#         self.score <- score
#
# Unlike an unsuccessful OR-tree result, TIMEOUT here retains an assignment.
# All outcomes contain a complete valid timetable and its soft-constraint score.

from proj.src.core.assignment import Assignment
class SetResult:
    def __init__(self, outcome: str, assignment: Assignment, score: int) -> None:
        if outcome not in ("ZERO_PENALTY", "LOCAL_OPTIMUM", "TIMEOUT"):
            raise ValueError(f"Invalid set-based search outcome: {outcome}")
        self.outcome = outcome
        self.assignment = assignment
        self.score = score
