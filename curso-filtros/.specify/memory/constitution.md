<!--
## Sync Impact Report
- Version change: 1.0.0 → 1.1.0 (MINOR: new pedagogical section added)
- Modified principles: None renamed
- Added sections: "Principios Pedagógicos del Curso de Filtros Bayesianos" (VII–XVI)
- Removed sections: None
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md — Project Type hint + Notebook context added
  - ✅ .specify/templates/tasks-template.md — Module structure task types noted
  - ✅ .specify/templates/spec-template.md — No structural changes required
  - ✅ Toolchain & Stack — Jupyter + nbval added
- Follow-up TODOs: None
-->

# curso-filtros Constitution

## Core Principles

### I. Código Limpio y Tipado Estático Estricto

All source code MUST target Python 3.12+ and pass `mypy --strict` without errors.
Type hints are MANDATORY on every function signature, variable with non-obvious
type, and class attribute. Use of `Any`, `cast`, or `# type: ignore` MUST be
justified with an inline comment explaining why no typed alternative exists;
unsupported suppressions block PR merge. `ruff` is the enforced formatter and
linter; no exceptions.

**Rationale**: Strict typing eliminates entire classes of runtime bugs and makes
refactoring safe in a signal-processing codebase where numeric type mismatches
produce silent, hard-to-diagnose errors.

### II. Tests Obligatorios con pytest

Tests with `pytest` are MANDATORY for every feature — not optional. Coverage
MUST NOT fall below 80% (enforced via `pytest-cov --fail-under=80`). Test files
MUST reside in `tests/` mirroring the `src/` layout. Integration tests MUST
cover the SQLite persistence paths. PRs that lower coverage below the threshold
MUST NOT be merged without a documented exception approved in the PR thread.

**Rationale**: A 80% coverage gate ensures all critical signal-processing paths
are verified without demanding 100% on trivial glue code. Mandatory enforcement
prevents "we'll add tests later" drift.

### III. Persistencia Local — Solo SQLite

The ONLY permitted persistence layer is SQLite, accessed via the `sqlite3`
stdlib module or `aiosqlite` for async paths. No cloud databases, no remote APIs
for data storage, no external ORMs that obscure the local-only constraint.
All data resides in a project-local `.db` file. Schema changes MUST be captured
as versioned migration scripts under `db/migrations/`.

**Rationale**: Local-only storage eliminates network dependencies, ensures the
project runs on any student machine without account setup, and keeps the
educational focus on signal processing — not infrastructure.

### IV. UX Prioritaria — Comandos Cortos y Mensajes Claros

CLI entry points MUST be short: maximum 3 tokens (e.g., `filtros run`,
`filtros plot`, `filtros export`). Every error message MUST state (1) what went
wrong and (2) what the user should do next — in plain language. Help text
(`--help`) MUST fit one terminal screen without scrolling. Interactive prompts
MUST show sensible defaults in brackets, e.g., `Window size [64]:`. Verbose
debug output MUST be hidden behind a `--verbose` / `-v` flag.

**Rationale**: The primary audience is students and researchers who need fast
iteration, not CLI experts. Confusing UX wastes class time and discourages
exploration of the filter tooling.

### V. Visualización: Plotly para Estático, Rerun.io para Tiempo Real

Static visualizations (filter frequency responses, spectrograms, comparison
charts, export figures) MUST use Plotly. Real-time or streaming visualizations
(live signal feeds, step-by-step filter animation) MUST use `rerun-sdk`. Using
both libraries for the same data type in the same feature is PROHIBITED.
All Plotly outputs MUST be exportable as HTML and PNG. All Rerun sessions MUST
save `.rrd` recordings when requested.

**Rationale**: Plotly and Rerun.io cover complementary use cases. A clear rule
for which to use prevents ad-hoc library sprawl and inconsistent UX across the
tool.

### VI. Simplicidad — YAGNI Estricto

