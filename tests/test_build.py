from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SPEC = importlib.util.spec_from_file_location("mod_build", Path(__file__).resolve().parents[1] / "tools/build.py")
mod_build = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(mod_build)


class BuildGuards(unittest.TestCase):
    def fixture(self, root, rows):
        config = json.loads((Path(__file__).resolve().parents[1] / "project.json").read_text(encoding="utf-8"))
        mod_build.write_json(root / "project.json", config)
        mod_build.write_json(root / "data/baseline.json", {"target_ids": ["test_town"], "protected_ids": ["official_town"], "map_location_count": 2, "steam_build_id": "1"})
        path = root / "data/descriptions/001.jsonl"
        path.parent.mkdir(parents=True)
        path.write_text("\n".join(json.dumps(row) for row in rows), encoding="utf-8")
        for name in ("CREDITS.md", "NOTICE.md", *mod_build.LICENSE_FILES):
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("Fixture attribution and license\n", encoding="utf-8")
        for name in mod_build.PLAYER_DOCUMENTS.values():
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("Fixture player guide\n", encoding="utf-8")
        thumbnail = root / config["thumbnail_file"]
        thumbnail.parent.mkdir(parents=True, exist_ok=True)
        thumbnail.write_bytes(b"test image bytes")

    def row(self, key="test_town"):
        return {"id": key, "english": "A town beside the river.", "simp_chinese": "河边的小镇。", "review_status": "bilingual_first_pass", "sources": [{"title": "Example", "url": "https://en.wikipedia.org/wiki/Example", "revision_id": 1}]}

    def test_rejects_official_override(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root, [self.row("official_town")])
            with self.assertRaisesRegex(ValueError, "official"):
                mod_build.load(root)

    def test_rejects_duplicate(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root, [self.row(), self.row()])
            with self.assertRaisesRegex(ValueError, "Duplicate"):
                mod_build.load(root)

    def test_rejects_missing_source_and_missing_translation(self):
        for field, value in (("sources", []), ("simp_chinese", "")):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                row = self.row()
                row[field] = value
                self.fixture(root, [row])
                with self.assertRaises(ValueError):
                    mod_build.load(root)

    def test_rejects_bad_source(self):
        for field, value, message in (("url", "ftp://example.org/x", "Unexpected source URL"), ("title", "", "Untitled"), ("revision_id", -1, "Invalid source revision")):
            with self.subTest(field=field), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                row = self.row()
                row["sources"][0][field] = value
                self.fixture(root, [row])
                with self.assertRaisesRegex(ValueError, message):
                    mod_build.load(root)

    def test_accepts_unpinned_non_wikipedia_source(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            row = self.row()
            row["sources"] = [{"title": "Gazetteer", "url": "http://dfz.example.gov.cn/page"}]
            self.fixture(root, [row])
            self.assertEqual(len(mod_build.load(root)[2]), 1)

    def test_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root, [self.row()])
            with self.assertRaises(FileExistsError):
                mod_build.build(root, root)

    def test_yaml_escaping(self):
        self.assertEqual(mod_build.quote('A "port"\\river\nNext'), 'A \\"port\\"\\\\river\\nNext')

    def test_rejects_path_traversal_in_mod_identity(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root, [self.row()])
            config = json.loads((root / "project.json").read_text())
            config["mod_id"] = "../../escape"
            mod_build.write_json(root / "project.json", config)
            with self.assertRaisesRegex(ValueError, "identity"):
                mod_build.load(root)

    def test_rejects_duplicate_protected_ids(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root, [self.row()])
            baseline = json.loads((root / "data/baseline.json").read_text())
            baseline["protected_ids"].append("official_town")
            mod_build.write_json(root / "data/baseline.json", baseline)
            with self.assertRaisesRegex(ValueError, "baseline"):
                mod_build.load(root)

    def test_roundtrip_and_reproducible_archive(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root, [self.row()])
            first = mod_build.build(root, root / "dist/first")
            second = mod_build.build(root, root / "dist/second")
            self.assertEqual(first["archive_sha256"], second["archive_sha256"])
            self.assertEqual(mod_build.verify_build(root, root / "dist/first"), first)

    def test_rejects_modified_text_and_unexpected_payload(self):
        for tamper in ("text", "extra"):
            with self.subTest(tamper=tamper), tempfile.TemporaryDirectory() as temporary:
                root = Path(temporary)
                self.fixture(root, [self.row()])
                mod_build.build(root, root / "dist/test")
                mod = root / "dist/test/location_descriptions_enhanced"
                if tamper == "text":
                    target = mod / "main_menu/localization/english/lde_001_l_english.yml"
                    original = target.read_bytes()
                    self.assertIn(b"river", original)
                    modified = original.replace(b"river", b"ocean")
                    self.assertNotEqual(original, modified)
                    target.write_bytes(modified)
                else:
                    (mod / "unexpected.exe").write_bytes(b"extra")
                with self.assertRaises(ValueError):
                    mod_build.verify_build(root, root / "dist/test")

    def test_rejects_tampered_zip(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            self.fixture(root, [self.row()])
            mod_build.build(root, root / "dist/test")
            archive = next((root / "dist/test").glob("*.zip"))
            with archive.open("ab") as stream:
                stream.write(b"tampered")
            with self.assertRaisesRegex(ValueError, "Archive hash"):
                mod_build.verify_build(root, root / "dist/test")


if __name__ == "__main__":
    unittest.main()
