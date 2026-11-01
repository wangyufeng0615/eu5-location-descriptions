import unittest
from unittest.mock import Mock
from tools.steam_page import Steam, B, U64, U32


class GallerySafetyTests(unittest.TestCase):
    def test_refuses_to_break_either_language_body_image(self):
        steam = Steam.__new__(Steam)
        steam.ug = Mock()
        before = {'previews': [{'file':'badges.zh-CN.png', 'url':'https://example.test/chinese.png', 'index':6, 'type':0}]}
        with self.assertRaisesRegex(RuntimeError, 'independent hosting'):
            steam.clean_gallery(before, ['English description', '[img]https://example.test/chinese.png[/img]'])
        steam.ug.assert_not_called()

    def test_removes_only_badges_in_descending_index_order(self):
        steam = Steam.__new__(Steam)
        steam.ug = Mock(return_value=123)
        steam.submit = Mock()
        before = {'previews': [
            {'file':'screenshot.png', 'url':'https://example.test/game.png', 'index':0, 'type':0},
            {'file':'badges.en.png', 'url':'https://example.test/old-en.png', 'index':5, 'type':0},
            {'file':'badges.zh-CN.png', 'url':'https://example.test/old-zh.png', 'index':6, 'type':0}]}
        steam.clean_gallery(before, ['[img]https://example.test/independent.png[/img]'])
        removed = [c.args[-1] for c in steam.ug.call_args_list if c.args[0]=='RemoveItemPreview']
        self.assertEqual(removed, [6,5])
        steam.submit.assert_called_once_with(123)


class ChangeNoteTests(unittest.TestCase):
    def test_change_note_submits_text_without_setting_fields(self):
        steam = Steam.__new__(Steam)
        steam.ug = Mock(return_value=77)
        steam.submit = Mock()
        steam.change_note("  1.0.6\n\n- Fixed ten locations.  ")
        names = [c.args[0] for c in steam.ug.call_args_list]
        self.assertEqual(names, ['StartItemUpdate'])
        steam.submit.assert_called_once_with(77, "1.0.6\n\n- Fixed ten locations.")

    def test_empty_change_note_is_refused(self):
        steam = Steam.__new__(Steam)
        steam.ug = Mock()
        with self.assertRaises(ValueError):
            steam.change_note("   ")
        steam.ug.assert_not_called()


class SubmitResultTests(unittest.TestCase):
    def make(self, code):
        from tools.steam_page import UpdateResult, ITEM
        steam = Steam.__new__(Steam)
        steam.ug = Mock(return_value=1)
        res = UpdateResult(); res.result = code; res.agreement = False; res.item = ITEM
        steam.wait = Mock(return_value=res)
        return steam

    def test_failed_submit_raises(self):
        with self.assertRaisesRegex(RuntimeError, 'Steam result 2'):
            self.make(2).submit(5, "note")

    def test_ok_submit_returns_ok(self):
        self.assertEqual(self.make(1).submit(5, "note"), 1)
