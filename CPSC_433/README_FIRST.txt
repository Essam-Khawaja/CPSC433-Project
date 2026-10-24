CPSC 433 — TA-Shortened Proposal (16 pages)

How to use
1. Copy main.tex and the entire sections/ directory into your LaTeX project.
2. Compile main.tex twice with pdflatex (cross-references are resolved on the second pass).
3. Fill in the team member and submission date placeholders on the cover.

What changed relative to the previous 22-page condensed draft
- sections/2-problem.tex: IDENTICAL (kept as TA liked it).
- sections/5-set-based.tex: mathematical model, prose, and worked example preserved;
  removed the 52-line pseudocode block and replaced it with a short paragraph on
  data structures (assignment fact set, dictionaries, occupancy arrays) and operation.
- sections/6-and-tree.tex: rewritten as a focused ~3-page model/process/example;
  preserved the incumbent, exhaustive division, certified resolution, sound lower bound,
  MRV/DFS controller, global-optimality argument, and five-visit worked example.
  Removed long procedural exposition and all pseudocode.
- sections/4-or-tree.tex: replaced its pseudocode with a compact explanation and
  implementation data structures (assignment mapping, unassigned set, DFS stack).
- sections/7-integration.tex: replaced pseudocode with a two-case mathematical
  description of the OR -> Set / OR -> AND alternatives.
- main.tex: removed unused algorithm/algpseudocode packages.
- Other files remain unchanged.

Review points
- Confirm whether the instructor wants explicit proof certificates in the AND-tree
  definition; this version retains the essential invariant and proof.
- Confirm the existing same-type interpretation of pair requests in Section 2,
  inherited unchanged from the prior draft.
- Ensure formal notation aligns with the final input specification once distributed.
- TA approved two alternative pipelines (OR -> Set and OR -> AND), as user reported.

Keep previous draft as a backup; review the diff before merging teammate edits.
