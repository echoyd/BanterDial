#!/usr/bin/env python3
"""Validate one or more Banter Card TOML files without modifying them."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tomllib
from typing import Any


SCHEMA_VERSION = 1
WEIRDNESS_LEVELS = {"grounded", "weird", "unhinged"}
DIAL_FIELDS = ("warmth", "wit", "bluntness", "energy", "brevity")
REQUIRED_FIELDS = {
    "schema_version",
    "name",
    "description",
    "weirdness",
    *DIAL_FIELDS,
}


class CardValidationError(ValueError):
    """Raised when a Banter Card fails schema validation."""

    def __init__(self, errors: list[str]) -> None:
        super().__init__("; ".join(errors))
        self.errors = errors


def _has_control_characters(value: str) -> bool:
    return any(ord(character) < 32 for character in value)


def validate_card(card: Any) -> dict[str, Any]:
    """Return a normalized card or raise CardValidationError."""

    if not isinstance(card, dict):
        raise CardValidationError(["card root must be a TOML table"])

    errors: list[str] = []
    keys = set(card)
    missing = sorted(REQUIRED_FIELDS - keys)
    unknown = sorted(keys - REQUIRED_FIELDS)

    if missing:
        errors.append(f"missing fields: {', '.join(missing)}")
    if unknown:
        errors.append(f"unknown fields: {', '.join(unknown)}")

    version = card.get("schema_version")
    if type(version) is not int or version != SCHEMA_VERSION:
        errors.append("schema_version must be the integer 1")

    for field, maximum in (("name", 40), ("description", 160)):
        value = card.get(field)
        if not isinstance(value, str):
            errors.append(f"{field} must be a string")
            continue
        stripped = value.strip()
        if not stripped:
            errors.append(f"{field} must not be empty")
        elif len(stripped) > maximum:
            errors.append(f"{field} must be at most {maximum} characters")
        if _has_control_characters(value):
            errors.append(f"{field} must not contain control characters")

    weirdness = card.get("weirdness")
    if weirdness not in WEIRDNESS_LEVELS:
        errors.append("weirdness must be grounded, weird, or unhinged")

    for field in DIAL_FIELDS:
        value = card.get(field)
        if type(value) is not int or not 0 <= value <= 5:
            errors.append(f"{field} must be an integer from 0 to 5")

    if errors:
        raise CardValidationError(errors)

    return {
        "schema_version": SCHEMA_VERSION,
        "name": card["name"].strip(),
        "description": card["description"].strip(),
        "weirdness": card["weirdness"],
        **{field: card[field] for field in DIAL_FIELDS},
    }


def load_and_validate(path: Path) -> dict[str, Any]:
    """Load and validate a Banter Card from disk."""

    with path.open("rb") as card_file:
        return validate_card(tomllib.load(card_file))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cards", nargs="+", type=Path, help="Banter Card TOML files")
    parser.add_argument(
        "--json",
        action="store_true",
        help="print machine-readable validation results",
    )
    args = parser.parse_args()

    results: list[dict[str, Any]] = []
    failed = False

    for path in args.cards:
        try:
            card = load_and_validate(path)
            results.append({"path": str(path), "valid": True, "card": card})
        except (OSError, tomllib.TOMLDecodeError, CardValidationError) as error:
            failed = True
            if isinstance(error, CardValidationError):
                errors = error.errors
            else:
                errors = [str(error)]
            results.append({"path": str(path), "valid": False, "errors": errors})

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for result in results:
            if result["valid"]:
                print(f"VALID: {result['path']}")
            else:
                print(f"INVALID: {result['path']}")
                for error in result["errors"]:
                    print(f"  - {error}")

    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
