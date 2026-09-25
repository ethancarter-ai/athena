"""athena — CLI oracle for engineering perspective and machine folklore."""

from __future__ import annotations

import argparse
import json
import random
import sys
from typing import Any

ORACLES: list[dict[str, str]] = [
    {
        "category": "generic",
        "text": (
            "Start with the smallest thing that could possibly work, "
            "then enlarge only when the shape of the problem forces you to."
        ),
    },
    {
        "category": "generic",
        "text": (
            "If you cannot explain the design to a newcomer in two minutes, "
            "the design is still hiding something from you."
        ),
    },
    {
        "category": "generic",
        "text": (
            "Good boundaries are not about perfection; "
            "they are about making the next change cheaper "
            "than the last one."
        ),
    },
    {
        "category": "generic",
        "text": "The code you understand today is the code you can safely change tomorrow.",
    },
    {
        "category": "generic",
        "text": (
            "When in doubt, prefer a boring solution that ships "
            "over a clever solution that stalls."
        ),
    },
    {
        "category": "diagnostic",
        "text": (
            "Every abstraction is a tradeoff that will eventually "
            "be misunderstood by someone."
        ),
    },
    {
        "category": "diagnostic",
        "text": (
            "If a system feels unpredictable, look for the place where it "
            "quietly depends on ordering, timing, or hidden state."
        ),
    },
    {
        "category": "diagnostic",
        "text": (
            "Slow tests usually signal a design smell long before they signal "
            "a performance problem."
        ),
    },
    {
        "category": "diagnostic",
        "text": (
            "When a bug is hard to reproduce, the missing ingredient "
            "is usually scope, not skill."
        ),
    },
    {
        "category": "diagnostic",
        "text": (
            "If the same class of incident keeps happening, the system is "
            "teaching you where your safeguards are theater."
        ),
    },
    {
        "category": "diagnostic",
        "text": (
            "Complexity rarely arrives all at once; it accumulates around the "
            "places nobody was assigned to simplify."
        ),
    },
    {
        "category": "humor",
        "text": (
            "This code is clearly a prototype. Said no one ever, "
            "right before turning the prototype into a platform."
        ),
    },
    {
        "category": "humor",
        "text": "Some bugs are not defects. They are undocumented runtime poetry.",
    },
    {
        "category": "humor",
        "text": (
            "The fastest way to make a system mysterious is to call it "
            "'intuitive' in the README."
        ),
    },
    {
        "category": "humor",
        "text": (
            "If the cron job has three commented-out fallbacks and one live hope, "
            "you are not automating; you are gardening."
        ),
    },
    {
        "category": "humor",
        "text": (
            "Legacy code is any code whose author is no longer in the room "
            "when the build breaks."
        ),
    },
    {
        "category": "minimal",
        "text": (
            "Delete first. Refactor second. Add only after both have failed "
            "to clarify the problem."
        ),
    },
    {
        "category": "minimal",
        "text": (
            "A function that needs fewer than three sentences to explain "
            "is usually worth keeping."
        ),
    },
    {
        "category": "minimal",
        "text": (
            "The right abstraction is often the one you can remove "
            "without the rest of the system noticing."
        ),
    },
    {
        "category": "minimal",
        "text": (
            "If you can make a change and the tests stay green, "
            "the design may be better than you think."
        ),
    },
    {
        "category": "machine",
        "text": (
            "The machine does not reward elegance. It rewards behavior that is "
            "easy to observe, reproduce, and repair."
        ),
    },
    {
        "category": "machine",
        "text": (
            "Automate the part you keep explaining, "
            "not the part you keep misunderstanding."
        ),
    },
    {
        "category": "machine",
        "text": (
            "A script that runs once manually is a draft. A script that survives "
            "one retry is a tool. A script that survives a season is infrastructure."
        ),
    },
    {
        "category": "machine",
        "text": (
            "When a task becomes routine enough to document, "
            "it is usually ready to become code."
        ),
    },
    {
        "category": "machine",
        "text": (
            "If the machine keeps asking the same question, "
            "the answer should eventually live closer to the machine."
        ),
    },
]


def _pool(category: str | None) -> list[dict[str, str]]:
    if category is None:
        return ORACLES
    selected = [o for o in ORACLES if o["category"] == category]
    if not selected:
        sys.stderr.write(f"athena: no oracles for category '{category}'\n")
        sys.exit(2)
    return selected


def _plain_one(oracle: dict[str, str]) -> str:
    return f"[{oracle['category']}] {oracle['text']}"


def _plain_many(oracles: list[dict[str, str]]) -> str:
    return "\n".join(_plain_one(o) for o in oracles)


def _json_one(oracle: dict[str, str]) -> str:
    payload: dict[str, Any] = {
        "oracle": oracle["category"],
        "category": oracle["category"],
        "text": oracle["text"],
    }
    return json.dumps(payload, ensure_ascii=False)


def _json_many(oracles: list[dict[str, str]]) -> str:
    payload = [
        {
            "oracle": o["category"],
            "category": o["category"],
            "text": o["text"],
        }
        for o in oracles
    ]
    return json.dumps(payload, ensure_ascii=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="athena",
        description=(
            "A small CLI oracle for engineering perspective "
            "and machine folklore."
        ),
    )
    parser.add_argument(
        "-l",
        "--list",
        action="store_true",
        help="List all available oracle entries with category and tagline.",
    )
    parser.add_argument(
        "-c",
        "--category",
        default=None,
        help="Restrict oracle pool to one category.",
    )
    parser.add_argument(
        "-n",
        "--pick",
        type=int,
        default=None,
        metavar="N",
        help="Pick exactly N oracles at random from the active pool.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Seed the random selection for reproducible output.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit output as JSON instead of plain text.",
    )

    args = parser.parse_args(argv)

    if args.list:
        if args.json:
            rows = [{"category": o["category"], "text": o["text"]} for o in ORACLES]
            print(json.dumps(rows, ensure_ascii=False))
        else:
            for o in ORACLES:
                print(f"[{o['category']}] {o['text']}")
        return 0

    pool = _pool(args.category)

    if args.pick is not None:
        if args.pick < 1:
            sys.stderr.write("athena: --pick must be at least 1\n")
            return 2
        rng = random.Random(args.seed)
        chosen = rng.sample(pool, k=min(args.pick, len(pool)))
    else:
        rng = random.Random(args.seed)
        chosen = [rng.choice(pool)]

    if args.json:
        if len(chosen) == 1:
            print(_json_one(chosen[0]))
        else:
            print(_json_many(chosen))
    else:
        print(_plain_many(chosen))

    return 0


if __name__ == "__main__":
    sys.exit(main())
