"""ExtensionRule, Move, and Swap representations."""

class ExtensionRule:
    def apply(self, current, problem, checker):
        # Depending on which object is calling apply, the Move or Swap version of replacements will be called.
        changes = self.replacements(current)
        candidate = current.copy()


class Move(ExtensionRule):
    # Store one component and one destination.
    def __init__(self, component, destination):
        self.component = component  # Which component changes.
        self.destination_slot = destination # Where it should go.

    def replacements(self, current):
        return {self.component: self.destination}

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

# PSEUDOCODE ONLY. See the final proposal PDF, Section 5, for the search model.
# A complete Assignment represents the set of Assigned(component, slot) facts.
# Rules produce new assignments; they never mutate the current assignment.
# The hill climber pays one step per attempted rule, not this method.
#
# CLASS ExtensionRule
#
#
#     METHOD apply(current, problem, checker)
#         REQUIRE current is a complete valid assignment
#         changes <- replacements(current)
#         candidate <- new Assignment()
#
#         # Rebuild counters instead of editing placements in place.
#         # For a swap, BOTH destinations are chosen before checking anything.
#         # No old placement remains to incorrectly block a swapped component.
#         FOR component IN problem.components, in fixed order
#             slot <- changes.get(component, current.placements[component])
#
#             IF NOT checker.canAssign(component, slot, candidate)
#                 return NONE
#
#             candidate.add(component, slot)
#
#         # Every component was added once and passed the hard checks.
#         # Domains also preserve mandatory CPSC 851/913 assessment bookings.
#         return candidate
#
# CLASS Move EXTENDS ExtensionRule
#
#     CONSTRUCTOR(component, destination)
#         store component and destination
#
#     METHOD replacements(current)
#         return {component: destination}
#
