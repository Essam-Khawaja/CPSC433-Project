"""
Problem instance, component domains, conflict graph, and lookups.
"""


class ProblemInst:
    def __init__(self, name, lectures, tutorials, lec_slots, tut_slots, not_compatible, unwanted, preferences, pairs, partial_assignments):
        # Raw data from the parser
        self.name = name
        self.lectures = lectures
        self.tutorials = tutorials
        self.lec_slots = lec_slots
        self.tut_slots = tut_slots
        self.not_compatible = not_compatible   # list of (comp, comp)
        self.unwanted = unwanted               # list of (comp, slot)
        self.partial = partial_assignments     # list of (comp, slot)
        self.preferences = preferences         # list of (comp, slot, value)
        self.pairs = pairs                     # list of (comp, comp)

        # Built below
        self.domains = {}     # component -> list of slots it is allowed in
        self.conflicts = {}   # component -> set of components it can't overlap

        # Order matters: conflicts need the tutorial links
        self.linkTutorials()
        self.buildConflicts()
        self.buildDomains()

        # Last, so anything added during setup is included
        self.components = self.lectures + self.tutorials

    def domain(self, comp):
        return self.domains[comp]

    def linkTutorials(self):
        # Links the lectures and tutorials together
        for tutorial in self.tutorials:
            for lecture in self.lectures:
                # Must be the same course
                if lecture.program != tutorial.program:
                    continue
                if lecture.number != tutorial.number:
                    continue

                # If the tutorial names a section, it must match
                if tutorial.lec_section is not None:
                    if lecture.section != tutorial.lec_section:
                        continue

                tutorial.lectures.append(lecture)
                lecture.tutorials.append(tutorial)

            if len(tutorial.lectures) == 0:
                print(f"Warning: no lecture found for {tutorial}")

    def addConflict(self, a, b):
        if a is b:
            return
        self.conflicts[a].add(b)
        self.conflicts[b].add(a)

    def buildConflicts(self):
        """
        Mapping conflict with the constraints and shi:
            C6: A tutorial can't overlap it's own lecture
            C7: Not compatible classes (make sure they don't overlap)
            C11: No 500-level courses overlapping each other
        """

        # Everyone starts with no conflicts
        for comp in self.lectures + self.tutorials:
            self.conflicts[comp] = set()

        # C7: not compatible lines from the file
        for a, b in self.not_compatible:
            self.addConflict(a, b)

        # C6: a tutorial can't overlap its own lecture(s)
        for tutorial in self.tutorials:
            for lecture in tutorial.lectures:
                self.addConflict(tutorial, lecture)

        # C11: 500-level lectures can't overlap each other
        fiveHundreds = []
        for lecture in self.lectures:
            if 500 <= lecture.number <= 599:
                fiveHundreds.append(lecture)

        for i in range(len(fiveHundreds)):
            for j in range(i + 1, len(fiveHundreds)):
                self.addConflict(fiveHundreds[i], fiveHundreds[j])

    def buildDomains(self):
        """
        The domain considers a lot of other hard constraints:
            C5: AL class shouldn't go into a class with al = 0
            C8: Partially assigned goes into its own slot
            C9: Class cannot go into unwanted slots
            C10: Evening classes must start at or after 6pm
            C12: No lectures at Tue/Thurs at 11am cause of the dept meetings
        """
        # Turn the unwanted list into: component -> set of slots
        unwantedMap = {}
        for comp, slot in self.unwanted:
            if comp not in unwantedMap:
                unwantedMap[comp] = set()
            unwantedMap[comp].add(slot)

        # Turn the partial list into: component -> slot
        # Two different fixed slots for one component is impossible
        partialMap = {}
        impossible = set()
        for comp, slot in self.partial:
            if comp in partialMap and partialMap[comp] is not slot:
                impossible.add(comp)
            partialMap[comp] = slot

        for comp in self.lectures + self.tutorials:
            # Lectures only use lecture slots, tutorials only use tutorial slots
            if comp.is_lecture():
                candidates = self.lec_slots
            else:
                candidates = self.tut_slots

            # Keep only the slots that pass every check
            allowed = []
            for slot in candidates:
                if self.isAllowed(comp, slot, unwantedMap):
                    allowed.append(slot)

            # C8: partial assignment shrinks the domain to one slot (or none)
            if comp in impossible:
                domain = []
            elif comp in partialMap:
                fixedSlot = partialMap[comp]
                if fixedSlot in allowed:
                    domain = [fixedSlot]
                else:
                    domain = []
            else:
                domain = allowed

            self.domains[comp] = domain

    def isAllowed(self, comp, slot, unwantedMap):
        # C9: unwanted
        if comp in unwantedMap and slot in unwantedMap[comp]:
            return False

        # C5: active-learning class needs a slot that allows AL
        if comp.al_required and slot.al_max_capacity == 0:
            return False

        # C10: evening classes start at 18:00 or later
        if comp.is_evening and slot.start < 18 * 60:
            return False

        # C12: no lectures on Tue/Thu at 11:00 (department meeting)
        if comp.is_lecture() and slot.day == "TU" and slot.start == 11 * 60:
            return False

        return True
