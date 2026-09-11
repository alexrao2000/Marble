#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile


DEFAULT_PATH = Path("/Users/alexrao/.codex/phrase-preferences/phrases.json")


def validate_ledger(value: object) -> dict[str, object]:
    if not isinstance(value, dict):
        raise ValueError("ledger must be a JSON object")
    if set(value) != {"version", "love", "hate"}:
        raise ValueError("ledger must contain exactly version, love, and hate")
    if type(value["version"]) is not int or value["version"] != 1:
        raise ValueError("ledger must use version 1")
    if not isinstance(value["love"], list) or not isinstance(value["hate"], list):
        raise ValueError("love and hate must be lists")
    if not all(isinstance(item, str) for key in ("love", "hate") for item in value[key]):
        raise ValueError("love and hate entries must be strings")
    return {"version": 1, "love": list(value["love"]), "hate": list(value["hate"])}


def update_preference(path: Path, preference: str, phrase: str) -> dict[str, object]:
    if preference not in {"love", "hate"}:
        raise ValueError("preference must be love or hate")
    phrase = phrase.strip()
    if not phrase:
        raise ValueError("phrase must be non-empty")

    if path.exists():
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError("ledger must contain valid JSON") from exc
        ledger = validate_ledger(raw)
    else:
        ledger = {"version": 1, "love": [], "hate": []}

    folded = phrase.casefold()
    ledger["love"] = [item for item in ledger["love"] if item.casefold() != folded]
    ledger["hate"] = [item for item in ledger["hate"] if item.casefold() != folded]
    ledger[preference].append(phrase)

    path.parent.mkdir(parents=True, exist_ok=True)
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temp_name = handle.name
            json.dump(ledger, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
        temp_name = None
    finally:
        if temp_name is not None:
            Path(temp_name).unlink(missing_ok=True)
    return ledger


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Record a phrase preference.")
    parser.add_argument("preference", choices=("love", "hate"))
    parser.add_argument("phrase")
    parser.add_argument("--file", type=Path, default=DEFAULT_PATH)
    args = parser.parse_args(argv)
    try:
        ledger = update_preference(args.file, args.preference, args.phrase)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(json.dumps(ledger, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
