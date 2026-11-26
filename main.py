#!/usr/bin/env python3
"""Roast the Smart Fridge: one line, best laugh wins.

The joke picks the fridge's most two-faced habit: it is supposed to keep
food cold and mind its own business, yet it acts like a nosy neighbour
who files a report on your midnight eating. The sting lands at the end
-- the thing you bought to chill your leftovers has appointed itself
your moral superior, and it does the judging from inside a lit box.
"""

import os
import sys
from pathlib import Path

ENTRY = "My smart fridge just emailed me a weekly report on my 2am snacking \u2014 I wanted cold leftovers, not a snitch with a lightbulb and a superiority complex."

MAX_CHARS = 160
DEST = Path(os.environ.get("OUTPUT_DIR", "/output")) / "entry.txt"


def gate_problems(line: str) -> list:
    """Collect every way the line could fail the bounty gate."""
    problems = []
    cleaned = line.strip()
    if cleaned != line:
        problems.append("roast has leading or trailing whitespace")
    if not cleaned:
        problems.append("roast is empty or only whitespace")
    if len(line) > MAX_CHARS:
        problems.append(f"roast is {len(line)} chars, over the {MAX_CHARS} limit")
    if "\n" in line or "\r" in line:
        problems.append("roast must fit on one line")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("roast is not valid UTF-8 text")
    return problems


def emit(line: str) -> Path:
    """Check the roast, write it out, then prove the file matches."""
    faults = gate_problems(line)
    if faults:
        raise ValueError("; ".join(faults))
    DEST.parent.mkdir(parents=True, exist_ok=True)
    # No trailing newline: the file must hold exactly the roast, byte for byte.
    DEST.write_text(line, encoding="utf-8")
    on_disk = DEST.read_text(encoding="utf-8")
    if on_disk != line:
        raise ValueError("entry.txt on disk differs from the roast")
    return DEST


def main() -> int:
    try:
        target = emit(ENTRY)
    except ValueError as err:
        print(f"refused to write entry: {err}", file=sys.stderr)
        return 1
    print(f"wrote {len(ENTRY)} chars ({len(ENTRY.encode('utf-8'))} bytes) to {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
