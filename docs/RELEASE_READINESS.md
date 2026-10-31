# 发布状态与收尾记录

核对日期：2026-10-31（Asia/Shanghai）。项目为 **Descriptions for Every Tile / 所有地块的描述**，当前版本1.0.2，内部ID为 `location_descriptions_enhanced`。工坊条目 [3830305546](https://steamcommunity.com/sharedfiles/filedetails/?id=3830305546) 当前公开，已通过Steam API实时读回核对。

## 今天完成

- 重做英中四色西西里封面，标题放大、顶部留白收紧。地图参考游戏中主岛的23个地点；左下角English ✓在上、中文 ✓在下。英文作主封面和包内缩略图，中文作附加图片。
- 两枚徽章改为精确SVG排版并导出透明PNG，修正边缘、留白和coverage的视觉居中。英中各自制作，只保留100%覆盖和语言支持。
- 按作者最终中文稿同步改写英文，去掉数字汇总说明；两语标题、正文和各自徽章已发布，线上读回与本地逐字一致。
- 徽章改由Steam RemoteStorage/FileShare独立托管。移除画廊徽章后，两套正文图片实际HTTP 200且SHA-256与本地一致。画廊保留4张真实游戏截图和中文封面，原顺序不变。
- 增加无界面的Steam页面维护工具，核对所有者，默认只读，写入须显式旗标及用户授权。两语标题与正文必须一起提交；不修改可见性或创建条目。
- 增加两项画廊维护回归测试：不得删除任一正文仍引用的预览；只能移除指定徽章，按倒序索引操作。后续封面更新不再把徽章加入画廊。
- 收尾归整文档与来源记录，形成本地Git提交；未执行远程推送。旧设计、旧包和回执保留，不删除恢复材料。

## 实际发布包

当前已上传：`dist/release-1.0.2/location_descriptions_enhanced/`，2026-10-31 21:22 生效，Steam API 读回大小 38,097,176 字节，与本地包一致。

- ZIP SHA-256：`861109fac8b45a5fe71ecf1fad20393db09b8ac162c669b3263567aedf37310d`；187个运行文件。
- 28,316条英中新增介绍，257条官方介绍受保护，适配原版地图合计28,573个地点。游戏基线为1.4.6 / Steam build 26300913。
- 工具/技术文档MIT，新增介绍及翻译CC BY-SA 4.0；具体范围和第三方权利以LICENSE及归属文件为准。

| 版本 | 上线时间 | 内容 |
|---|---|---|
| 1.0.0 | 10-31 02:19 起 | 首发 28,254 条；下午换四色封面与页面文案（仍为1.0.0，包 `dist/release-1.0.0-language-artwork/`） |
| 1.0.1 | 10-31 20:38 | 补上导出工具漏读的62个地点（ID紧贴 `}` 未被识别），33条去破折号；工坊简介数字同步改为28,316 |
| 1.0.2 | 10-31 21:22 | 修复旧脚本留下的正文损坏：124条英文段落合并、182处中文段首空格、40条 early later、约50条谈论资料的句子等 |

18:52 一次更新误传了整个工程文件夹（317 MB），18:54 已重传覆盖；工坊历史版本不能删除，旧版下载链接仅作者登录可见。

## 验证证据

22项自动测试通过，当前包重新读取及ZIP校验通过。本地预检通过；未提供的人工验收项继续保持未就绪，不等同于线上发布失败，也不自动补写通过。

| 核对内容 | 本地证据 |
|---|---|
| 收尾时线上两语标题、正文和画廊 | `dist/steam-day-end-readback-20261031.json` |
| 收尾时徽章HTTP/哈希、订阅差异及包哈希 | `dist/day-end-verification-20261031.json` |
| 最新本地预检 | `dist/day-end-preflight-20261031.json` |
| 独立徽章云文件、句柄及URL | `dist/steam-independent-badges-20261031.json`、`workshop/page.json` |
| 最终画廊移除及图片可用性 | `dist/steam-gallery-cleanup-final-20261031.json`、`dist/steam-gallery-cleanup-final-verification-20261031.json` |
| 作者最终文案发布记录 | `dist/steam-author-description-update-20261031.json` |

关键实测教训已写入 [PUBLISHING.md](PUBLISHING.md)：单独更新简中描述会清空本地化标题；删除预览会使其旧CDN链接404。必须先独立托管图片、迁移正文并验证，再清理画廊。不能删除page.json记录的两个徽章云文件。

## 剩余事项

1. Steam下载完成后复核本机新缩略图，并按需在游戏里查看。正文双语由游戏语言选择；工坊标题及正文由Steam显示语言选择，主封面不随语言自动切换。
2. 今天的本地源码提交尚待同步GitHub；沿用私有仓库安排，本轮未更改远端可见性。云端CI仍对应此前提交，不能冒称今天的源码已在云端通过。
3. 页面兼容性文字按作者指定稿发布。本轮未新增中途加入存档、同类模组、成就、联机或跨平台实测；具体覆盖冲突参见 [COMPATIBILITY.md](COMPATIBILITY.md)。
4. 独立史实复核和第三方特殊声明检查继续由内容工程处理；`independent_fact_review_complete`仍为false。本轮不扩大词条工作。

收尾前的完整累计报告保存在本地 `dist/day-end-history-20261031/RELEASE_READINESS.before-closeout.md`，此前Git记录保留。发布步骤见 [PUBLISHING.md](PUBLISHING.md)，游戏验收见 [SMOKE_TEST.md](SMOKE_TEST.md)，更新回滚见 [UPDATE_AND_ROLLBACK.md](UPDATE_AND_ROLLBACK.md)。
