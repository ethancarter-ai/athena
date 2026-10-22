# athena — CLI Oracle

**athena** is a zero-dependency Python CLI that dispenses wisdom, answers, and perspective from a curated set of oracles. Open it when you need a nudge, a diagnosis, or a playful bit of machine folklore — and pipe the output into scripts, logs, or your shell prompt.

## About

Developers often reach for a quick external opinion before committing to a path: is this architecture sound? should I refactor now or later? is this the right abstraction? **athena** gives you a small, fast, offline oracle that returns a single self-contained answer per invocation — no network, no setup beyond `pip install`, and no state to maintain.

It is not a fortune teller. It is a deliberately small collection of hard-won engineering perspective, phrased as standalone statements that stand on their own without additional context.

## Features

- **Multiple oracles** — choose from voices like `generic`, `diagnostic`, `humor`, `minimal`, or `machine` without installing extra data.
- **Single-answer mode** — `athena` prints one oracle entry and exits; ideal for prompts, aliases, and CI messages.
- **List mode** — `athena --list` prints every available oracle entry with its category and a short tagline.
- **Category filter** — `athena --category diagnostic` narrows the pool before picking.
- **Deterministic picks** — `--seed 42` makes `--pick` reproducible for demos and tests.
- **JSON output** — `--json` emits a single JSON object with `oracle`, `category`, and `text` fields.
- **Zero runtime dependencies** — stdlib only; works on Python 3.11+.

## Installation

```bash
python -m pip install athena
```

Or run from a checkout:

```bash
git clone <repo-url>
cd athena
python -m pip install -e .
```

## Usage

```bash
athena [options]
```

### Options

| Flag                   | Description                                                              |
|------------------------|--------------------------------------------------------------------------|
| `-l, --list`           | List all available oracle entries with category and tagline.            |
| `-c, --category <cat>` | Restrict oracle pool to one category (e.g. `diagnostic`, `humor`).     |
| `-n, --pick <N>`       | Pick exactly N oracles at random from the active pool.                  |
| `--seed <int>`         | Seed the random selection for reproducible output.                      |
| `--json`               | Emit output as a JSON object instead of plain text.                     |
| `--help`               | Show help and exit.                                                      |

### Examples

```bash
# One random oracle
athena

# Diagnose a fuzzy feeling about a design
athena --category diagnostic

# Pick three independent perspectives
athena --pick 3

# Reproducible output for a demo
athena --pick 2 --seed 7

# Machine-readable output
athena --json

# List everything available
athena --list
```

### Output shape

Plain text mode prints one line per oracle:

```
[diagnostic] Every abstraction is a tradeoff that will eventually be misunderstood by someone.
```

JSON mode emits a single object:

```json
{"oracle": "diagnostic", "category": "diagnostic", "text": "Every abstraction is a tradeoff that will eventually be misunderstood by someone."}
```

When `--pick 3` is used in JSON mode, the result is a JSON array of objects.

## Project Structure

```
athena/
├── athena.py         # CLI entrypoint and oracle dataset
├── pyproject.toml    # Package metadata, entrypoint, tool config
├── README.md         # This file
└── .gitignore        # Python build artifacts and common noise
```

- `athena.py` — flat single-module implementation: oracle data, formatting, argparse CLI
- `pyproject.toml` — packaging, console script, ruff config
- `README.md` — user-facing documentation
- `.gitignore` — keeps build metadata and editor noise out of the repo

## Tech Stack

- Python 3.11+
- Standard library only (`argparse`, `json`, `random`, `sys`)
- `pyproject.toml` packaging with a `athena` console script entrypoint
- Flat single-module layout for minimal friction

## Tags / Keywords

`cli`, `oracle`, `developer-tools`, `wisdom`, `terminal`, `zero-dependency`, `python`

## License

MIT

## Repository

- [Source](https://github.com/ethancarter-ai/athena)
