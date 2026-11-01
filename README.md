# Descriptions for Every Tile / 所有地块的描述

**[English](#english) · [简体中文](#简体中文)**

![Mod cover](workshop/assets/cover.jpg)

## English

Historical and geographical descriptions for the places EU5 leaves blank. English and Simplified Chinese are included in the same mod.

Game version 1.4 has 28,573 locations. This mod adds descriptions to the 28,316 without vanilla text and leaves the 257 existing vanilla descriptions alone. Coverage includes cities, towns, countryside, mountains, sea zones and lakes.

### Getting started

Subscribe on the Steam Workshop, wait for the download to finish, then enable the mod in EU5's Mods and DLC menu. Set the game language to English or Simplified Chinese. You do not need a separate Chinese translation mod.

Prefer not to use the Workshop? Download the ZIP from [Releases](https://github.com/wangyufeng0615/eu5-location-descriptions/releases/latest):

1. Download `location_descriptions_enhanced-<version>.zip`.
2. Extract it into `Documents\Paradox Interactive\Europa Universalis V\mod\`, so that you have `mod\location_descriptions_enhanced\`.
3. Start EU5 and enable **Descriptions for Every Tile** in Mods and DLC.

Use either the Workshop copy or the ZIP copy, not both. To update, delete the old folder and extract the new ZIP.

See the [changelog](CHANGELOG.md) for the current version and what changed.

### What to expect

Some places have a detailed local history; others have a shorter description of the surrounding region, landscape or waterways. The texts were drafted with AI assistance from published sources, mostly Wikipedia in English and the local language, then corrected and checked by the author, a geography enthusiast; city entries were checked fact by fact. Corrections and better local references are welcome.

The mod adds description text. It does not add events, change location names or alter gameplay rules. No other mod or DLC dependency is declared.

### In game

Hover over a location to read its description. Seas, lakes and impassable places have them too.

![Nicusìa town description in English](workshop/screenshots/nicosia.en.png)
![Mount Etna description in English](workshop/screenshots/mount-etna.en.png)

### Compatibility

Made for game version 1.4 (Steam build 26300913). It can be added to an existing save, and achievements stay available. In multiplayer, everyone needs the same mods.

Mods that replace the map or write the same location descriptions can conflict. This includes name/flavour mods that also contain descriptions: load order can give you one mod's English text and another's Chinese text.

See the [FAQ](docs/FAQ.md) and [compatibility notes](docs/COMPATIBILITY.md).

### Help improve a place

Found a wrong date, awkward translation or a place matched to the wrong location? Leave a comment on the Workshop page in English or Chinese. Include the place name; a region, screenshot or source helps, but you do not need all of them or an internal ID.

I'll actively maintain the mod, follow up on feedback, fix problems and keep it up to date as the game changes. You can help without writing code or working in both languages. See [contributing](CONTRIBUTING.md).

### Source and build

The descriptions are written and checked in a separate research ledger and exported into `data/`; neither `data/` nor the generated localization is edited by hand. Source-checkout contributors can use tools/find_location.py to find the right record.

Python 3.10 or newer is enough; no additional packages or game installation are needed to build the frozen content:

    python -B tools/build.py --check
    python -B -m unittest discover -s tests -v
    python -B tools/build.py --output dist/my-candidate
    python -B tools/preflight.py --build dist/my-candidate --output dist/my-check.json

Use a new output directory for each build. The result includes the loadable mod folder, a ZIP and a checksum receipt. Build and publication details are in [PUBLISHING.md](docs/PUBLISHING.md).

### Credits and reuse

New descriptions and translations use **CC BY-SA 4.0**; tools and technical documentation use **MIT**. Keep the per-location source credits, identify changes and follow the applicable share-alike terms. See [LICENSE](LICENSE), [CREDITS.md](CREDITS.md) and [NOTICE.md](NOTICE.md).

The cover is an AI-assisted graphic, not a game screenshot. This is an unofficial community project, with no affiliation to Paradox, Valve or Wikimedia.

## 简体中文

为 EU5 中原本没有介绍的地点补上历史与地理文本。英文、简体中文首发一起提供，订阅同一个模组即可，不需要另装汉化包。

游戏 1.4 版共有 28,573 个地点。本模组为其中没有原版介绍的 28,316 个补上介绍，原版已有的 257 个介绍保持原文。范围包括城市、乡镇、乡村、山地、海域和湖泊。

### 怎么使用

在 Steam 创意工坊订阅，等待下载完成，再到游戏内“模组和 DLC”中启用。游戏语言选择英文或简体中文。

不想用创意工坊，也可以从 [Releases](https://github.com/wangyufeng0615/eu5-location-descriptions/releases/latest) 下载 ZIP：

1. 下载 `location_descriptions_enhanced-<版本号>.zip`。
2. 解压到 `文档\Paradox Interactive\Europa Universalis V\mod\`，解压后应有 `mod\location_descriptions_enhanced\` 文件夹。
3. 启动游戏，在“模组和 DLC”里启用 **所有地块的描述**。

创意工坊版和 ZIP 版二选一，不要同时启用。更新时删掉旧文件夹，再解压新的 ZIP。

当前版本和每次的改动见[更新记录](CHANGELOG.md)。

### 内容是什么样的

资料较充分的地点会介绍当地历史；部分地点只有简短介绍，或采用适用于该地区、地形与水域的背景。正文先以 AI 辅助、依据公开资料（主要是英文和当地语言的维基百科）起草，再由作者（一名地理爱好者）尽可能订正、校验，城市条目逐项核对过年份和人物。欢迎纠错和补充可靠的地方资料。

模组只增加介绍文本，不新增事件、不改地名或玩法数值，也没有声明需要其他模组或额外 DLC。

### 游戏内效果

鼠标悬停在地点上就能看到介绍，海域、湖泊和不可通行地块也有。

![基亚扎的中文介绍](workshop/screenshots/piazza.zh-CN.png)
![埃特纳火山的中文介绍](workshop/screenshots/mount-etna.zh-CN.png)

### 兼容性

适配游戏 1.4 版（Steam build 26300913）。存档可以中途加入，成就照常可以获得；联机时所有玩家需要启用相同的模组。

地图大修、修改同一地点介绍的模组可能冲突。有些地名或风味模组也包含介绍文本，不能仅凭名称判断互不影响。混用时，英文和中文还可能分别来自不同模组。

见[常见问题](docs/FAQ.zh-CN.md)和[兼容性说明](docs/COMPATIBILITY.md)。

### 想帮忙完善

如果发现年代有误、中文不通顺、地点认错，直接在工坊页面留言就好，中英文都可以。请带上地点名称；所在地区、截图和资料链接有的话可以附上，不知道内部 ID 也没关系。

我会积极维护这个模组，认真查看反馈，持续修正问题并跟进游戏更新。不需要会写代码，也不要求一次把两种语言都改完。具体方式见[贡献指南](CONTRIBUTING.zh-CN.md)。

### 源码与构建

正文在单独维护的研究库里撰写和核对，再导出到 `data/`；不要手改 `data/` 或生成的本地化文件。使用源码的贡献者可以通过 tools/find_location.py 查找地点记录。

Python 3.10 以上即可构建当前冻结内容，无需游戏或额外依赖：

    python -B tools/build.py --check
    python -B -m unittest discover -s tests -v
    python -B tools/build.py --output dist/my-candidate
    python -B tools/preflight.py --build dist/my-candidate --output dist/my-check.json

每次构建使用新的输出目录，产物包含运行文件夹、ZIP 和哈希回执。发布操作见 [PUBLISHING.md](docs/PUBLISHING.md)。

### 来源与许可

新增介绍和翻译采用 **CC BY-SA 4.0**，工具及技术文档采用 **MIT**。再利用时请保留逐地点来源归属、标明修改，并遵守适用的相同方式共享要求。范围见 [LICENSE](LICENSE)、[CREDITS.md](CREDITS.md)及 [NOTICE.md](NOTICE.md)。

封面是 AI 辅助生成的图形，不是游戏截图。本项目为非官方社区模组，与 Paradox、Valve、Wikimedia 没有关联。
