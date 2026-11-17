# Timetable source

This directory scaffolds the pipeline: parse input -> OR-tree feasibility search
-> set-based hill climbing -> output. The new modules and tests are placeholders;
the pipeline is not implemented yet.

## Layout and ownership

| Path | Responsibility | Owner role |
| --- | --- | --- |
| `main.py` | Connect parsing, searches, and output | Pipeline integration |
| `model/` | Slots, components, domains, conflict graph, input parsing, 851/913 bookings | Parser owner |
| `core/assignment.py` | Timetable assignments and slot counters | Shared core |
| `core/constraint_checker.py` | `canAssign`, `legalSlots`, `isValid` | Checker owner |
| `core/evaluator.py` | `eval`, `deltaMove` | Evaluator owner |
| `core/time_budget.py` | Shared search time budget | Shared core |
| `ortree/` | OR-tree nodes, feasibility search, results | OR-tree owner |
| `setbased/` | Extension rules, moves, swaps, neighbourhood, hill climbing, results | Set-based owner |
| `output/` | Final timetable output | Pipeline integration |
| `tests/` | Component tests and end-to-end pipeline tests | Respective module owners |
| `tests/fixtures/` | Paper's tiny example and brute-force reference solver | Shared testing |
| `inputs/` | Course sample input files, including `input.txt` | Parser owner |

`genetic_algorithm.py` remains at this directory's root and is unchanged.

## Running

No timetable command-line interface is implemented yet. `main.py` is reserved
for the pipeline entry point.

Run test discovery from the repository root:

```sh
python3 -m unittest discover -s src/tests
```

The test files currently contain no test cases.

## Input and output

`inputs/input.txt` preserves the existing sample input. The parser will read
the course input format and add the required 851/913 bookings.

`output/output_writer.py` is reserved for the final timetable writer. Its output
format and the pipeline's command-line arguments still need to be implemented.
