from pathlib import Path
import struct
import tempfile
import unittest
import re
import json
import hashlib
from tools import preflight


class PreflightTests(unittest.TestCase):
    def test_first_release_language_mapping_cannot_drop_chinese(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "mapping"):
                preflight.check_launch_materials(Path(directory), {"game_languages": {"english": "english"}})

    def test_absent_manual_evidence_keeps_release_pending(self):
        result = preflight.check_release_evidence(None, {})
        self.assertFalse(result["all_recorded"])
        self.assertEqual(len(result["pending"]), len(preflight.EVIDENCE_CHECKS))

    def test_manual_evidence_is_package_bound_and_files_are_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = root / "test-record.md"
            record.write_text("Synthetic fixture record, not an actual game result.")
            checksum = hashlib.sha256(record.read_bytes()).hexdigest()
            receipt = {"archive_sha256": "a" * 64, "version": "0.2.0-alpha.1", "baseline_build": "1"}
            evidence = {"schema_version": 1, "archive_sha256": receipt["archive_sha256"], "mod_version": receipt["version"], "game_build": "1", "workshop_item_id": "123", "checks": {name: {"status": "passed", "record_file": record.name, "sha256": checksum} for name in preflight.EVIDENCE_CHECKS}}
            path = root / "evidence.json"
            path.write_text(json.dumps(evidence))
            self.assertTrue(preflight.check_release_evidence(path, receipt)["all_recorded"])
            record.write_text("Changed fixture")
            with self.assertRaisesRegex(ValueError, "changed"):
                preflight.check_release_evidence(path, receipt)
            evidence["archive_sha256"] = "b" * 64
            path.write_text(json.dumps(evidence))
            with self.assertRaisesRegex(ValueError, "exact package"):
                preflight.check_release_evidence(path, receipt)

    def test_personal_path_pattern_distinguishes_its_own_source(self):
        self.assertIsNone(re.search(preflight.PERSONAL_PATH_RE, Path(preflight.__file__).read_text(encoding="utf-8")))
        self.assertIsNotNone(re.search(preflight.PERSONAL_PATH_RE, "/" + "Users" + "/tester/file"))

    def test_nested_bbcode_and_unbalanced_rejection(self):
        preflight.check_bbcode("[h1]Title[/h1][i]Text[b]Bold[/b][/i]")
        with self.assertRaises(ValueError):
            preflight.check_bbcode("[h1]Title[/i]")
        with self.assertRaises(ValueError):
            preflight.check_bbcode("[b]Open")

    def test_png_and_jpeg_dimensions(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "test.png"
            path.write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00\x00\x00\x0dIHDR" + struct.pack(">II", 512, 512))
            self.assertEqual(preflight.image_size(path), (512, 512))
            path = Path(directory) / "test.jpg"
            path.write_bytes(b"\xff\xd8\xff\xc0\x00\x11\x08" + struct.pack(">HH", 700, 900) + b"\x00" * 10)
            self.assertEqual(preflight.image_size(path), (900, 700))

    def test_invalid_image(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "invalid.png"
            path.write_bytes(b"not an image")
            with self.assertRaises(ValueError):
                preflight.image_size(path)

    def test_generated_files_excluded_from_source_scan(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "dist").mkdir()
            (root / "dist/cache.txt").write_text("generated")
            (root / "README.md").write_text("source")
            self.assertEqual([p.name for p in preflight.source_files(root)], ["README.md"])


if __name__ == "__main__":
    unittest.main()
