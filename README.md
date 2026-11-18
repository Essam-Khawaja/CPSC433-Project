# CPSC 433 Project — Course Timetabling via Three Search Paradigms

Group project proposal for CPSC 433 (Artificial Intelligence), University of Calgary, Fall 2026.
It proposes two search systems for the course timetabling problem: OR-tree feasibility followed
by set-based improvement (Proposal A), and OR-tree feasibility followed by AND-tree
branch-and-bound (Proposal B).

## How Things Will Work (By Yours Truly Essam-Kun)

This is me breaking down the problem from our PDF into code ideas. Will not implement on my own cause I do want everyone to work on it, but I am abstracting it beforehand so that we do not waste a lot of time on Tuesday.

### Our basic building blokcs:

1. Parser: Read the file and turn it into our objects:

- Slot Obj
- Lec Obj -> has the lecture number
- Tut Obj
- Note: We need to define the connection between lecture and tutorial as well, idk how but we need to

2. ProblemInstance: Preprocessing the objects. Before we put it to work, we take all the slots, lecs, tuts, and assign stuff to them like their domain and shi

### OR-TREE:

1. Assignment: Add each component to a slot
2. ConstraintChecker: Is slot currently full? Is slot conflicting with another slot that overlaps it. Remember we only have to check for hard constraints here. Return bool
3. ORTreeSearch: Does the search

- Look at every class that is not placed yet; pass it through constraintCheck to see how many it can use
- if any class has zero options, a mistake was made earlier so erase the last placement and try that class's next option (backtracking). Will need to decide how our app 'remembers' these things
- Once all classes are picked, put it into **assign0**

### SET-BASED SEARCH

1. Evaluator: Scores with penalty points. Lowest or 0.
2. Move: Picks one class and puts it in different slot
3. Swap: Trades slots between two classes
4. NeighbourhoodGenerator: List every move and swap possible right now, use the ConstraintChecker from OR-TREE to invalidate the ones that break the hard constraints
5. SetBasedHillClimb:

- pass assign0 to Evaluator -> if 0, stop, otherwise continue
- NeighbourhoodGen: Check all Moves and Swaps
- Score what the timetable will look like after **each** move
- Take the change with the lowest score. If score beats current one, make it and then go back to step 1
- If nothing beats current score, stop

Then, a final writeOutput function should be good enough for the rest of the tingz.
