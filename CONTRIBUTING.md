# Contributing to OpenGrants OS

Thank you for helping build the open infrastructure for funding open-source AI and public goods.

## Ways to Contribute

- **Data sources**: New crawlers / adapters for NSF, NIH, Horizon Europe, foundations, open-source funds
- **Agents**: Ranking signals, eligibility logic, drafting prompts, red-team criteria
- **Evaluation**: Gold sets, benchmarks, human preference data
- **Documentation**: Tutorials, architecture deep-dives, deployment guides
- **Bugs & UX**: Issues and pull requests are very welcome

## Development Setup

```bash
git clone https://github.com/ANAMIZED/opengrants-os.git
cd opengrants-os
python -m venv .venv
source .venv/bin/activate   # or Windows equivalent
pip install -e ".[dev,agents]"
```

## Code Style

- Python 3.11+
- `ruff` for linting and formatting
- Type hints encouraged
- Strong provenance and grounding for any grant-related claim

## Pull Request Process

1. Fork and create a feature branch
2. Keep changes focused
3. Add tests where practical
4. Update docs/README if behavior changes
5. Open a PR with a clear description of *why*

## Code of Conduct

Be respectful, collaborative, and focused on the public-good mission. Harassment or bad-faith contributions will not be tolerated.

## License

By contributing you agree that your contributions will be licensed under the Apache License 2.0.
