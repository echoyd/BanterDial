from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ROOT = ROOT / "plugins" / "banter-dial"
MANIFEST_PATH = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"


class PublicPackageTests(unittest.TestCase):
    def test_plugin_manifest(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["name"], "banter-dial")
        self.assertEqual(manifest["version"], "0.2.1")
        self.assertEqual(manifest["skills"], "./skills/")
        self.assertTrue((PLUGIN_ROOT / "skills" / "banter-dial" / "SKILL.md").is_file())

    def test_manifest_assets_exist(self) -> None:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        interface = manifest["interface"]
        paths = [interface["composerIcon"], interface["logo"], *interface["screenshots"]]
        for relative in paths:
            self.assertTrue((PLUGIN_ROOT / relative.removeprefix("./")).is_file(), relative)

    def test_marketplace_points_to_plugin(self) -> None:
        marketplace = json.loads(MARKETPLACE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(marketplace["name"], "banterdial")
        entry = marketplace["plugins"][0]
        self.assertEqual(entry["name"], "banter-dial")
        self.assertEqual(entry["source"]["path"], "./plugins/banter-dial")
        self.assertEqual(entry["policy"]["installation"], "AVAILABLE")


if __name__ == "__main__":
    unittest.main()
