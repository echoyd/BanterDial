from __future__ import annotations

from pathlib import Path
import re
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SKILL_PATH = (
    PROJECT_ROOT
    / "plugins"
    / "banter-dial"
    / "skills"
    / "banter-dial"
    / "SKILL.md"
)
MODES_PATH = SKILL_PATH.parent / "references" / "modes.md"
OPENAI_YAML_PATH = SKILL_PATH.parent / "agents" / "openai.yaml"


class SkillBudgetTests(unittest.TestCase):
    def test_common_path_stays_compact(self) -> None:
        self.assertLessEqual(len(SKILL_PATH.read_text(encoding="utf-8")), 3000)

    def test_advanced_mode_reference_stays_compact(self) -> None:
        self.assertLessEqual(len(MODES_PATH.read_text(encoding="utf-8")), 1800)

    def test_description_stays_small_and_discriminating(self) -> None:
        skill = SKILL_PATH.read_text(encoding="utf-8")
        match = re.search(r"(?m)^description:\s*(.+)$", skill)
        self.assertIsNotNone(match)
        assert match
        self.assertLessEqual(len(match.group(1)), 220)
        self.assertIn("explicitly invoked", match.group(1))

    def test_implicit_invocation_is_disabled(self) -> None:
        metadata = OPENAI_YAML_PATH.read_text(encoding="utf-8")
        self.assertRegex(metadata, r"(?m)^\s*allow_implicit_invocation:\s*false\s*$")

    def test_simplified_chinese_has_native_three_level_guidance(self) -> None:
        skill = SKILL_PATH.read_text(encoding="utf-8")
        required = [
            "For Simplified Chinese:",
            "translation tone",
            "mock-polite jab",
            "Put the punchline last and stop.",
            "Roast the code, bug, tool, process, or situation",
        ]
        for phrase in required:
            self.assertIn(phrase, skill)

    def test_high_stakes_detour_restores_selected_level(self) -> None:
        skill = SKILL_PATH.read_text(encoding="utf-8")
        self.assertIn("temporarily use effective Grounded style", skill)
        self.assertIn("automatically restore the selected level", skill)


if __name__ == "__main__":
    unittest.main()
