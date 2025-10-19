# Repository Guidelines

## Project Structure & Module Organization
The runtime package now lives entirely under `stateset/`. The async client lives in `stateset/client.py` and exposes the high-level `Stateset` entry point. Lightweight resource wrappers live in `stateset/resources/` (`base.py`, `orders.py`, `returns.py`, etc.) and rely on the shared HTTP stack in the client. We removed the broken OpenAPI-generated surface (`api/`, `models/`, legacy `client.py`) in favour of this slimmer layout. Shared type aliases and exceptions remain in `stateset/types.py` and `stateset/errors.py`. Tests are concentrated in `tests/test_client.py`, which uses `httpx.MockTransport` to exercise the async client without real network calls.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` creates an isolated environment.
- `pip install -e .[dev]` installs runtime and tooling in editable mode.
- `python -m pytest -q` runs the suite and produces coverage data (`--cov=stateset` still writes `htmlcov/` and `coverage.xml`).
- `ruff check .` enforces linting aligned with `pyproject.toml`.
- `black .` formats code to the shared 88-character standard.
- `mypy stateset` performs type checking against Python 3.8+.

## Coding Style & Naming Conventions
Stick to 4-space indentation, 88-character lines, and explicit type hints. New resources should extend `CollectionResource` from `stateset/resources/base.py` and live in their own module (for example, `stateset/resources/payments.py`). Use `snake_case` for modules and functions, `PascalCase` for classes, and keep constants upper snake case. Run `black` before committing, then `ruff check` to ensure formatting and linting remain aligned with the configuration.

## Testing Guidelines
Author tests under `tests/` with `pytest` and prefer async-aware helpers (`pytest.mark.asyncio`). Use `httpx.MockTransport` or stubbed `_requestor` objects to avoid hitting real endpoints. Maintain coverage by inspecting the terminal summary or the generated HTML report; if a change would intentionally lower coverage, call it out in the pull request description.

## Commit & Pull Request Guidelines
History favors concise, present-tense messages (`add async client wrapper`). Keep subject lines under 72 characters and focus on the observable behavior change. In pull requests, describe the motivation, summarize the solution, and list the local commands you ran (`python -m pytest -q`, `ruff check .`, etc.) so reviewers can reproduce results. Link related issues or tickets when available.

## Configuration & Secrets
Instantiate the client with `Stateset(api_key="...", base_url=...)` or pass a pre-configured `httpx.AsyncClient` when you need custom transports. Never commit API keys or sample secrets; rely on environment variables or ignored config files and scrub sensitive values from logs before sharing reproduction steps.
