"""Pipeline entry point: parse input, run OR-tree search, hill climb, write output."""
from proj.src.model.problem_instance import ProblemInst

from model.parser import readInput

def main():
    data = readInput('./inputs/input.txt')

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


    print(data)

if __name__ == "__main__":
    main()
