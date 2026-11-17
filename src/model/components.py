"""Component, Lecture, and Tutorial representations."""

class Component:
    def __init__(self, id: str, program: str, number: int, al_required: bool):
        self.id = " ".join(id.split())  # This basically strips all spaces within id, then adds only a single one between each
        self.program = program
        self.number = number
        self.al_required = al_required
        self.is_evening = False

    def is_lecture(self) -> bool:
        raise NotImplementedError

    def is_tutorial(self) -> bool:
        return not self.is_lecture()

    def __repr__(self) -> str:
        return self.id

class Lecture(Component):
    def __init__(self, id: str, program: str, number: int, al_required: bool, section: str):
        super().__init__(id, program, number, al_required)

        self.section = section
        self.tutorials: list[Tutorial] = [] # All tuts it has

        # Hard Constraint 10: All lectures beginning with 9 are evening classes
        self.is_evening = section.startswith("9")

    def is_lecture(self) -> bool:
        return True


class Tutorial(Component):
    def __init__(self, id: str, program: str, number: int, al_required: bool, lec_section: str, tut_number: str):
        super().__init__(id, program, number, al_required)
        self.lec_section = lec_section  # "01", or None if shared by all sections
        self.tut_number = tut_number          # e.g. "01"

        # Only evening if explicitly attached to a LEC 9xx section
        if lec_section is not None:
            self.is_evening = lec_section.startswith("9")

        self.parents: list[Lecture] = []  # parent lectures, filled in by ProblemInstance

    def is_lecture(self) -> bool:
        return False
