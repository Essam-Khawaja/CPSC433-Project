"""Hill-climbing search for lower-penalty timetables."""

# PSEUDOCODE ONLY. Best-improvement control from the final proposal PDF, Section 5.
# Input is the successful OR-tree assignment, not an empty assignment.
# Reuse the OR-tree StepBudget for a shared work limit, not an elapsed-time limit.
#
# CLASS SetBasedHillClimb
#
#     CONSTRUCTOR(problem, checker, evaluator, budget)
#         store problem, checker, evaluator, and budget
#         neighbourhood <- new NeighbourhoodGenerator(problem)
#
#     METHOD search(initial_assignment)
#         IF NOT checker.isValid(initial_assignment)
#             raise error: hill climbing requires a complete valid timetable
#
#         current <- initial_assignment.copy()
#         current_score <- evaluator.eval(current)
#
#         LOOP
#             IF current_score = 0
#                 return SetResult("ZERO_PENALTY", current, current_score)
#
#             best <- current
#             best_score <- current_score
#             scan_complete <- TRUE
#
#             FOR rule IN neighbourhood.candidateRules(current)
#                 IF budget.expired()
#                     scan_complete <- FALSE
#                     break
#
#                 budget.consume()
#                 candidate <- rule.apply(current, problem, checker)
#                 IF candidate is NONE
#                     continue
#
#                 # The last available step still pays for a full evaluation.
#                 # Do not check expired() again between consume() and scoring.
#                 candidate_score <- evaluator.eval(candidate)
#
#                 # Strict comparison keeps the first rule among equal scores.
#                 IF candidate_score < best_score
#                     best <- candidate
#                     best_score <- candidate_score
#
#                 # Penalties are nonnegative, so nothing can beat zero.
#                 IF best_score = 0
#                     return SetResult("ZERO_PENALTY", best, best_score)
#
#             # Preserve improvements found even if the scan was interrupted.
#             improved <- best_score < current_score
#             current <- best
#             current_score <- best_score
#
#             IF NOT scan_complete
#                 return SetResult("LIMIT_REACHED", current, current_score)
#
#             IF NOT improved
#                 return SetResult("LOCAL_OPTIMUM", current, current_score)
#
#             # Otherwise repeat with the strictly better complete assignment.
#
# No equal-score or worsening transitions are accepted, preventing cycles.
# A local optimum is not necessarily globally optimal. An interrupted scan does
# not prove local optimality, but still returns a valid score no worse than input.
# If the final step completes a full scan with no improvement, report LOCAL_OPTIMUM
# even though the budget is now exhausted. Only an interrupted scan is LIMIT_REACHED.

from src.core.assignment import Assignment
from .neighbourhood import NeighbourhoodGenerator
from .set_result import SetResult


class SetBasedHillClimb:
    def __init__(self, problem, checker, evaluator, budget)-> None:
        self.problem = problem
        self.checker = checker
        self.evaluator = evaluator
        self.budget = budget
        self.neighbourhood = NeighbourhoodGenerator(problem)


    def search(self, initialAssignment: Assignment) -> SetResult:
        if not self.checker.isValid(initialAssignment):
            raise ValueError("hill climbing requires a complete valid time table")

        current = initialAssignment.copy()
        currentScore = self.evaluator.eval(current)

        while True:
            if currentScore == 0:
                return SetResult("ZERO_PENALTY",current, currentScore)

            best = current
            bestScore = currentScore
            scanComplete = True

            for rule in self.neighbourhood.candidateRules(current):
                if self.budget.expired():
                    scanComplete = False
                    break

                self.budget.consume()
                candidate = rule.apply(current, self.problem, self.checker)
                if candidate is None:
                    continue

                #the last available step still pays for a full evaluation
                candidateScore = self.evaluator.eval(candidate)

                if candidateScore < bestScore:
                    best = candidate
                    bestScore = candidateScore

                if bestScore == 0:
                    return SetResult("ZERO_PENALTY", best, bestScore)

            #preserve improvements found even if the scan was interrupted
            improved = bestScore < currentScore
            current = best
            currentScore = bestScore

            if not scanComplete:
                return SetResult("TIMEOUT", current, currentScore)

            if not improved:
                return SetResult("LOCAL_OPTIMUM", current, currentScore)
