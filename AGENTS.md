# EU5 创意工坊发布工程

本目录是独立的发布工程，负责 GitHub 源目录、构建、工坊素材和发布维护。先读 [docs/STRUCTURE.md](docs/STRUCTURE.md) 和 [docs/PUBLISHING.md](docs/PUBLISHING.md)。

当前显示名为 **Descriptions for Every Tile**，中文“所有地块的描述”。2026-10-31 已公开发布为工坊条目 [3830305546](https://steamcommunity.com/sharedfiles/filedetails/?id=3830305546)，英文和简体中文标题、描述分别填写，截图英文在前。封面同日改用用户在 Codex 里做的四色西西里版（`workshop/assets/`），轮廓版归档在 `dist/artwork-history-20261031-sicily-outline/`，不要恢复旧封面。用户要求页面朴素、简短，只讲每个地块都有介绍、支持英中两种语言、不改官方介绍和玩法；改动说明只写内容更新，封面这类细节不写。内部mod ID保留 `location_descriptions_enhanced`。

- 原始研究工程位于相邻 `../eu5-location-descriptions/`；数据库、资料缓存、写作批次和历史报告留在那里，不复制进本工程。
- `data/` 是从原工程导出的双语正文、来源和保护集合，由原工程 `tools/export_workshop.py` 生成（读游戏当前的地图定义和官方介绍文件，跳过有官方原文和已不在地图上的地点）。正文修订先回原工程，再单向导入；不直接另写一套。2026-10-30 版对应游戏 1.4（build 26300913）：28,254 个地点双语正文，官方 257 个地点受保护；城市已逐项核对事实，其余条目未逐篇独立核验。
- 正文PR只作为提案，采纳后由维护者先回写研究主库并导出，不直接将外部PR当作新的内容权威。玩家可用任一首发语言反馈，不强制内部ID；详见CONTRIBUTING.md及CONTRIBUTING.zh-CN.md。
- 普通玩家直接在工坊留言区反馈，不要求GitHub或分类讨论。2026-10-31用户授权在双语页面承诺积极维护、查看反馈、持续修正问题并跟进游戏更新；不承诺固定回复期限。按用户要求精简发布工程，不维护本地HTML预览工具或分类讨论模板；页面效果在实际私有工坊条目检查。
- README、发布说明、版本、构建工具、测试和工坊素材以本目录为维护入口。原工程 `packaging/public/` 及历史 `dist/github-preview-*` 不再作为活动模板。
- `dist/` 为生成运行包、ZIP及验收记录，不提交Git。工坊只上传其中实际模组文件夹，不能上传整个工程。
- 本地检查：`python -B tools/build.py --check`，`python -B -m unittest discover -s tests -v`；构建用 `python -B tools/build.py --output dist/<新的目录名>`，不得覆盖旧产物。
- GitHub `wangyufeng0615/eu5-location-descriptions` 只含本发布工程，按用户要求保持私有。Windows 连不上 github.com：推送时在 Windows 打 `git bundle`，拷到能联网的机器克隆、导入、快进推送，再在 Windows 用 `git update-ref refs/remotes/origin/main <sha>` 对齐。用户已选择工具MIT、介绍CC BY-SA 4.0。发布状态见 [docs/RELEASE_READINESS.md](docs/RELEASE_READINESS.md)。
- 当前已发布包为 `dist/release-1.0.0/`（预检 `dist/release-1.0.0-preflight.json`），英文和简体中文同条目、同运行包；`dist/` 只留最新一版和封面历史。文案、截图与封面直接维护在 `workshop/`。更新工坊用游戏内 Mod Tools 的“加载模组”选项卡→“从文件夹上传内容”，路径指向新构建的模组文件夹；不覆盖旧产物，预检不代表线上状态。
- 不使用Computer Use／Computer User；不写入账号密码或token。上传、安装和可见性变更只在用户明确要求时做。
- 项目总览（两个工程、数据流、技术要点、维护流程）和推广文案（Reddit、贴吧、B站脚本）在 Obsidian 笔记库的 生活/游戏/EU5 地块描述 Mod 项目总览.md 与 生活/游戏/EU5 地块描述 Mod 推广文案.md。
