# EU5 创意工坊发布工程

本目录是独立的发布工程，负责 GitHub 源目录、构建、工坊素材和发布维护。先读 [docs/STRUCTURE.md](docs/STRUCTURE.md) 和 [docs/PUBLISHING.md](docs/PUBLISHING.md)。

当前显示名为 **Descriptions for Every Tile**，中文“所有地块的描述”。2026-10-31用户选定西西里岛轮廓版双语封面，英文突出EVERY TILE，中文突出所有地块。主封面与包内缩略图用英文，中文README和配套发布素材用中文版。用户要求朴素、实用，避免繁复画风；不要恢复旧封面。内部mod ID保留 `location_descriptions_enhanced`。

- 原始研究工程位于相邻 `../eu5-location-descriptions/`；数据库、资料缓存、写作批次和历史报告留在那里，不复制进本工程。
- `data/` 是从原工程导出的双语正文、来源和保护集合，由原工程 `tools/export_workshop.py` 生成（读游戏当前的地图定义和官方介绍文件，跳过有官方原文和已不在地图上的地点）。正文修订先回原工程，再单向导入；不直接另写一套。2026-10-30 版对应游戏 1.4（build 26300913）：28,254 个地点双语正文，官方 257 个地点受保护；城市已逐项核对事实，其余条目未逐篇独立核验。
- 正文PR只作为提案，采纳后由维护者先回写研究主库并导出，不直接将外部PR当作新的内容权威。玩家可用任一首发语言反馈，不强制内部ID；详见CONTRIBUTING.md及CONTRIBUTING.zh-CN.md。
- 普通玩家直接在工坊留言区反馈，不要求GitHub或分类讨论。2026-10-31用户授权在双语页面承诺积极维护、查看反馈、持续修正问题并跟进游戏更新；不承诺固定回复期限。按用户要求精简发布工程，不维护本地HTML预览工具或分类讨论模板；页面效果在实际私有工坊条目检查。
- README、发布说明、版本、构建工具、测试和工坊素材以本目录为维护入口。原工程 `packaging/public/` 及历史 `dist/github-preview-*` 不再作为活动模板。
- `dist/` 为生成运行包、ZIP及验收记录，不提交Git。工坊只上传其中实际模组文件夹，不能上传整个工程。
- 本地检查：`python -B tools/build.py --check`，`python -B -m unittest discover -s tests -v`；构建用 `python -B tools/build.py --output dist/<新的目录名>`，不得覆盖旧产物。
- GitHub目标为 `wangyufeng0615/eu5-location-descriptions`，仓库已按用户2026-10-26授权私有创建并上传，仅含本发布工程，使用独立main历史。按用户安排，游戏与工坊验收完成后再公开；当前验收未完成，不得提前更改可见性。正文包未安装、工坊未上传。用户已选择工具MIT、介绍CC BY-SA 4.0；真实游戏截图/验收、第三方特殊声明检查和首次订阅验收待处理，推送核验状态见 [docs/RELEASE_READINESS.md](docs/RELEASE_READINESS.md)。
- 当前候选 `dist/release-candidate-20261031-1.0.0-final/`，其下保留 `private-test.local.vdf` 和 `release-evidence.json`；英文和简体中文同条目、同运行包。文案与封面直接维护在 `workshop/`，不再生成重复首发资料包。2026-10-31已接入双语封面与显示名，并补使用方法、留言入口和维护承诺，未修改词条、安装或上传。用 `tools/build.py --verify` 和 `tools/preflight.py --build` 检查，人工证据通过 `--evidence` 绑定实际包和证据文件哈希。此前候选保留历史。预检不代表公开上线，不将封面当游戏截图，不自动接受账号条款或更改可见性。
- 不使用Computer Use／Computer User；不写入账号密码或token，不自动上传、安装或更改外部可见性。
