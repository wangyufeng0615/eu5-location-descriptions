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
