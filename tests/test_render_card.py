from __future__ import annotations

import importlib.util
from pathlib import Path
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from unittest.mock import patch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS_DIR = (
    PROJECT_ROOT
    / "plugins"
    / "banter-dial"
    / "skills"
    / "banter-dial"
    / "scripts"
)
sys.path.insert(0, str(SCRIPTS_DIR))
SCRIPT_PATH = SCRIPTS_DIR / "render_card.py"
SPEC = importlib.util.spec_from_file_location("render_card", SCRIPT_PATH)
assert SPEC and SPEC.loader
RENDERER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDERER)


CARD = {
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


class RenderCardTests(unittest.TestCase):
    def test_rendered_svg_is_valid_xml(self) -> None:
        svg = RENDERER.render_card_svg(CARD)
        ET.fromstring(svg)

    def test_render_contains_card_settings(self) -> None:
        svg = RENDERER.render_card_svg(CARD)
        self.assertIn("Dry Debugger", svg)
        self.assertIn("WEIRD", svg)
        self.assertIn(">5/5<", svg)

    def test_render_escapes_untrusted_text(self) -> None:
        card = dict(CARD, name="A < B & C")
        svg = RENDERER.render_card_svg(card)
        self.assertIn("A &lt; B &amp; C", svg)
        ET.fromstring(svg)

    def test_default_output_keeps_banter_suffix(self) -> None:
        path = Path("dry-debugger.banter.toml")
        self.assertEqual(
            RENDERER.default_output_path(path),
            Path("dry-debugger.banter.svg"),
        )

    def test_malformed_toml_fails_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            card_path = Path(directory) / "broken.banter.toml"
            output_path = Path(directory) / "broken.svg"
            card_path.write_text('name = "unterminated', encoding="utf-8")
            with patch.object(
                sys,
                "argv",
                [
                    "render_card.py",
                    str(card_path),
                    "--output",
                    str(output_path),
                ],
            ):
                result = RENDERER.main()

        self.assertEqual(result, 1)
        self.assertFalse(output_path.exists())


if __name__ == "__main__":
    unittest.main()
