# Repository structure / 目录结构

This repository builds and publishes the mod. The descriptions themselves are written and checked in a separate research ledger and exported here one way.

本仓库负责构建和发布模组。介绍正文在单独维护的研究库里撰写和核对，单向导出到这里。

```text
data/            exported English/Chinese descriptions, per-location sources, vanilla protection set
                 研究库导出的双语正文、来源和官方保护集合（不手改）
tools/           build.py, preflight.py, release.py, steam_page.py, find_location.py
tests/           unit tests for the tools
workshop/        Workshop page text, covers, screenshots, badges, tooltip GUI override
                 工坊页面文案、封面、截图、徽章和提示框界面文件
docs/            FAQ, compatibility, publishing and maintenance notes
project.json     name, version and mod metadata
dist/            build output, ignored by Git / 构建产物，不提交
```

| Content / 内容 | Maintained in / 维护位置 | How it reaches the package / 如何进入发布包 |
|---|---|---|
| Location descriptions and sources / 地点正文和来源 | research ledger / 研究库 | exported to `data/`, then built |
| Name, version, README, changelog / 名称、版本、说明 | this repository / 本仓库 | edited here |
| Workshop page and artwork / 工坊页面和素材 | `workshop/` | uploaded with `tools/steam_page.py` or by hand |
| Player README, FAQ, compatibility notes / 玩家文档 | `workshop/player-readme.*.md`, `docs/` | copied into the package by `tools/build.py` |
| Tooltip GUI override / 提示框界面 | `workshop/gui/` | copied into `in_game/gui/` |

The build needs only Python's standard library and the committed `data/`; the game is not required. The preflight check can optionally compare against an installed game with `--game-root`.

构建只需要 Python 标准库和仓库里的 `data/`，不需要安装游戏。预检可以加 `--game-root` 对照本地游戏文件。
