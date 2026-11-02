import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1] / 'tools'
sys.path.insert(0, str(TOOLS))
import steam_upload as upload

class FakeSteam:
    def __init__(self, owner=True, changed=False):
        self.owner, self.changed, self.calls, self.submitted = owner, changed, [], False
    def query(self, lang):
        if not self.owner:
            raise RuntimeError('Item identity, game or signed-in owner does not match')
        return {'title': 'title', 'description': 'body', 'visibility': 1 if self.submitted and self.changed else 0,
                'cover': 'cover', 'previews': []}
    def ug(self, name, *args):
        self.calls.append(name)
        return 1
    def submit(self, handle, notes):
        self.submitted = True
        return 1

class UploadGuards(unittest.TestCase):
    def test_owner_mismatch_prevents_any_write(self):
        steam = FakeSteam(owner=False)
        with self.assertRaises(RuntimeError):
            upload.perform_upload(steam, Path('/release'), '1.0.8', {}, lambda: None)
        self.assertEqual(steam.calls, [])
        self.assertFalse(steam.submitted)
    def test_only_content_is_staged_and_metadata_checked(self):
        steam, record = FakeSteam(), {}
        upload.perform_upload(steam, Path('/release'), '1.0.8', record, lambda: None)
        self.assertEqual(steam.calls, ['StartItemUpdate', 'SetItemContent'])
        self.assertEqual(record['result'], 1)
        self.assertTrue(record['metadata_unchanged'])
    def test_unexpected_visibility_change_is_not_success(self):
        record = {}
        with self.assertRaisesRegex(RuntimeError, 'visibility'):
            upload.perform_upload(FakeSteam(changed=True), Path('/release'), '1.0.8', record, lambda: None)
        self.assertNotIn('metadata_unchanged', record)
    def test_version_mismatch_prevents_build_or_upload(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'project.json').write_text(json.dumps({'version':'1.0.7'}))
            with patch.object(upload.build, 'verify_build') as verify:
                with self.assertRaisesRegex(ValueError, 'differs'):
                    upload.check_release(root, '1.0.8')
                verify.assert_not_called()
    def test_unsafe_version_rejected(self):
        for version in ['../1.0.7', 'v1.0.7', '1.0.7-beta']:
            with self.assertRaises(ValueError):
                upload.check_release(Path('/unused'), version)

if __name__ == '__main__':
    unittest.main()
