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
