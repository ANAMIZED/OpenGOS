# Contributing to OpenGOS

Thank you for helping build open infrastructure for funding open-source software and public goods.

## Ways to contribute

- **Data sources** — New adapters for foundations, EU programs, national funds, open-source funds
- **Agents** — Ranking signals, eligibility logic, drafting prompts, evaluation criteria
- **Evaluation** — Gold sets, benchmarks, human preference data
- **Documentation** — Tutorials, architecture notes, deployment guides
- **Bugs & UX** — Issues and pull requests are welcome
- **Agent UX** — Improvements to MCP tools, `AGENTS.md`, `SKILL.md`

## Development setup

```bash
git clone https://github.com/ANAMIZED/OpenGOS.git
cd OpenGOS
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -e ".[dev,agents]"
```

Run the MCP server:

```bash
opengos
# or
python -m opengrants
```

## Code style

- Python 3.11+
- `ruff` for linting and formatting
- Type hints encouraged
- Strong **provenance** and grounding for any funding-related claim
- Keep MCP tool names and signatures stable when possible

```bash
ruff check src
ruff format src
```

## Project conventions

Read [`AGENTS.md`](AGENTS.md) for the full agent-oriented map of the repo.

Key rules:

1. Public-goods funding is first-class (not secondary to federal grants)
2. Every opportunity should carry source + timestamp + official URL
3. Do not invent eligibility or award amounts
4. Prefer small, focused PRs

## Pull request process

1. Open an issue for larger changes when practical
2. Keep PRs focused
3. Ensure lint passes
4. Describe user-facing impact in the PR body
5. Update docs / README when you change the MCP tool surface

## License

By contributing, you agree that your contributions will be licensed under the Apache License 2.0.
