"""Set-based search result."""

# PSEUDOCODE ONLY.
#
# CLASS SetResult
#
#     CONSTRUCTOR(outcome, assignment, score)
#         REQUIRE outcome is one of:
#             "ZERO_PENALTY"  - a valid assignment with globally minimal score 0
#             "LOCAL_OPTIMUM" - a full scan found no improving move or swap
#             "LIMIT_REACHED" - the step budget interrupted a neighbourhood scan
#
#         self.outcome <- outcome
#         self.assignment <- assignment
#         self.score <- score
#
# Unlike an unsuccessful OR-tree result, LIMIT_REACHED retains an assignment.
# All outcomes contain a complete valid timetable and its soft-constraint score.
# This is a work limit, not a timeout. The current OR-tree API still uses the
# legacy outcome "TIMEOUT" for step exhaustion; main must interpret each stage.
