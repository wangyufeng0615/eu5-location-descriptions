# Steam官方要求与本项目落实

检索日期：2026-10-26（Asia/Shanghai）。只把读取到的一手资料和本机官方游戏文件作为已核对依据。Steamworks面向开发商的后台设置，与社区Mod作者的发布工作分开处理。

| 主题 | 官方依据 | 对本工程的落实 |
|---|---|---|
| 运行包内容 | [ISteamUGC SetItemContent](https://partner.steamgames.com/doc/api/ISteamUGC#SetItemContent) | 上传实际模组文件夹，避免将所有文件合并成ZIP再交给工坊；ZIP仅作单独下载。 |
| 创建与更新 | [Workshop implementation](https://partner.steamgames.com/doc/features/workshop/implementation) | 保存首次产生的条目ID，后续更新原条目。SteamCMD只保留为官方记录的测试后备渠道，不做无人值守上传。 |
| 标题与正文大小 | [ISteamRemoteStorage constants](https://partner.steamgames.com/doc/api/ISteamRemoteStorage#constants) | 标题使用UTF-8字节检查，最大正文8000 bytes；本项目正文预算保守设为小于8000。另遵守EU5创建工具名称3–60字符。 |
| 页面语言 | [SetItemUpdateLanguage](https://partner.steamgames.com/doc/api/ISteamUGC#SetItemUpdateLanguage) | Steam页面API语言为 `english` / `schinese`；游戏文本目录是 `english` / `simp_chinese`。已准备分语言文案，也提供合并双语文案供游戏上传UI只有单字段时使用；不假定UI一定有多语言编辑器。 |
| 图片 | [SetItemPreview / AddItemPreviewFile](https://partner.steamgames.com/doc/api/ISteamUGC#SetItemPreview) | 主图准备JPG，包内提供PNG缩略图。附加图片接口明确小于1 MB。本项目对两个分发图片也使用小于1,000,000 bytes的保守预算，方形及至少512像素为项目政策，不冒称Steam/EU5的通用硬性尺寸。 |
| 可见性 | [PublishedFileVisibility](https://partner.steamgames.com/doc/api/ISteamRemoteStorage#ERemoteStoragePublishedFileVisibility) | 初始配置为私有2；Unlisted 3仍可通过链接访问。实际游戏UI可见性选项待操作确认，不能猜默认。 |
| 条款 | [Workshop legal agreement入口](https://steamcommunity.com/workshop/workshoplegalagreement/)、[Steam Subscriber Agreement §6](https://store.steampowered.com/subscriber_agreement/) | 官方入口目前引导至SSA；实际上传可能出现游戏附加条款。由账号所有者接受，不自动勾选或代为接受。 |
| 账号资格 | [Limited User Accounts](https://help.steampowered.com/en/faqs/view/71D3-35C2-AD96-AA3A) | 官方搜索可读摘要将提交工坊内容列为受限功能。正文读取返回页面壳，未据此断言本账号状态。上传前在Steam账号中确认资格，无需本项目读取账号配置或凭据。 |
| 邮件和审核 | [User-Generated Content Approval](https://help.steampowered.com/en/wizard/HelpWithUGCSubmission) | 首次提交可能要邮箱确认，某些社区会审核新条目或更新。审核时订阅者可能仍收到此前已批准版本；用实际下载文件核验，不能把上传完成当公开可见。 |
| 内容与权利 | [Steam Online Conduct](https://store.steampowered.com/online_conduct/)、[Paradox User Agreement §5](https://legal.paradoxplaza.com/eula) | 项目免费、不冒充官方、保留来源和权利边界，不分发原版游戏或其他无权使用的材料。 |
| 维基材料 | [Wikimedia Terms §7](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use#7._Licensing_of_Content)、[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/legalcode.en) | 用户选择新增正文用CC BY-SA 4.0，工具用MIT；随包提供许可原文、逐地点来源和修订/贡献历史链接，并说明改写与翻译。第三方特殊声明和受保护引用仍须逐项处理，许可选择不等于全量审核。 |

Steam游戏商品上架、Steam Direct付费、发行商Cloud配额或API后台开关不作为本社区模组的额外流程。不能把发行游戏的审核要求或其他游戏的模组步骤直接当成EU5作者要求。[Steam Workshop overview](https://partner.steamgames.com/doc/features/workshop)提供平台背景。

## EU5本机证据

本轮重新核对Steam AppID **3450310**、build **24187685**，并读取随游戏提供的：

- `game/main_menu/gui/mod_tools.gui`：新建上传、从文件夹更新、错误/进度结果界面，名称输入最多60字符。
- `game/main_menu/create_mod_tags.json`：Historical、Translation为实际支持的Steam标签。
- `game/main_menu/localization/english/caesar_tools_l_english.yml`：字段、按钮和上传更新路径文案。
- `clausewitz/loading_screen/localization/gui/cw_ugc_dlc_l_english.yml`：Steam在线、名称3–60字符和短介绍要求。

已工作的旧原型证明 `.metadata/metadata.json` 链路；当前正文包仍需独立游戏验收。`.metadata/thumbnail.png`按常见EU5约定准备，未声称已通过该版本缩略图显示/上传实测。官方wiki请求401，Steam部分帮助页只返回壳；这些限制已记录，不以社区转载替代已验证的官方结论。

## 这轮可在本地解决的差距

完整许可与归属、原创封面和缩略图、双语/合并文案、版本变更说明、成品逐值与ZIP复验、输入边界保护、字节及图片预算、源码清单/敏感模式检查、只读游戏基线检查、CI配置、纠错入口、实机清单和回滚方案均纳入准备。

GitHub发布工程已私有上传并核对远端；真实截图、游戏中长文本/多语言效果、Steam账号资格和条款、首次工坊上传/审核/真实订阅仍待实际操作，必须留出可核验结果，不填虚构通过状态。当前状态见 [RELEASE_READINESS.md](RELEASE_READINESS.md)。
