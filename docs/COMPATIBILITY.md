# Compatibility / 兼容性

The mod adds location-description text (`in_game/localization/`) and overrides two vanilla tooltip templates so that seas, lakes and impassable locations show their description (`in_game/gui/zz_lde_location_tooltips.gui`). For the 257 locations with a vanilla description it replaces that key (`in_game/localization/<language>/replace/`) with the vanilla text, unchanged, followed by its own paragraphs. It changes no gameplay, map or names.

本模组只增加地点介绍文本（`in_game/localization/`），并覆盖两个官方提示框模板，让海域、湖泊和不可通行地块也显示介绍（`in_game/gui/zz_lde_location_tooltips.gui`）。官方已有介绍的 257 个地点，用 `in_game/localization/<语言>/replace/` 替换该键，内容是原样保留的官方原文加上本模组补写的段落。不改玩法、地图和地名。

| Combination / 组合 | Status / 状态 |
|---|---|
| Existing saves / 已有存档 | Can be added mid-game / 可以中途加入 |
| Achievements / 成就 | Available. The mod changes the checksum; the game states this affects only multiplayer. Launch options such as `-debug_mode` block achievements regardless of mods. / 可以获得。本模组会改变校验码，游戏说明这只影响联机；`-debug_mode` 等启动选项无论是否开模组都会让成就不可用 |
| Multiplayer / 联机 | Host and all players need the same mods in the same order / 房主和所有玩家需要相同的模组和顺序 |
| [Oikoumene: Dynamic Place Names](https://steamcommunity.com/sharedfiles/filedetails/?id=3721193233) | Both provide English descriptions for 578 of the same locations; Oikoumene's take precedence there / 有 578 个地点重叠，同时启用时优先显示 Oikoumene 的介绍 |
| Other location-description mods / 其他地点介绍模组 | The same keys can be replaced; the later-loaded text wins / 同一个键会被覆盖 |
| Mods that edit the location tooltip / 修改地点提示框的界面模组 | May hide the description block or override the sea/lake/impassable templates / 可能隐藏介绍或覆盖海域、湖泊、不可通行地块的模板 |
| Map overhauls / 地图大修 | Location IDs may differ; descriptions can land on the wrong places / 地点 ID 可能不同，介绍会对不上 |
| Translation bundles / 汉化合集 | May replace the same Chinese keys; this mod already includes Simplified Chinese / 可能覆盖同一中文键；本模组已内置简中 |

If another mod replaces only the English descriptions, the Chinese text from this mod can describe the same place differently. Load order does not merge the two languages.

若另一个模组只替换英文，中文仍来自本模组，两种语言可能讲的不是同一套内容。加载顺序不会合并两种语言。
