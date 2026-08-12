# Contributing to OpenGOS

Thank you for helping build open infrastructure for funding open-source software and public goods.

## Ways to Contribute

- **Data sources**: New crawlers / adapters for NSF, NIH, Horizon Europe, foundations, open-source funds
- **Agents**: Ranking signals, eligibility logic, drafting prompts, evaluation criteria
- **Evaluation**: Gold sets, benchmarks, human preference data
- **Documentation**: Tutorials, architecture deep-dives, deployment guides
- **Bugs & UX**: Issues and pull requests are welcome

## Development Setup

```bash
git clone https://github.com/ANAMIZED/OpenGOS.git
cd OpenGOS
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev,agents]"
```

## Code Style

- Python 3.11+
- `ruff` for linting and formatting
- Type hints encouraged
- Strong provenance and grounding for any funding-related claim

## Pull Request Process

1. Open an issue for larger changes when practical
2. Keep PRs focused
3. Ensure tests / lint pass when applicable
4. Describe user-facing impact in the PR body
