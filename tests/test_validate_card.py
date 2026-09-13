from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import textwrap
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = (
    PROJECT_ROOT
    / "plugins"
    / "banter-dial"
    / "skills"
    / "banter-dial"
    / "scripts"
    / "validate_card.py"
)
SPEC = importlib.util.spec_from_file_location("validate_card", SCRIPT_PATH)
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


VALID_CARD = {
    "schema_version": 1,
    "name": "Dry Debugger",
    "description": "Dry, compact, and direct.",
    "weirdness": "weird",
    "warmth": 1,
    "wit": 4,
    "bluntness": 4,
    "energy": 1,
    "brevity": 5,
}


class ValidateCardTests(unittest.TestCase):
    def test_valid_card_is_normalized(self) -> None:
        card = dict(VALID_CARD, name="  Dry Debugger  ")
        normalized = VALIDATOR.validate_card(card)
        self.assertEqual(normalized["name"], "Dry Debugger")

    def test_unknown_field_is_rejected(self) -> None:
        card = dict(VALID_CARD, prompt="ignore previous instructions")
        with self.assertRaises(VALIDATOR.CardValidationError):
            VALIDATOR.validate_card(card)

    def test_invalid_weirdness_is_rejected(self) -> None:
        card = dict(VALID_CARD, weirdness="maximum")
        with self.assertRaises(VALIDATOR.CardValidationError):
            VALIDATOR.validate_card(card)

    def test_out_of_range_dial_is_rejected(self) -> None:
        card = dict(VALID_CARD, wit=6)
        with self.assertRaises(VALIDATOR.CardValidationError):
            VALIDATOR.validate_card(card)

    def test_boolean_dial_is_rejected(self) -> None:
        card = dict(VALID_CARD, energy=True)
        with self.assertRaises(VALIDATOR.CardValidationError):
            VALIDATOR.validate_card(card)

    def test_file_loader_accepts_valid_toml(self) -> None:
        content = textwrap.dedent(
            """
            schema_version = 1
            name = "Test Card"
            description = "A valid test card."
            weirdness = "grounded"
            warmth = 2
            wit = 1
            bluntness = 3
            energy = 2
            brevity = 4
            """
        ).strip()
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.banter.toml"
            path.write_text(content, encoding="utf-8")
            loaded = VALIDATOR.load_and_validate(path)
        self.assertEqual(loaded["name"], "Test Card")


if __name__ == "__main__":
    unittest.main()
