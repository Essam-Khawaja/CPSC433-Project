"""Hard-constraint checks: canAssign, legalSlots, and isValid."""
from core.assignment import Assignment

class ConstraintChecker:
    def __init__(self, prob):
        self.prob = prob

    def canAssign(self, component, slot, assignment):
        # If component in placements already
        if component in assignment.placements:
            return False

        # If slot is not in domain
        if slot not in self.prob.domain(component):
            return False

        # If slot has exceeded slot capacity
        if assignment.counts.get(slot, 0) + 1 > slot.max_capacity:
            return False

        # If component needs active learning, check if it has capacity still
        if component.al_required:
            if assignment.al_counts.get(slot, 0) + 1 > slot.al_max_capacity:
                return False

        for otherComp in self.prob.conflicts[component]:
            if otherComp in assignment.placements:
                otherSlot = assignment.placements[otherComp]

                if slot.overlaps(otherSlot):
                    return False

        return True

    def legalSlots(self, component, assignment):
        # Start with an empty list.
        final_slots = []

        # Visit each slot in the component's domain.
        for slot in self.prob.domain(component):
            # Check if we can assign the component in a slot.
            if self.canAssign(component, slot, assignment):
                # If yes, add that slot.
                final_slots.append(slot)

        # Return the collected slots after the loop finishes.
        return final_slots


    def isConsistent(self, assignment):
        temp = Assignment()

        for component, slot in assignment.placements.items():
            if component not in self.prob.components:
                return False

            if not self.canAssign(component, slot, temp):
                return False

            temp.add(component, slot)

        return True

    def isValid(self, assignment):
        '''
        First check: is the timetable complete?
        assignments.placements is a dictionary mapping components to slots. Iterating over a dictionary gives its keys, so this produces the set of assigned components.
        self.prob.components contains every component that needs scheduling.

        Second check: are the placements consistent?
        This checks whether the placements violate any hard mistakes.
        '''
        return set(assignment.placements) == set(self.prob.components) and self.isConsistent(assignment)
