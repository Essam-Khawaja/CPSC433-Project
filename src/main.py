"""Pipeline entry point: parse input, run OR-tree search, hill climb, write output."""
from core.step_budget import StepBudget
from ortree.or_tree_search import ORTreeSearch
from core.constraint_checker import ConstraintChecker
from model.problem_instance import ProblemInst
from core.assignment import Assignment

from model.parser import readInput
import sys

def main():
    # CLI input args
    # TODO: Uncomment
    # input_file_path, w_minfilled, w_pref, w_pair, w_secdiff, pen_lecturemin, pen_tutorialmin, pen_notpaired, pen_section = check_args()

    data = readInput('./inputs/input.txt')
    # TODO: Switch to below for assignment submission
    # data = readInput(input_file_path)

    probInst = ProblemInst(
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

    checker = ConstraintChecker(probInst)
    budget = StepBudget(100000)

    search = ORTreeSearch(probInst, checker, budget)

    result = search.search()

    """
    checker ← new ConstraintChecker(problem)
        budget ← new TimeBudget(60 seconds)
        search ← new ORTreeSearch(problem, checker, budget)

        result ← search.search()

        IF result.outcome = TIMEOUT:
            PRINT "Search timed out"
            RETURN

        IF result.outcome = FAILURE:
            PRINT "No feasible timetable exists"
            RETURN

        initial_assignment ← result.assignment

        // Once hill climbing is implemented, pass initial_assignment to it.
        FOR component IN initial_assignment.placements, sorted by identifier:
            slot ← initial_assignment.placements[component]
            PRINT component.identifier, slot.day, slot.start_time
    """

    def printTimetable(assignment):
        for component in sorted(assignment.placements, key=str):
            slot = assignment.placements[component]
            print(f"{component} : {slot}")

    if result.assignment is None:
        print(f"No timetable found ({result.outcome})")
    else:
        printTimetable(result.assignment)

if __name__ == "__main__":
    main()

def check_args():
    # input command line args
    # program filepath w_minfilled w_pref w_pair w_secdiff pen_lecturemin pen_tutorialmin pen_notpaired pen_section
    # 10 args as
    if(len(sys.argv) != 10):
        print("[ERROR] Not enough arguments!")
        print("python program_path input_file_path w_minfilled w_pref w_pair w_secdiff pen_lecturemin pen_tutorialmin pen_notpaired pen_section")

    # sys.argv[0] is the current program's path
    return sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7], sys.argv[8], sys.argv[9], sys.argv[10]
