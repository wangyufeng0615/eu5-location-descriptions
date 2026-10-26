import unittest
from pathlib import Path
import tempfile
from tools.prepare_launch import render_bbcode, prepare


class LaunchCopyTests(unittest.TestCase):
    def test_launch_pack_cannot_pollute_the_game_payload(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            candidate = root / "candidate"
            candidate.mkdir()
            with self.assertRaisesRegex(ValueError, "outside"):
                prepare(root, candidate, candidate / "nested-launch-pack")

    def test_preview_escapes_markup_without_losing_bilingual_text(self):
        result = render_bbcode('[h1]English / 简体中文[/h1]\n<script>alert("x")</script>')
        self.assertIn('<h1>English / 简体中文</h1>', result)
        self.assertNotIn('<script>', result)
        self.assertIn('&lt;script&gt;', result)

    def test_preview_rejects_invalid_bbcode(self):
        with self.assertRaises(ValueError):
            render_bbcode('[h1]unclosed')


if __name__ == "__main__":
    unittest.main()
