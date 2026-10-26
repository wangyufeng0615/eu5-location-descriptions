# EU5工坊页面参考与本次取舍

检索日期：2026-10-26。样本来自EU5工坊按[总独立订阅量排序的第一页](https://steamcommunity.com/workshop/browse/?appid=3450310&browsesort=totaluniquesubscribers&section=readytouseitems)，不是对模组质量或当前可用性的认证。直接阅读作者页面；不复制其正文、截图、图标、群号或个人风格。

| 作者页面 | 观察到的页面做法 | 本项目采用的方式 |
|---|---|---|
| [Better Road Builder](https://steamcommunity.com/sharedfiles/filedetails/?id=3605677866) | 功能、排错和兼容条件分开写 | 页面先回答做什么、怎么用和冲突，技术维护放文档 |
| [Glorp UI](https://steamcommunity.com/sharedfiles/filedetails/?id=3601047146) | 醒目的版本信息，功能列表与建议入口 | 显示实际基线；只写已证实的兼容性，不照抄其运行结论 |
| [Community Flavor Pack](https://steamcommunity.com/sharedfiles/filedetails/?id=3599543453) | 简短目标、明确范围，以及FAQ/建议/许可/署名入口 | 玩家文案简洁，贡献与许可可单独找到，不为本项目凭空建立Discord |
| [凯撒汉化](https://steamcommunity.com/sharedfiles/filedetails/?id=3599706198) | 中文FAQ、反馈和招募入口 | 中文独立自然撰写，提供无需GitHub的反馈路径；不照搬其玩笑、许可或外部联系方式 |
| [Oikoumene: Dynamic Place Names](https://steamcommunity.com/sharedfiles/filedetails/?id=3721193233) | 列明语言、资料方法、纠错意愿及同类内容覆盖风险 | 英中同包；欢迎单语言纠错；明确其也有介绍内容，不能归为纯地名无冲突 |
| [Europa Expanded](https://steamcommunity.com/sharedfiles/filedetails/?id=3599116549) | 将已实现内容与未来计划分开 | 首发只承诺英中已写正文，其他语言不写成已支持 |

部分Steam文本抓取同时带有“移除/不兼容”页面提示，无法仅凭抓取确定其真实可见性或当前运行状态；本报告只引用实际读到的作者说明。订阅排名及数量会变化，不把样本写成永久排名。

## 双语首发安排

一个工坊条目、同一运行包，含英文和简体中文；不拆成互相依赖的语言子模组。英文与中文页面各自可独立阅读，并保留合并版供只有一个描述字段时使用。

Steam页面使用 english / schinese，游戏目录使用 english / simp_chinese。分别核对标题、说明、截图和变更记录；两语应表达相同的事实和限制。依据：[Steam语言代码](https://partner.steamgames.com/doc/store/localization/languages)、[工坊语言接口](https://partner.steamgames.com/doc/api/ISteamUGC#SetItemUpdateLanguage)。

当前模板中的“订阅/留言”是公开时的玩家指引，不表示已经上传。实际上传、协议、邮件确认、平台审核和真实订阅分别留证。依据：[Steam UGC确认与审核](https://help.steampowered.com/en/wizard/HelpWithUGCSubmission)。
