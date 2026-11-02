# Descriptions for Every Tile：发布工程

本仓库把 EU5 地点介绍打包成创意工坊模组（工坊条目 [3830305546](https://steamcommunity.com/sharedfiles/filedetails/?id=3830305546)，英文名 **Descriptions for Every Tile**，中文名“所有地块的描述”，内部 mod ID `location_descriptions_enhanced`）。目录结构见 [docs/STRUCTURE.md](docs/STRUCTURE.md)，发布步骤见 [docs/PUBLISHING.md](docs/PUBLISHING.md)。

## 内容从哪里来

- `data/` 是导出结果：双语正文、每个地点的来源和官方保护集合，由单独维护的研究库单向导出。不要手改 `data/`，也不要手改构建出的本地化文件；正文修改先在研究库完成，再重新导出。
- 外部提交的正文修改只当提案。采纳后由维护者回写研究库、重新导出，再进入这里。
- 跳过的地点：游戏已有官方介绍的（当前 257 个）保持原文，导出时跳过。

## 本地检查与构建

```
python -B tools/build.py --check
python -B -m unittest discover -s tests -v
python -B tools/build.py --output dist/<新目录>
python -B tools/build.py --verify dist/<新目录>
python -B tools/preflight.py --build dist/<新目录> --output dist/<新目录>-preflight.json
```

- 只用 Python 标准库，3.10 及以上即可，不需要游戏。
- 构建和预检的输出目录每次用新的，不覆盖旧产物。`dist/` 不提交。
- 正式发版用 `python -B tools/release.py <x.y.z> --note "<英文更新说明>"`，它会升版本、写 CHANGELOG、跑完上面的检查并构建到 `dist/release-x.y.z/`，详见 PUBLISHING。

## 版本和上传

- 版本号一律 `x.y.z`，不加后缀；`tools/build.py` 拒绝其他写法。每次上传工坊前先升版本，更新记录写在 `CHANGELOG.md`。
- 上传工坊只传构建出的模组文件夹 `location_descriptions_enhanced/`（含隐藏的 `.metadata/`），不能传整个仓库或 `dist/`。用游戏模组工具上传时填这个文件夹的完整路径。
- 用户要求发版时，默认用 `tools/steam_upload.py --upload` 在已登录 Steam 的 Windows 桌面会话更新既有条目；先完成本地检查并保留上传记录，步骤见 `docs/PUBLISHING.md`。EU5 模组工具作为备用。创建条目、订阅、可见性变更、接受条款和账号权限变更不包含在发版授权内，仍由作者处理。

## 工坊页面

- 页面文案、封面和截图在 `workshop/`。英文 `description.en.txt`、中文 `description.zh-CN.txt`、合并版 `description.default.txt` 要一起改。
- `tools/steam_page.py` 通过正在运行的 Steam 客户端修改已有条目：不带参数时只读；写入必须显式加 `--descriptions`、`--assets` 等参数，每次用新的 `--output` 记录文件。它必须在登录了 Steam 的桌面会话里运行。
- 实测过的坑：只更新描述会清空中文标题，所以每种语言的标题和描述要一起提交（工具已这样做）；删除画廊图片会让引用它的旧链接失效。正文里的徽章图托管在 Steam 云文件上，文件名记在 `workshop/page.json`，不要删除这些云文件。
- 不用工具修改可见性、创建新条目或接受条款。

## 写作风格

页面和文档保持朴素、简短；更新说明只写内容变化，封面等细节不写。
