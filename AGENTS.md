# EU5 创意工坊发布工程

本目录是独立的发布工程，负责 GitHub 源目录、构建、工坊素材和发布维护。先读 [docs/STRUCTURE.md](docs/STRUCTURE.md) 和 [docs/PUBLISHING.md](docs/PUBLISHING.md)。

当前显示名为 **Descriptions for Every Tile**，中文“所有地块的描述”。2026-10-31 已公开发布为工坊条目 [3830305546](https://steamcommunity.com/sharedfiles/filedetails/?id=3830305546)，英文和简体中文标题、描述分别填写，截图英文在前。封面采用四色西西里版，左下角English ✓在上、中文 ✓在下；正文分别嵌入精确排版的英中双徽章。现行主图位于 `workshop/assets/`，不恢复旧封面。用户要求页面朴素、简短；改动说明只写内容更新，封面这类细节不写。内部mod ID保留 `location_descriptions_enhanced`。

- 原始研究工程位于相邻 `../eu5-location-descriptions/`；数据库、资料缓存、写作批次和历史报告留在那里，不复制进本工程。
- `data/` 是从原工程导出的双语正文、来源和保护集合，由原工程 `tools/export_workshop.py` 生成（读游戏当前的地图定义和官方介绍文件，跳过有官方原文和已不在地图上的地点）。正文修订先回原工程，再单向导入；不直接另写一套。2026-10-30 版对应游戏 1.4（build 26300913）：28,254 个地点双语正文，官方 257 个地点受保护；城市已逐项核对事实，其余条目未逐篇独立核验。
- 正文PR只作为提案，采纳后由维护者先回写研究主库并导出，不直接将外部PR当作新的内容权威。玩家可用任一首发语言反馈，不强制内部ID；详见CONTRIBUTING.md及CONTRIBUTING.zh-CN.md。
- 普通玩家直接在工坊留言区反馈，不要求GitHub或分类讨论。2026-10-31用户授权在双语页面承诺积极维护、查看反馈、持续修正问题并跟进游戏更新；不承诺固定回复期限。按用户要求精简发布工程，不维护本地HTML预览工具或分类讨论模板；页面效果在实际私有工坊条目检查。
- 徽章只出现在正文，不加入画廊。现行英中徽章通过Steam RemoteStorage/FileShare独立托管，cloud_file及URL记录在workshop/page.json，不删除对应云文件。移除预览会使其旧CDN链接404，不能用已删除的画廊条目托管正文图片；维护时先迁移正文链接并验证，再清理预览。画廊保留游戏截图及中文封面。
- README、发布说明、版本、构建工具、测试和工坊素材以本目录为维护入口。原工程 `packaging/public/` 及历史 `dist/github-preview-*` 不再作为活动模板。
- `dist/` 为生成运行包、ZIP及验收记录，不提交Git。工坊只上传其中实际模组文件夹，不能上传整个工程。
- 本地检查：`python -B tools/build.py --check`，`python -B -m unittest discover -s tests -v`；构建用 `python -B tools/build.py --output dist/<新的目录名>`，不得覆盖旧产物。
- GitHub `wangyufeng0615/eu5-location-descriptions` 只含本发布工程，按用户要求保持私有。Windows 连不上 github.com：推送时在 Windows 打 `git bundle`，拷到能联网的机器克隆、导入、快进推送，再在 Windows 用 `git update-ref refs/remotes/origin/main <sha>` 对齐。用户已选择工具MIT、介绍CC BY-SA 4.0。发布状态见 [docs/RELEASE_READINESS.md](docs/RELEASE_READINESS.md)。
- 版本号一律用 `x.y.z`，不加后缀；每次上传工坊前先在 `project.json` 和 CHANGELOG 升版本，构建目录命名为 `dist/release-x.y.z/`（`tools/build.py` 拒绝带后缀的版本号）。1.0.1 = 四色封面 + 33 条标点修正 + 补上导出漏掉的 62 个地块；1.0.2 = 修复旧脚本留下的正文格式损坏（英文段落合并、中文段首空格、early later、谈论资料的句子）；1.0.3 = 玩家反馈修正 Wallerfangen 颜料名（Wallerfanger blue）；1.0.4 = 玩家反馈重写无锡（锡矿得名不再当作事实）；`dist/release-1.0.0/` 与 `dist/release-1.0.0-language-artwork/` 是旧命名下的历史包，保留回滚。游戏模组工具上传时路径填完整路径 `%USERPROFILE%\Documents\Paradox Interactive\Europa Universalis V\location_descriptions_enhanced`（构建后用 robocopy /MIR 同步）；2026-10-31 填相对名字时曾把整个工程文件夹（317 MB）传上去。文案、截图与封面直接维护在 `workshop/`。可用 `tools/steam_page.py` 经游戏自带DLL及当前Steam登录会话更新既有条目，默认只读，写入必须显式指定旗标；操作及实测限制见PUBLISHING。两语标题和正文须一起提交，已实测描述单独更新会清空中文标题。不得修改可见性、自动接受条款或创建新条目；所有写入仍须用户明确授权。不覆盖旧产物，预检不代表线上状态。
- 不使用Computer Use／Computer User；不写入账号密码或token。上传、安装和可见性变更只在用户明确要求时做。
- 项目总览（两个工程、数据流、技术要点、维护流程）和推广文案（Reddit、贴吧、B站脚本）在 Obsidian 笔记库的 生活/游戏/EU5 地块描述 Mod 项目总览.md 与 生活/游戏/EU5 地块描述 Mod 推广文案.md。
