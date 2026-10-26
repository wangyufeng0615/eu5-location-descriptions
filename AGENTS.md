# EU5 创意工坊发布工程

本目录是独立的发布工程，负责 GitHub 源目录、构建、工坊素材和发布维护。先读 [docs/STRUCTURE.md](docs/STRUCTURE.md) 和 [docs/PUBLISHING.md](docs/PUBLISHING.md)。

当前显示名为 **Location Descriptions for Every Tile**，中文“全地图地点介绍”。用户要求封面朴素、实用，避免书卷场景、金色装饰、立体微缩景观等繁复画风。不要恢复已被替换的旧封面；内部mod ID保留 `location_descriptions_enhanced`。

- 原始研究工程位于相邻 `../eu5-location-descriptions/`；数据库、资料缓存、写作批次和历史报告留在那里，不复制进本工程。
- `data/` 是从原工程冻结快照导入的双语正文、来源和保护集合。正文修订先回原工程，再单向导入；不直接另写一套、不自动提升审核状态。当前 28,449 个地点双语首稿，官方124个地点受保护，独立事实核验未完成。
- 正文PR只作为提案，采纳后由维护者先回写研究主库并导出，不直接将外部PR当作新的内容权威。玩家可用任一首发语言反馈，不强制内部ID；详见CONTRIBUTING.md及CONTRIBUTING.zh-CN.md。
- README、发布说明、版本、构建工具、测试和工坊素材以本目录为维护入口。原工程 `packaging/public/` 及历史 `dist/github-preview-*` 不再作为活动模板。
- `dist/` 为生成运行包、ZIP及验收记录，不提交Git。工坊只上传其中实际模组文件夹，不能上传整个工程。
- 本地检查：`python -B tools/build.py --check`，`python -B -m unittest discover -s tests -v`；构建用 `python -B tools/build.py --output dist/<新的目录名>`，不得覆盖旧产物。
- GitHub目标为 `wangyufeng0615/eu5-location-descriptions`，仓库已按用户2026-10-26授权私有创建并上传，仅含本发布工程，使用独立main历史。按用户安排，游戏与工坊验收完成后再公开；当前验收未完成，不得提前更改可见性。正文包未安装、工坊未上传。用户已选择工具MIT、介绍CC BY-SA 4.0；真实游戏截图/验收、第三方特殊声明检查和首次订阅验收待处理，推送核验状态见 [docs/RELEASE_READINESS.md](docs/RELEASE_READINESS.md)。
- 当前候选 `dist/release-candidate-20261026-en-zh-final/`，首发资料包 `dist/launch-pack-20261026-en-zh-final/`；英文和简体中文同条目、同运行包。用 `tools/build.py --verify` 和 `tools/preflight.py --build` 检查，人工证据通过 `--evidence` 绑定实际包和证据文件哈希。此前候选保留历史。预检不代表公开上线，不将封面当游戏截图，不自动接受账号条款或更改可见性。
- 不使用Computer Use／Computer User；不写入账号密码或token，不自动上传、安装或更改外部可见性。
