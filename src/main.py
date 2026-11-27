"""Run OR-tree feasibility search followed by set-based improvement."""

# Needed to read arguments through the command line interface
from model.components import Component
import sys

# All of our lovely classes
from core.constraint_checker import ConstraintChecker
from core.evaluator import Evaluator
from core.step_budget import StepBudget
from model.parser import readInput
from model.problem_instance import ProblemInst
from ortree.or_tree_search import ORTreeSearch
from setbased.hill_climber import SetBasedHillClimb

# Just a nice helper class; returns the number if it is positive otherwise gives out an error
def nonnegativeInteger(name, value) -> int:
    try:
        number = int(value)
    except ValueError as error:
        raise ValueError(f"{name} must be an integer, got '{value}'") from error

    if number < 0:
        raise ValueError(f"{name} must be nonnegative")

    return number

# Check if the argument is cool and in format 😎
def checkArgs(arguments) -> dict:
    if len(arguments) != 9:
        raise ValueError("Expected an input filename and eight numeric arguments")

    numericNames = (
        "wMinFilled",
        "wPref",
        "wPair",
        "wSecDiff",
        "penLectureMin",
        "penTutorialMin",
        "penNotPaired",
        "penSection",
    )

    args = {"inputPath": arguments[0]}

    # The zip function allows us to create a 2D array fast and then iterate over it.
    # Essentially, this would create [[numericNames[0], arguments[0]], ...], and we can iterate over that
    for name, value in zip(numericNames, arguments[1:]):
        args[name] = nonnegativeInteger(name, value)

    return args

def readProblem(inputPath) -> ProblemInst:
    data = readInput(inputPath)

    return ProblemInst(
        name=data["name"],
        lectures=data["lectures"],
        tutorials=data["tutorials"],
        lec_slots=data["lecture slots"],
        tut_slots=data["tutorial slots"],
        not_compatible=data["not compatible"],
        unwanted=data["unwanted"],
        preferences=data["preferences"],
        pairs=data["pair"],
        partial_assignments=data["partial assignments"],
    )

# Temp print function for debug
def printTimetable(assignment, score) -> None:
    print(f"Eval-value: {score}")

    # TODO: It does not identify component's type here; tried explicitly stating it (check following line), but it still is underlined. Code does run so idk js check it out
    # component: Component
    for component in sorted(assignment.placements, key=str):
        slot = assignment.placements[component]
        print(f"{component.id} : {slot.day}, {slot.start_time}")

# Will comment this out later, literally at work rn and my break's about to end lmao so yeah I'll explain it some other time
def main():
    try:
        args = checkArgs(sys.argv[1:])
    except ValueError as error:
        print(f"Argument error: {error}", file=sys.stderr)
        print("Usage: python3 src/main.py inputPath wMinFilled wPref wPair wSecDiff penLectureMin penTutorialMin penNotPaired penSection", file=sys.stderr)
        return 2

    try:
        problem = readProblem(args["inputPath"])
    except (OSError, ValueError) as error:
        print(f"Input error: {error}", file=sys.stderr)
        return 2

    checker = ConstraintChecker(problem)
    evaluator = Evaluator(
        problem=problem,
        w_minfilled=args["wMinFilled"],
        w_pref=args["wPref"],
        w_pair=args["wPair"],
        w_secdiff=args["wSecDiff"],
        pen_lecturemin=args["penLectureMin"],
        pen_tutorialmin=args["penTutorialMin"],
        pen_notpaired=args["penNotPaired"],
        pen_section=args["penSection"],
    )
    budget = StepBudget(100000)

    orSearch = ORTreeSearch(problem, checker, budget)
    orResult = orSearch.search()

    if orResult.outcome == "TIMEOUT":
        print(
            "Step budget exhausted before finding a valid timetable.",
            file=sys.stderr,
        )
        return 1

    if orResult.outcome == "FAILURE":
        print("No feasible timetable exists.", file=sys.stderr)
        return 1

    hillClimber = SetBasedHillClimb(problem, checker, evaluator, budget)
    finalResult = hillClimber.search(orResult.assignment)

    if finalResult.outcome == "TIMEOUT":
        print(
            "Step budget exhausted; returning the best timetable found.",
            file=sys.stderr,
        )

    printTimetable(finalResult.assignment, finalResult.score)
    return 0


if __name__ == "__main__":
    sys.exit(main())
