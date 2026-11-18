"""Soft-constraint scoring: eval and deltaMove."""

# PSEUDOCODE ONLY. Penalties follow the final proposal PDF, Section 2.3.
# Category weights and the four subfunctions follow the Input and Output
# Definition PDF, page 4. Hard constraints are handled by the checker.
#
# CLASS Evaluator
#
#     CONSTRUCTOR(problem, w_minfilled, w_pref, w_pair, w_secdiff,
#                 pen_lecturemin, pen_tutorialmin,
#                 pen_notpaired, pen_section)
#         REQUIRE weights, penalties, and preference values are nonnegative integers
#         store problem, weights, and penalties
#         # Zero weights are valid and disable that category's penalty.
#         # Weights and penalties come from CLI configuration, not readInput().
#
#     METHOD eval(assignment)
#         REQUIRE assignment is complete and valid, with accurate slot counters
#         return (
#             w_minfilled * evalMinfilled(assignment)
#             + w_pref * evalPref(assignment)
#             + w_pair * evalPair(assignment)
#             + w_secdiff * evalSecdiff(assignment)
#         )
#
#     METHOD evalMinfilled(assignment)
#         score <- 0
#
#         # Charge per missing component, including slots with zero assignments.
#         FOR slot IN problem.lec_slots
#             missing <- max(0, slot.min_desired - assignment.counts.get(slot, 0))
#             score <- score + pen_lecturemin * missing
#
#         FOR slot IN problem.tut_slots
#             missing <- max(0, slot.min_desired - assignment.counts.get(slot, 0))
#             score <- score + pen_tutorialmin * missing
#
#         return score
#
#     METHOD evalPref(assignment)
#         score <- 0
#         # Each preferred slot not received contributes its stated penalty.
#         FOR (component, preferred_slot, value) IN problem.preferences
#             IF assignment.placements[component] is not preferred_slot
#                 score <- score + value
#
#         return score
#
#     METHOD evalPair(assignment)
#         score <- 0
#         # Pairing means the SAME slot, not merely overlapping times.
#         # Count each supplied request; the proposal assumes same-type pairs.
#         FOR (a, b) IN problem.pairs
#             IF assignment.placements[a] is not assignment.placements[b]
#                 score <- score + pen_notpaired
#
#         return score
#
#     METHOD evalSecdiff(assignment)
#         score <- 0
#         # Count unordered pairs of lecture sections of the same course once.
#         FOR i FROM 0 TO length(problem.lectures) - 1
#             FOR j FROM i + 1 TO length(problem.lectures) - 1
#                 a <- problem.lectures[i]
#                 b <- problem.lectures[j]
#
#                 IF a.program = b.program AND a.number = b.number
#                     IF assignment.placements[a] is assignment.placements[b]
#                         score <- score + pen_section
#
#         return score
#
#     METHOD deltaMove(assignment, move, checker)
#         # Correct baseline first; optimize affected terms only if needed later.
#         candidate <- move.apply(assignment, problem, checker)
#         IF candidate is NONE
#             return NONE
#
#         return eval(candidate) - eval(assignment)
#
# A negative delta is an improvement. The hill climber initially uses full eval
# for moves and swaps, so it does not depend on an optimized deltaMove.
