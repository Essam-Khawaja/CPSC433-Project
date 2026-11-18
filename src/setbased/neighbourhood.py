
"""Candidate move and swap generation for the legal neighbourhood."""

# PSEUDOCODE ONLY. Yield rules one at a time, not a list of assignments.
# Fixed order: all moves first, then swaps; use problem/domain list order.
# This gives the hill climber deterministic tie-breaking.
# The hill climber consumes a step BEFORE applying each rule and checking its
# legality, so even candidates rejected by hard constraints count toward the limit.
#
# CLASS NeighbourhoodGenerator
#
#     CONSTRUCTOR(problem)
#         store problem
#
#     METHOD candidateRules(current)
#         REQUIRE current is a complete valid assignment
#
#         FOR component IN problem.components
#             old_slot <- current.placements[component]
#
#             FOR destination IN problem.domain(component)
#                 IF destination is old_slot
#                     continue
#
#                 yield new Move(component, destination)
#
#         FOR i FROM 0 TO length(problem.components) - 1
#             FOR j FROM i + 1 TO length(problem.components) - 1
#                 a <- problem.components[i]
#                 b <- problem.components[j]
#                 slot_a <- current.placements[a]
#                 slot_b <- current.placements[b]
#
#                 IF slot_a is slot_b
#                     continue
#
#                 # Also excludes swaps between lecture and tutorial slots.
#                 # Fixed partial assignments remain protected by their domains.
#                 IF slot_b NOT IN problem.domain(a)
#                     continue
#                 IF slot_a NOT IN problem.domain(b)
#                     continue
#
#                 yield new Swap(a, b)
#
# This generator does not consume or check the budget. Exhausting it naturally
# means a complete scan; the hill climber records any budget-interrupted scan.
# A yielded rule is only a candidate. rule.apply rejects hard-constraint violations.

from .extension_rule import Move, Swap

class NeighbourhoodGenerator:
    def __init__(self, problem) -> None:
        self.problem = problem
    # Yield one candidate rule at a time for a complete, valid assignment.
    def candidateRules(self, current):
        components = self.problem.components

        # 1. Moves: try changing one component's slot.
        for component in components:
            old_slot = current.placements[component]

            for destination in self.problem.domain(component):
                if destination is old_slot:
                    continue
                yield Move(component, destination)

        # 2. Swaps: try exchanging the slots of two different components.
        for i in range(len(components)):
            for i in range (i+1, len(components)):
                a = components[i]
                b = components[j]

                slot_a = current.placements[a]
                slot_b = current.placements[b]

                if slot_a is slot_b:
                    continue

                # Each component must be allowed to use the other's slot.
                if slot_b not in self.problem.domain(a):
                    continue

                if slot_a not in self.problem.domain(b):
                    continue

                yield Swap(a, b)
