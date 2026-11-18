"""OR-tree search for a feasible timetable."""

# CLASS ORTreeSearch
#
#     FIELDS
#         problem
#         checker
#         budget
#         root
#
#     CONSTRUCTOR(problem, checker, budget)
#         store the dependencies
#
# Helper A: Choose a component using MRV
# METHOD selectMRV(node)
#
#     best_component ← NONE
#     best_slots ← NONE
#
#     FOR component in problem.components, in its fixed list order
#
#         IF component is not in node.unassigned
#             continue
#
#         slots ← checker.legalSlots(component, node.assignment)
#
#         IF slots is empty
#             return (component, empty list)
#
#         IF best_component is NONE
#            OR length(slots) < length(best_slots)
#
#             best_component ← component
#             best_slots ← slots
#
#     return (best_component, best_slots)
#
# Helper B: Implement Altern and the expansion rule.
# METHOD expand(node, component, legal_slots)
#
#     FOR slot in legal_slots, in fixed order
#
#         child_assignment ← node.assignment.copy()
#         child_assignment.add(component, slot)
#
#         child_unassigned ← copy of node.unassigned
#         remove component from child_unassigned
#
#         child ← new ORNode(child_assignment, child_unassigned)
#         append child to node.children
#
# The complete search loop.
# METHOD search()
#
#     root ← new ORNode(
#         empty Assignment,
#         set containing all problem.components
#     )
#
#     frontier ← empty stack
#     push root onto frontier
#
#     WHILE frontier is not empty
#
#         IF budget.expired()
#             return ORResult(TIMEOUT, NONE)
#
#         node ← pop frontier
#         budget.consume()  # One step per processed node, including leaves.
#
#         IF NOT checker.isConsistent(node.assignment)
#             node.status ← "no"
#             continue
#
#         IF node.unassigned is empty
#             IF checker.isValid(node.assignment)
#                 node.status ← "yes"
#                 return ORResult(SUCCESS, node.assignment)
#
#             OTHERWISE
#                 node.status ← "no"
#                 continue
#
#         (component, slots) ← selectMRV(node)
#
#         IF slots is empty
#             node.status ← "no"
#             continue
#
#         expand(node, component, slots)
#
#         FOR child in node.children, in REVERSE order
#             push child onto frontier
#
#     return ORResult(FAILURE, NONE)

from .or_node import OrNode
from core.assignment import Assignment
from .or_result import OrResult

class ORTreeSearch:

    def __init__(self, problem, checker, budget) -> None:
        self.problem = problem
        self.checker = checker
        self.budget = budget
        self.root = None

    # Select the unassigned component that has the fewest legal slots left.
    def selectMRV(self, node: OrNode):
        best_component = None
        best_slots = None

        for component in self.problem.components:
            if component not in node.unassigned:
                continue

            slots = self.checker.legalSlots(component, node.assignment)

            if not slots:
                return component, []

            if best_slots is None or len(slots) < len(best_slots):
                best_component = component
                best_slots = slots

        return best_component, best_slots

    def expand(self,node: OrNode, component, legal_slots):
        for slot in legal_slots:
            child_assignment = node.assignment.copy()
            child_assignment.add(component, slot)

            child_unassigned = node.unassigned.copy()
            child_unassigned.remove(component)

            node.children.append(OrNode(child_assignment,child_unassigned))

    def search(self) -> OrResult:
        self.root = OrNode(Assignment(), set(self.problem.components))

        frontier: list[OrNode] = [self.root]

        while frontier:
            if self.budget.expired():
                return OrResult("TIMEOUT", None)

            node = frontier.pop()
            # One step pays for processing this node, including all its checks.
            # Keep TIMEOUT as the existing outcome for budget exhaustion.
            self.budget.consume()

            if not self.checker.isConsistent(node.assignment):
                node.status = "no"
                continue

            if not node.unassigned:
                if self.checker.isValid(node.assignment):
                    node.status = "yes"
                    return OrResult("SUCCESS", node.assignment)
                node.status = "no"
                continue

            component, slots = self.selectMRV(node)

            if component is None or not slots:
                node.status = "no"
                continue

            self.expand(node,component,slots)

            # A stack pops the last item pushed, so push the first child last.
            for child in reversed(node.children):
                frontier.append(child)

        return OrResult("FAILURE", None)
