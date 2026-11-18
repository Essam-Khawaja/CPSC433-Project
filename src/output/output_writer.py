"""Write the final timetable and evaluation results."""

# As output from your system, I expect an assignment presented in the following form
# and the Eval-value that your system assigns to the assignment. There are several
# ways how we could output an assignment, but I prefer it ordered by lectures. This
# means that we order the lectures alphabetically. After each lecture, the tutorials for
# the lecture (also alphabetically). At the end of each lecture or tutorial, output the
# assigned slot using the assigned days and times that identified it in the input file.
# Here is an example (that is not the solution to the above input example, please
# create your own test examples for the system functionality):
# Eval-value: 30
# CPSC 231 LEC 01 : MO, 10:00
# CPSC 231 LEC 01 TUT 01 : TU, 10:00
# CPSC 231 LEC 02 : MO, 14:00
# CPSC 231 LEC 02 TUT 02 : MO, 8:00
# SENG 300 LEC 01 : TU, 9:30
# SENG 300 TUT 01 : MO, 8:00
# DATA 201 LEC 01 : MO, 8:00
# DATA 201 LEC 01 LAB 01 : FR, 10:00

class OutputWriter:
    def __init__(self):
        print("Output")
