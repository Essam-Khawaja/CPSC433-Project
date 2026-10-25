# CPSC 433 Project — Course Timetabling via Three Search Paradigms

Group project proposal for CPSC 433 (Artificial Intelligence), University of Calgary, Fall 2025.
It proposes two search systems for the course timetabling problem: OR-tree feasibility followed
by set-based improvement (Proposal A), and OR-tree feasibility followed by AND-tree
branch-and-bound (Proposal B).

**📄 Latest PDF (from `main`): <https://essam-khawaja.github.io/CPSC433-Project/proposal.pdf>**

## Layout

```
CPSC_433/
├── main.tex              # Preamble, notation macros, title page, bibliography
├── sections/             # One file per section, so members can edit in parallel
│   ├── abstract.tex
│   ├── 1-introduction.tex … 9-conclusion.tex
│   └── appendix-a-constraints.tex, appendix-b-derivations.tex
└── D2L Instructions/     # Assignment and problem descriptions from D2L
```

## Building

The PDF is built by CI and is not tracked in git (`CPSC_433/main.pdf` is ignored).

- **`main`:** every push rebuilds the PDF and deploys it to the link above.
- **Other branches and PRs:** the PDF is attached to that run on the
  [Build PDF workflow page](https://github.com/Essam-Khawaja/CPSC433-Project/actions/workflows/build-pdf.yml).

To build locally:

```bash
cd CPSC_433 && latexmk -pdf main.tex
```

## Workflow

Work on your own branch and merge into `main` when a section is ready.
`\TODO{...}` blocks mark what each section still needs; they render as highlighted "[TO FILL: …]" notes in the PDF.
