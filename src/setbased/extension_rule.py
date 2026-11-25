"""ExtensionRule, Move, and Swap representations."""
from core.assignment import Assignment

class ExtensionRule:
    def apply(self, current, problem, checker):
        # Depending on which object is calling apply, the Move or Swap version of replacements will be called.
        # Assumes current is a complete, valid assignment.
        changes = self.replacements(current)
        candidate = Assignment()

        for component in problem.components:
            # Use the replacement if this component changes.
            # Otherwise, preserve its current slot.
            slot = changes.get(component, current.placements[component])

            if not checker.canAssign(component, slot, candidate):
                return None

            candidate.add(component, slot)

        return candidate

    def replacements(self, current):
        raise NotImplementedError('Move and Swap need to have their own replacement methods defined please :)')


class Move(ExtensionRule):
    # Store one component and one destination.
    def __init__(self, component, destination):
        self.component = component  # Which component changes.
        self.destination_slot = destination # Where it should go.

    def replacements(self, current):
        return {self.component: self.destination_slot}

class Swap(ExtensionRule):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    # Return a dictionary describing proposed changes.
    def replacements(self, current):
        # Create a dictionary DESCRIBING lecture A and lecture B's swapped timeslots.
        changes = {
            self.a: current.placements[self.b],
            self.b: current.placements[self.a]
        }

        return changes
