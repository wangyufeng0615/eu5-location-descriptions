# Compatibility / 兼容性

Checked documentation and local package baseline: 2026-10-26. This table separates file-level reasoning from actual game tests. It is not a tested-mod whitelist.

以下按文件职责判断潜在冲突，不代表已逐一进游戏验证。

| Combination / 组合 | Status / 状态 | Guidance / 建议 |
|---|---|---|
| Vanilla map, build 24187685 / 原版地图 | Seven source fingerprints match; runtime pending / 7份源指纹一致，实机待验收 | First test this combination / 首先验收此组合 |
| Other location-description mods / 其他地点介绍模组 | Possible same-key overlap / 可能同键覆盖 | Use one description set pending a patch / 暂用一套介绍 |
| Oikoumene: Dynamic Place Names | Its author also lists description content; combination not tested / 作者列有地点介绍，组合未测试 | Check English and Chinese together, not just names / 同时核对英中介绍，不只看地名 |
| Map overhauls / 地图大修 | IDs and location scope may differ / ID和地理范围可能变化 | Requires explicit mapping and protection review / 需要重新映射并核对官方保护 |
| UI, road or portrait mods / UI、道路和肖像模组 | No compatibility certification / 尚未认证 | No declared dependency; report actual UI or load conflicts / 无声明依赖，按实测反馈 |
| Translation bundles / 汉化合集 | May replace the same Chinese keys / 可能覆盖同一中文键 | This mod already includes Simplified Chinese / 本模组已内置简中 |
| Achievements, saves, multiplayer, other OS / 成就、存档、联机、其他系统 | Not yet confirmed / 尚未确认 | No blanket claim from “text only” / 不以“纯文本”代替测试 |

If another mod replaces only English descriptions, it can leave Chinese showing a different set of facts. A later load position is not a bilingual merge. An eventual patch must retain location identity, the official protection set and agreement between the languages.

若另一个模组只替换英文，中文可能继续显示另一套事实。加载顺序不会自动合并双语内容；兼容补丁必须同时核对地点身份、官方保护集合及英中事实对应。

The Oikoumene author's page explicitly includes city flavour descriptions and describes same-content load-order conflicts: [Workshop page](https://steamcommunity.com/sharedfiles/filedetails/?id=3721193233). This reference is evidence of potential overlap, not a claim that we tested its files or obtained a collaboration agreement.

Oikoumene 的作者页面明确列有城市介绍并说明同类内容会受顺序影响。这里据此提示重叠风险，没有声称测试过对方文件或已经达成合作。
