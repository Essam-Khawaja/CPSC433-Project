"""Gives us the neighbourhood of candidate slots for the move and swap extension rules"""
from core.assignment import Assignment
from .extension_rule import Move, Swap

class NeighbourhoodGenerator:
    def __init__(self, problem) -> None:
        self.problem = problem

    # Yield one candidate rule at a time for a complete, valid assignment.
    # Yielding allows us to iterate without having to store anything, since we do not exactly know how many slots there migth be
    def candidateRules(self, current: Assignment):
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
            for j in range (i+1, len(components)):
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
