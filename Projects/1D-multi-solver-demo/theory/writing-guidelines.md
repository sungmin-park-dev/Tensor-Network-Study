# Theory Writing Guidelines For Agents

## Purpose

This document defines the writing rules for theory notes in `1D-multi-solver-demo`. It combines the
LSWT writing-style policy with local conventions established during the exact-solution note review.

The source policy is:

- `/Users/david/GitHub/Linear-Spin-Wave-Theory/GOVERNMENT/Agents-Bylaws/policies/lswt-writing-style.md`

These guidelines apply to theory notes that may later be promoted to LSWT or to the Study vault.

## Core Writing Style

- State the physical object, model, or derivation step before giving broad background.
- Move quickly to the relevant definition, Hamiltonian, or derivation target.
- Keep equations central to the argument.
- Introduce new symbols immediately before or after first use.
- Avoid using `where` as a repeated template after every equation.
- Use `Therefore`, `Thus`, and `Note that` only when they mark a real transition.
- State the condition under which a claim holds, such as OBC, PBC, a fixed parity sector, or a chosen
  convention.
- After an important equation, add one short sentence explaining its role or consequence.
- Do not mix implementation plans, benchmark management, or agent notes into theory exposition.

## Obsidian Math

- Inline math must use `$...$`.
- Display math must use `$$...$$`.
- Do not use `\(...\)` or `\[...\]`.
- Use display math for central equations.
- Use inline math for short definitions or secondary references.

## Self-Contained Definitions

- A model document must be readable without relying on the project Hamiltonian family.
- A `Definition` section must define the Hamiltonian, bond notation, operator notation, and relevant
  boundary convention when they are needed for the displayed equations.
- Do not write a model definition only as a parameter slice of a larger Hamiltonian family.
- If a model is also known as a point or limit of a larger family, mention that in the introduction,
  not as the primary definition.

## Exact-Solution Note Structure

The current draft structure for exact-solution notes is:

```text
Introduction -> Definition -> Solution -> Physical Quantities -> References
```

This structure is provisional and may be revised after review.

Within `Solution`, use boundary-condition subsections when the finite-size solution depends on the
boundary condition:

```text
Solution
  Open Boundary Condition
  Periodic Boundary Condition
```

## Method And Model Separation

- Method documents explain general transformations, assumptions, and caveats.
- Model-specific documents contain Hamiltonians, boundary terms, spectra, and benchmark references.
- Do not put a model-specific boundary term, such as the XX model PBC hopping term, in a general
  Jordan-Wigner method note.
- Do not use a model-specific exact-solution note as a general method reference.

## Notation Discipline

- Do not introduce a symbol that is used only once when prose is clearer.
- Prefer existing project notation unless it creates a conflict.
- Use $L$ for chain length and $i=0,1,\ldots,L-1$ for site indices in this project.
- Use $N_f$ for fermion number.
- Use $\Pi$ for the total fermion-parity operator.
- Use $\lambda_{\Pi}$ for a total parity eigenvalue.
- Use $\pi_i=1-2n_i$ for local fermion parity when local parity must be named.

## Review Discipline

- Modify only the part the user asked to change.
- If the requested change is ambiguous, ask before editing.
- Keep derivation, convention, benchmark use, and open issues separate.
- If a paragraph becomes too broad, move model-specific details to the corresponding model note.
- Before treating a statement as canonical, check whether it is a derivation, a convention, a
  benchmark requirement, or an open review issue.

## Anti-Patterns

- Repeating `where` after every display equation.
- Starting many paragraphs with the same transition phrase.
- Calling an unverified step `clear`, `obvious`, or `intuitive`.
- Using project-specific benchmark language as if it were part of the model definition.
- Mixing method-level claims with model-specific equations.
- Adding implementation tasks or future plans to theory exposition.
