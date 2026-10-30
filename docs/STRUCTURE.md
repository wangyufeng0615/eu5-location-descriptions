# 两个工程的职责和目录

2026-10-26按用户确认，原始研究工程与创意工坊工程整理为开发盘根目录的两个并列目录。

```text
eu5-location-descriptions/              原始研究工程
  content/                             写作批次、稿件与研究记录
  build/                               唯一主库、源指纹与必要对账
  tools/                               研究、导入、内容检查和候选导出
  dist/github-preview-20261026/         保留的历史发布预览
  packaging/public/                    保留的历史模板，不再维护

eu5-location-descriptions-workshop/     当前发布工程，本目录
  data/                                冻结基线的双语正文和来源
  tools/                               可移植构建工具
  tests/                               输入保护测试
  workshop/                            工坊页面文案和发布素材
  docs/                                结构、发布流程、初次导入记录
  project.json                         名称、版本和模组元数据
  README.md / README.zh-CN.md           项目首页
  CONTRIBUTING.md / CONTRIBUTING.zh-CN.md  双语贡献入口
  dist/                                生成包及校验记录，Git忽略
```

两个目录均位于本机开发盘根目录，独立于游戏安装目录。原工程和已有Git历史不迁移、不删除；发布工程不继承原Git历史。2026-10-26按用户授权创建私有GitHub仓库 `wangyufeng0615/eu5-location-descriptions`，本工程使用独立main历史。推送核验结果见RELEASE_READINESS，游戏与工坊验收完成前保持私有。

## 文件维护归属

| 内容 | 维护位置 | 如何进入发布包 |
|---|---|---|
| 英中地点正文、来源和审核状态 | 原研究工程 | 从确认过的正文检查点单向导出到本工程 `data/` |
| 官方保护集合与游戏源指纹 | 原研究工程 | 随正文一起核对并导出，不能只替换部分正文 |
| 名称、版本、README、发布说明 | 本工程 | 直接维护并进入未来GitHub源仓库 |
| 工坊页面、封面和截图 | 本工程 | 在 `workshop/` 维护，按发布流程上传 |
| 构建工具和测试 | 本工程 | 读取本地 `data/`，无需研究库或游戏即可构建 |
| 运行包、ZIP和构建回执 | 本工程 `dist/` | 实际模组文件夹用于工坊；ZIP供单独下载 |
| 玩家FAQ、贡献指南和包内README | 本工程及 `workshop/player-readme.*.md` | 构建时按 `tools/build.py` 的映射复制，包内链接以模组根目录解析 |
| 发布文案与封面 | 本工程 `workshop/` | 直接使用原文件，最终页面效果在实际私有工坊条目检查 |
| 人工验收记录 | 本工程 `dist/` | 从 `docs/release-evidence.example.json` 复制，绑定实际候选包；不上传至工坊运行目录 |

`data/descriptions/` 为57个JSONL分片，500个地点一片，最后一片不足500。`data/baseline.json` 保存目标ID、124个官方保护ID及源文件指纹。不要在两个工程中各自修改同一介绍；不进行自动双向同步。将来若决定迁移正文的权威来源，应单独调整本约定。

## 后续同步的简单流程

1. 在原工程修订内容，按原管线形成新的完整正文检查点。当前原工程已精简为唯一主库，不能把历史字段 `snapshot_database` 指向的主库误称为独立不可变快照。
2. 原工程运行 `tools/prepare_distribution.py --output dist/<新的候选名>`；它从当前发布工程读取包装文件，以只读事务一致地读取研究库中的正文、来源和保护集合，记录逻辑数据哈希，生成独立候选，不覆盖本工程或已有预览。
3. 核对候选 `data/`、官方保护集合、源指纹及差异后，再将确认过的整份数据导入本工程。已有数据在本地或Git中保留恢复点；不能直接覆盖README、工坊文案等发布文件。
4. 在本工程执行检查和测试，构建到新的 `dist/` 子目录，保留版本和哈希回执。

本次只是目录独立化；数据来自此前已核对的完整快照，未做正文改写、事实复审、上传或安装。初次导入追溯见 [initial-import.json](initial-import.json)，发布步骤见 [PUBLISHING.md](PUBLISHING.md)。
