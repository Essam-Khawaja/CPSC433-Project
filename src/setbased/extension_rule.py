"""ExtensionRule, Move, and Swap representations."""

# PSEUDOCODE ONLY. See the final proposal PDF, Section 5, for the search model.
# A complete Assignment represents the set of Assigned(component, slot) facts.
# Rules produce new assignments; they never mutate the current assignment.
# The hill climber pays one step per attempted rule, not this method.
#
# CLASS ExtensionRule
#
#     METHOD replacements(current)
#         abstract: return a mapping of changed component -> destination slot
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
# CLASS Swap EXTENDS ExtensionRule
#
#     CONSTRUCTOR(a, b)
#         store the two distinct components a and b
#
#     METHOD replacements(current)
#         return {
#             a: current.placements[b],
#             b: current.placements[a]
#         }