Features MUST be implemented at the minimum complexity that satisfies stated
requirements. Abstractions MUST NOT be introduced speculatively. Three similar
code blocks MAY trigger a refactor; two MUST NOT. No new dependency may be added
without an explicit one-line justification in the PR description. Complexity
violations MUST be documented in the Complexity Tracking table of `plan.md`
before merge.

**Rationale**: This is a teaching and research tool. Architectural complexity
that obscures the signal-processing logic defeats the educational purpose of the
project.

## Principios Pedagógicos del Curso de Filtros Bayesianos

### VII. Rigor Matemático Sin Saltos Lógicos

Every derivation, proof, and mathematical development in course materials MUST be
complete. Steps MUST NOT be omitted with "puede demostrarse que…" without a
citation or a linked appendix. Intuitive explanations MUST precede, not replace,
formal derivations. Approximations MUST be explicitly labeled as approximations
with stated validity conditions.

**Rationale**: Students learning Bayesian filtering cannot build reliable intuition
on top of gaps. Each hidden step becomes a source of persistent confusion.

### VIII. Equilibrio Teoría-Práctica (50/50)

Each module MUST dedicate approximately equal effort to theoretical content and
hands-on Python implementation. Pure theory modules with no practical section are
PROHIBITED. Pure coding exercises with no theoretical grounding are PROHIBITED.
The split need not be line-by-line equal but MUST be evident at the module level.

**Rationale**: Understanding without implementation is fragile; implementation
without understanding is brittle. Both halves reinforce the other.

### IX. Estructura de Módulo Estándar

Every module MUST contain the following seven sections, in order:

1. **Objetivos de aprendizaje** — measurable, specific outcomes
2. **Prerequisitos** — explicit links to prior modules or concepts required
3. **Intuición** — informal explanation before any formula
4. **Derivación formal** — step-by-step mathematical development
5. **Ejemplo numérico paso a paso** — worked with concrete numbers
6. **Ejercicios guiados** — student-facing problems with scaffolding
7. **Evaluación** — self-assessment with expected answers or criteria

Omitting any section MUST be justified in the module header with a reason and
an approved alternative.

**Rationale**: A predictable structure reduces cognitive load so students focus
on content, not navigation. It also makes the course maintainable across authors.

### X. Notebooks Autoexplicativos y Ejecutables

Every Jupyter notebook MUST run successfully from top to bottom with a single
"Run All" command on a clean, freshly-created environment. Notebooks MUST NOT
require manual state manipulation (e.g., running cells out of order, setting
variables by hand). Every notebook MUST reference or include an environment
specification (`pyproject.toml` or `requirements.txt`).

**Rationale**: A notebook that breaks on "Run All" cannot be used in class and
erodes student trust in the material.

### XI. Reproducibilidad Educativa en Python

Every notebook MUST fix the random seed at the first code cell (`np.random.seed(42)`
or equivalent — document the library used). Cell execution order MUST follow
reading order; no cell may depend on output from a later cell. Every plot MUST
include: axis labels with units, a title, and a legend when multiple series appear.

**Rationale**: Fixed seeds ensure every student sees identical output, making
debugging and grading deterministic. Labeled plots are first-class teaching
artifacts, not afterthoughts.

### XII. Validación Numérica y Comparación de Métodos

Every implemented filter MUST include a numerical validation section that verifies
correctness against a known-good reference: an analytic solution, a `scipy`
reference implementation, or a published numerical result with citation. When two
or more methods solve the same problem, a side-by-side comparison (table or plot)
MUST be included highlighting trade-offs.

**Rationale**: Students learn both that their code is correct AND how methods
differ in practice — two lessons for the cost of one.

### XIII. Criterios de Éxito Medibles por Práctica

Every practical exercise MUST define explicit success criteria: an expected
numerical output (with tolerance), an expected plot characteristic, or a
pass/fail assertion executable in code. "El estudiante comprenderá X" is NOT a
valid success criterion — replace with an observable behavior or measurable output
(e.g., "RMSE < 0.05 on the provided test signal").

**Rationale**: Vague criteria make self-assessment impossible and grading
inconsistent. Concrete criteria let students know when they are done.

