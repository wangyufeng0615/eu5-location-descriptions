from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("mod_release", Path(__file__).resolve().parents[1] / "tools/release.py")
release = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(release)


class VersionAndChangelog(unittest.TestCase):
    def test_plain_versions_only(self):
        self.assertEqual(release.parse_version("1.0.12"), (1, 0, 12))
        for bad in ("1.0", "1.0.0-beta", "v1.0.0", "1.0.0.1", " 1.0.0"):
            with self.assertRaises(ValueError):
                release.parse_version(bad)

    def test_commit_subject_is_first_sentence(self):
        note = "Fix Wuchang: the game's Wuchang is modern Ezhou. It now covers Sun Quan's capital."
        self.assertEqual(release.commit_subject(note), "Fix Wuchang")
        self.assertEqual(release.commit_subject("Fix the pigment name in Wallerfangen."), "Fix the pigment name in Wallerfangen")
        self.assertLessEqual(len(release.commit_subject("x" * 200)), 72)

    def test_numeric_ordering(self):
        self.assertGreater(release.parse_version("1.0.10"), release.parse_version("1.0.9"))

    def test_set_project_version_keeps_formatting(self):
        text = '{\n  "name": "x",\n  "version": "1.0.4",\n  "tags": []\n}\n'
        self.assertEqual(release.set_project_version(text, "1.0.4", "1.0.5"), text.replace("1.0.4", "1.0.5"))
        with self.assertRaises(ValueError):
            release.set_project_version(text, "1.0.3", "1.0.5")

    def test_changelog_entry_goes_first(self):
        text = "# Changelog\n\n## 1.0.4 — 2026-11-01\n\n- Old.\n"
        result = release.add_changelog_entry(text, "1.0.5", "2026-11-02", ["First.", "Second."])
        self.assertTrue(result.startswith("# Changelog\n\n## 1.0.5 — 2026-11-02\n\n- First.\n- Second.\n\n## 1.0.4"))

    def test_changelog_rejects_duplicates_and_empty_notes(self):
        text = "# Changelog\n\n## 1.0.5 — 2026-11-01\n\n- Old.\n"
        with self.assertRaises(ValueError):
            release.add_changelog_entry(text, "1.0.5", "2026-11-02", ["New."])
        with self.assertRaises(ValueError):
            release.add_changelog_entry("# Changelog\n\n", "1.0.6", "2026-11-02", [])
        with self.assertRaises(ValueError):
            release.add_changelog_entry("# Changelog\n\n", "1.0.6", "2026-11-02", ["  "])


class Mirror(unittest.TestCase):
    def make_mod(self, root: Path, body: str) -> Path:
        (root / ".metadata").mkdir(parents=True)
        (root / ".metadata" / "metadata.json").write_text(json.dumps({"id": release.MOD_ID}), encoding="utf-8")
        (root / "a.txt").write_text(body, encoding="utf-8")
        return root

    def test_replaces_an_existing_copy_of_this_mod(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_mod(Path(tmp) / "build", "new")
            target = self.make_mod(Path(tmp) / "installed", "old")
            (target / "stale.txt").write_text("gone", encoding="utf-8")
            release.mirror(source, target)
            self.assertEqual(release.tree_hashes(source), release.tree_hashes(target))

    def test_refuses_to_replace_another_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            source = self.make_mod(Path(tmp) / "build", "new")
            other = Path(tmp) / "someone-else"
            other.mkdir()
            (other / "keep.txt").write_text("keep", encoding="utf-8")
            with self.assertRaises(ValueError):
                release.mirror(source, other)
            self.assertTrue((other / "keep.txt").exists())


if __name__ == "__main__":
    unittest.main()
