"""Hill-climbing search for lower-penalty timetables."""
from core.evaluator import Evaluator
from core.constraint_checker import ConstraintChecker
from model.problem_instance import ProblemInst

from core.assignment import Assignment
from .neighbourhood import NeighbourhoodGenerator
from .set_result import SetResult


class SetBasedHillClimb:
    def __init__(self, problem: ProblemInst, checker: ConstraintChecker, evaluator: Evaluator, budget)-> None:
        self.problem = problem  # The problem assignment
        self.checker = checker  # The constraint checker
        self.evaluator = evaluator  # The evaluati
        self.budget = budget    # The budget of the problem; how much we want to spend to solve it
        self.neighbourhood = NeighbourhoodGenerator(problem)


    def search(self, initialAssignment: Assignment) -> SetResult:
        if not self.checker.isValid(initialAssignment):
            raise ValueError("hill climbing requires a complete valid time table")
        current = initialAssignment.copy()
        currentScore = self.evaluator.eval(current)

        while True:
            # No need to hill climb if already optimized
            if currentScore == 0:
                return SetResult("ZERO_PENALTY",current, currentScore)

            best = current  # Stores the best assignment we have
            bestScore = currentScore    # Stores the best score we have
            scanComplete = True # For knowing if the loop scan is done

            # Through all the candidates by the neighbourhood
            for rule in self.neighbourhood.candidateRules(current):
                # Check if no more budget
                if self.budget.expired():
                    scanComplete = False
                    break

                # Use some of the budget on this move
                self.budget.consume()
                # Apply the rules from neighbourhood
                candidate = rule.apply(current, self.problem, self.checker)
                if candidate is None:
                    continue

                # the last available step still pays for a full evaluation
                candidateScore = self.evaluator.eval(candidate)

                # Update best score if its less than the current one
                # The best score in this case would be the minimum; that is why we use less than
                if candidateScore < bestScore:
                    best = candidate
                    bestScore = candidateScore

                # Check if optimized completely
                if bestScore == 0:
                    return SetResult("ZERO_PENALTY", best, bestScore)

            # preserve improvements found even if the scan was interrupted
            improved = bestScore < currentScore
            current = best
            currentScore = bestScore

            if not scanComplete:
                return SetResult("TIMEOUT", current, currentScore)

            if not improved:
                return SetResult("LOCAL_OPTIMUM", current, currentScore)