### XIV. Diagnóstico de Errores Comunes

Every module MUST include a "Errores comunes" section documenting at least two
typical mistakes students make in that topic area. For each mistake the section
MUST provide: (1) the symptom (what the student observes), (2) the diagnosis
procedure, and (3) the correct resolution. This section MUST appear before the
Evaluación section.

**Rationale**: Documenting known failure modes reduces frustration, cuts support
burden, and models the expert habit of anticipating errors.

### XV. Español Técnico Claro

All course materials MUST be written in Spanish. Technical terms that are
conventionally used in English (e.g., "Kalman filter", "prior", "likelihood",
"belief") MAY be retained but MUST be defined in Spanish on first use within each
module. Mathematical notation MUST be consistent across all modules and captured
in a shared `glosario.md` file at the repository root.

**Rationale**: A course in Spanish that peppers undefined English terms signals
carelessness and creates barriers for students whose first language is not English.

### XVI. Cierre Reflexivo de Módulo

Every module MUST end with two mandatory subsections:

- **¿Qué aprendiste?** — a bullet-point summary (≥ 5 items) of key concepts,
  written in first-person plural (e.g., "Aprendimos que la covarianza del error…")
- **¿Qué sigue?** — a forward pointer naming the next module or concept, and
  describing concretely how this module's content enables it

These two subsections MUST appear as the final cells of every notebook.

**Rationale**: Explicit metacognitive closure reinforces retention. Knowing "what
comes next" reduces anxiety and motivates students to continue.

## Toolchain & Stack

- **Runtime**: Python 3.12+ (declared in `pyproject.toml` `requires-python`)
- **Type checker**: `mypy --strict` (required, enforced in CI and local `make check`)
- **Linter/formatter**: `ruff` (replaces flake8 + black + isort — single tool)
- **Testing**: `pytest` + `pytest-cov` (coverage gate: `--fail-under=80`)
- **Notebook testing**: `nbval` (validates notebooks execute without error in CI)
- **Notebooks**: `jupyter` + `nbconvert` (HTML/PDF export for distribution)
- **Persistence**: SQLite via `sqlite3` (stdlib) or `aiosqlite` (async paths)
- **Static visualization**: `plotly`
- **Real-time visualization**: `rerun-sdk`
- **Dependency management**: `uv` preferred; fallback `pip` with `pyproject.toml`
- **CI**: GitHub Actions — runs `mypy --strict`, `ruff check`, `pytest --cov`,
  `nbval` on all notebooks

Cloud SDKs, remote databases, and telemetry libraries MUST NOT be added without
a constitution amendment.

## Development Workflow

- Feature branches MUST follow the pattern `###-short-description`.
- Every PR MUST pass: `mypy --strict`, `ruff check`, `pytest --cov --fail-under=80`,
  and `nbval` on all modified notebooks.
- Commits MUST be atomic: one logical change per commit.
- The `master` branch MUST always be in a runnable state (`filtros --help` exits 0
  and all notebooks pass `nbval`).
- Documentation lives in `docs/` as plain Markdown; auto-generated API docs are
  optional but MUST NOT replace human-written usage guides.
- Migration scripts under `db/migrations/` MUST be applied and committed before
  any code that depends on schema changes is merged.
- Every new course module MUST follow Principle IX (Estructura de Módulo Estándar)
  before the PR is opened.

## Governance

This constitution supersedes all prior informal conventions for `curso-filtros`.
Amendments MUST:

1. Be proposed as a PR that modifies this file.
2. State the semantic version bump type (MAJOR/MINOR/PATCH) with rationale.
3. Update all affected templates in `.specify/templates/` in the same PR.
4. Be merged before any feature relying on the amendment begins implementation.

All PR reviewers MUST verify compliance against each principle in the
Constitution Check section of `plan.md`. Unjustified violations block merge.

**Version**: 1.1.0 | **Ratified**: 2026-05-20 | **Last Amended**: 2026-05-20
