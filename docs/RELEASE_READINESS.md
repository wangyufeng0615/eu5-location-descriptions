# 发布准备情况

更新：2026-10-26（Asia/Shanghai）。当前结论：**英文与简体中文首发材料及候选包已准备，发布工程已上传私有GitHub；正文包尚未安装，工坊尚未上传或公开，实机及订阅验收仍待完成。**

显示名为 **Location Descriptions for Every Tile**（全地图地点介绍），内部ID保留 `location_descriptions_enhanced`。英文与简体中文同一个工坊条目、同一个运行包；其他语言作为后续贡献方向，不冒称已支持。封面沿用用户选定的朴素文字与地块线条，历史素材保留。

## 已落实

- 2026-10-30 按游戏 1.4（build 26300913）从原工程重新导出：28,254 个地点双语正文，257 个官方保护ID（1.3 新增 133 个官方介绍，原有对应正文不再导出），62 个已不在 1.3 地图上的ID移除。
- 用户已选择MIT工具许可、CC BY-SA 4.0新增正文许可；完整许可、具体适用范围、维基贡献者链接和改写/翻译声明随包提供。
- 原创AI封面及512像素包内PNG缩略图，保存主图、实际提示词和哈希来源；封面不冒充截图，也不混用官方游戏美术。
- 实际阅读六个EU5社区作者页面，按功能、使用、兼容、反馈和归属组织自然的英中文案；参考与取舍见 [COMMUNITY_REFERENCES.md](COMMUNITY_REFERENCES.md)。Oikoumene也含地点介绍，明确提示覆盖及两语内容不一致风险，没有冒称实测兼容。
- 英中工坊页面、合并后备文案、FAQ、完整贡献指南、公告、变更说明、三个双语反馈讨论主题及GitHub Issue/PR模板已准备。允许单语言、无内部ID的反馈；采纳的正文修改先回研究主库，再导出发布。不虚构外部联系方式、GitHub链接或工坊ID。
- 运行包附带双语使用说明、FAQ与贡献指南，手动下载玩家也能找到。英中离线工坊文案预览已实际渲染并查看，未用预览代替真实Steam页面或游戏截图。
- 构建后重新读取成品及ZIP，比对全部本地化、元数据、来源与许可；拒绝官方ID覆盖、重复ID、缺语种、无来源及异常配置路径。
- 预检检查UTF-8页面字节数、图片尺寸/大小、许可、文件清单、链接、敏感模式，以及可选的7份游戏源指纹/Steam build。
- GitHub Windows/Ubuntu构建检查已启用，第三方Actions固定到已查询的commit，仅有contents读取权限，不上传工坊或改变可见性。首次云端检查发现篡改测试依赖文件遍历顺序，已固定英文目标并断言实际修改。修复提交 `388f7a2` 的 [Windows与Ubuntu检查](https://github.com/wangyufeng0615/eu5-location-descriptions/actions/runs/40318351150) 均已成功，包含22项测试、构建、成品/ZIP复验及预检；这些结果不代表游戏跨平台实测。
- 私有仓库：[wangyufeng0615/eu5-location-descriptions](https://github.com/wangyufeng0615/eu5-location-descriptions)。首批提交 `8a1fa58` 和修复提交 `388f7a2` 已推送，API确认private和main，远端120个文件与本地Git文件清单一致，包含58个数据文件。研究库历史、数据库、缓存、dist及游戏原文件未上传；按用户安排，游戏与工坊验收完成前保持私有。
- 本次上传的是已整理、核对的发布快照。另一个任务已在研究工程继续扩写；本轮未将进行中的新稿混入发布数据。公开前须从确认过的研究检查点单向同步、重新构建及验收，旧包回执不能证明新正文已验收。
- 具体实机样本、截图计划、更新/回滚和上传排错说明已准备。新增只读地点搜索工具及首发资料包生成器；人工证据须绑定当前ZIP、版本、游戏build及证据文件哈希，缺记录保持未就绪。工具不独立判断记录真实性或史实正确性。

## 当前运行包与命令

当前模组文件夹：`dist/release-candidate-20261026-en-zh-final/location_descriptions_enhanced/`。同目录有ZIP和 `build_receipt.json`。最终预检记录为 `dist/release-preflight-en-zh-readycheck-20261026.json`；旧候选、预检及旧图保留历史，之后重建继续使用新目录。

22个自动测试通过，覆盖官方保护、双语缺失、来源修订、成品及ZIP篡改、双语页面、预览转义、包与人工证据绑定等。运行包186个文件，其中114个本地化文件；正文及原始58个数据文件不因发布整理而修改。当前1254×1254 JPG为108209 bytes、512×512 PNG为240629 bytes，低于项目预算。13个实机样本仍待用户操作验收。

首发资料包：`dist/launch-pack-20261026-en-zh-final/`，包括英中及合并HTML预览、可复制文案、`private-test.local.vdf`、`release-evidence.json` 与文件清单。VDF可见性2、首次ID为0，仅为SteamCMD测试后备配置，未执行上传。证据表已填入包身份，人工项全部pending。游戏工具仍为首选；已有条目更新必须填写真实条目ID。

当前ZIP SHA-256：`8485d0cc975b2f3fa753f4a25491bf15e06be0b8a0165040b07e75444ffca322`。

```sh
python -B tools/build.py --check
python -B -m unittest discover -s tests -v
python -B tools/build.py --output dist/YOUR_NEW_CANDIDATE
python -B tools/build.py --verify dist/YOUR_NEW_CANDIDATE
python -B tools/preflight.py --build dist/YOUR_NEW_CANDIDATE --output dist/YOUR_NEW_REPORT.json
python -B tools/prepare_launch.py --build dist/YOUR_NEW_CANDIDATE --output dist/YOUR_NEW_LAUNCH_PACK
```

预检可加 `--game-root` 指向本机游戏根目录，检查实际基线。本机7份游戏源文件及Steam build 26300913（1.4.6）已匹配。真实验收后用 `--evidence` 引用对应证据表；`--require-publish-ready` 在人工和外部记录未齐时返回非零。普通本地预检通过只代表本地材料和格式通过。工具不会上传、接受协议或自动改变公开状态。

## 尚待真实完成

| 项目 | 当前状态 | 完成方式 |
|---|---|---|
| 完整正文包实机显示及真实截图 | 待执行 | 按 [SMOKE_TEST.md](SMOKE_TEST.md)，由用户进行游戏操作，保存包哈希、语言、样本、截图和日志 |
| 第三方特殊声明与受保护引用 | 未做逐篇穷尽检查 | 对实际复用材料保留必要声明，发现问题回原内容工程处理；不能仅凭许可文件声称全部通过 |
| 独立史实复核 | 城市已完成，其余未逐篇 | 城市 573 条已对照英文和当地语言维基逐项核对；工坊介绍如实说明“AI 辅助起草、作者订正校验、难免疏漏”，欢迎纠错 |
| GitHub仓库可见性及上传 | 已私有上传，远端和修复提交CI已通过 | [wangyufeng0615/eu5-location-descriptions](https://github.com/wangyufeng0615/eu5-location-descriptions)，账号、private、main与120个源文件清单均已核对；不把私有链接当公开支持入口 |
| 研究工程后续扩写同步 | 本次未同步 | 按STRUCTURE的单向流程从确认过的检查点导出，核对差异后形成新候选并重新验收，不触碰另一任务进行中的写作 |
| Steam账号资格、条款、注册邮箱 | 待账号所有者确认 | 在实际提交流程检查，不读取或记录凭据 |
| 首次私有上传、审核与实际订阅 | 待执行 | 保留真实条目ID，核对实际下载版本/文件并进游戏复验 |
| 成就、联机和跨平台 | 未验证 | 无实测前不作为对外兼容承诺 |

这些剩余项包含明确需要游戏、账号或后续独立核验的工作，不用占位截图、生成图或自动生成的“通过”记录代替。

来源与要求见 [STEAM_REQUIREMENTS.md](STEAM_REQUIREMENTS.md)，操作顺序见 [PUBLISHING.md](PUBLISHING.md)，维护与回滚见 [UPDATE_AND_ROLLBACK.md](UPDATE_AND_ROLLBACK.md)。
