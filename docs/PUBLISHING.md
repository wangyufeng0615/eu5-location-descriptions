# Publication workflow / 发布流程

本目录现为独立发布工程，结构和与原研究工程的边界见 [STRUCTURE.md](STRUCTURE.md)。目录独立不代表已经上传或公开。

This is an alpha Workshop publishing project. The owner selected MIT for tools and CC BY-SA 4.0 for new prose/translations on 2026-10-26; see [LICENSE](../LICENSE). English and Simplified Chinese launch copy, player guides, cover artwork and local checks are prepared. The GitHub repository is private by the owner's instruction. Exceptional third-party reuse review and full-text game/subscription testing remain pending; no Workshop upload has occurred. Current evidence and outstanding work are in [RELEASE_READINESS.md](RELEASE_READINESS.md); official requirements are in [STEAM_REQUIREMENTS.md](STEAM_REQUIREMENTS.md).

## English and Simplified Chinese launch

Use one Workshop item containing both languages. Maintain the native [English](../README.md) and [Chinese](../README.zh-CN.md) player pages, [English](FAQ.md) and [Chinese](FAQ.zh-CN.md) FAQs, and both contribution guides together. Feedback may use either language and does not require an internal ID. Accepted content proposals go through the research ledger before export; see [MAINTAINING.md](MAINTAINING.md).

The current candidate is `dist/release-candidate-20261031-1.0.0-final/`. That directory retains `private-test.local.vdf` and `release-evidence.json` alongside the ZIP and build receipt, outside the actual mod folder; the evidence form identifies this exact package and all manual checks remain pending. Page text, announcements, change notes and artwork stay in `workshop/`, without a duplicate launch pack. These are prepared materials, not posted messages. Workshop comments are the player feedback channel. The author commits to active maintenance, following up on feedback, fixing problems and keeping up with game updates. Community-page choices are documented in [COMMUNITY_REFERENCES.md](COMMUNITY_REFERENCES.md).

Check the final page appearance on the actual private Steam Workshop item. No local HTML preview tool is required or maintained.

The selected display title is **Descriptions for Every Tile** / **所有地块的描述**. `workshop/page.json` lists both cover images for validation; the Chinese README uses the Chinese JPEG. The shared Workshop primary image and runtime thumbnail remain English. Use the Chinese JPEG as additional promotional material; no automatic language-specific Steam primary-image switching is assumed. Source geometry, prompts, selected images and old-artwork preservation are documented in [artwork notes](../workshop/assets/README.md).

For a later build, copy [release-evidence.example.json](release-evidence.example.json) into the new candidate directory alongside its ZIP and build receipt. Fill in the exact ZIP hash, version and game build. After real tests, reference the records for that package and run `python -B tools/preflight.py --build dist/YOUR_CANDIDATE --evidence dist/YOUR_CANDIDATE/release-evidence.json --require-publish-ready`. Missing records keep the release pending; incorrect file hashes or a different candidate fail validation. The tool checks record completeness, not the truth of game screenshots, account actions or historical claims, and never authorizes an upload. If needed, adapt `workshop/upload.vdf.example` for private SteamCMD testing; the game tools remain the preferred upload route.

## GitHub first

1. Review the English and Chinese README, selected license scopes, attribution and page drafts. Retain upstream third-party notices; the project license does not override them.
2. Run `python -B tools/build.py --check`, unit tests, then build into a new `dist/` directory. Preserve its `build_receipt.json` and ZIP hash.
3. The owner authorized `wangyufeng0615/eu5-location-descriptions` as a private repository on 2026-10-26. This source tree has its own main history; the research history, databases, caches and dist output are excluded. `.gitignore` cannot remove already tracked history. Verify the pushed commit and remote file tree after each upload.
4. Keep GitHub private until game and Workshop acceptance is complete, as the owner requested. Those checks are still pending; this source upload does not satisfy them. The private URL is for maintainers and invited collaborators, not a publicly accessible support channel. CI checks the source and build only; it does not publish to the Workshop or change visibility.

## EU5 Workshop

1. Review exceptional upstream notices, use the prepared cover and capture authentic screenshots while testing the full-text package according to [SMOKE_TEST.md](SMOKE_TEST.md). `supported_game_version: "*"` is not all-version compatibility. Test both languages and the official protection set; record saves/achievements/multiplayer only after actual tests.
2. In the Steam edition, with Steam running and online, use the game's **Mod Tools**. The installed official GUI exposes **Upload New Mod** and **Upload content from a folder**. Select only the built `location_descriptions_enhanced/` directory, never this repository root or its parent `dist/` directory. Include hidden `.metadata/`.
3. Review the account, package and visibility before submitting. Prefer a private first upload; the exact game default visibility has not been verified. If the game UI does not expose a private option, resolve visibility before a public submission. The generic Steam API supports private uploads; this does not establish what every EU5 UI version exposes.
4. Accept the applicable Workshop terms as the owner and complete any email verification or moderation step. Retain the resulting item ID; update that item in future. Use `workshop/page.json` and the English/Chinese text, or the combined `description.default.txt` if the game tool exposes one description field. Do not confuse Steam page `schinese` with the game's `simp_chinese` directory. Replace pre-publication status only with verified results.
5. Test a clean subscription/download, confirm the metadata and localization files actually received, disable local duplicate/prototype copies, enable the subscribed mod, and recheck both languages. Confirm the downloaded version matches the intended package before changing visibility to public.
6. Record item URL/ID, repository commit, version, baseline, checksum, change notes and test results. For rollback, rebuild and upload a known-good previous package to the same item ID; do not delete and recreate the listing.

## SteamCMD testing fallback

Valve documents SteamCMD workshop upload as a **testing** route. `workshop/upload.vdf.example` is deliberately incomplete and uses private visibility (`2`). It is not a verified EU5 upload integration. New items use `publishedfileid` zero; updates must retain the returned nonzero ID. SteamCMD writes that ID back on success. Credentials and Guard codes must not be committed or put in scripts. No unattended uploader is supplied.

## Official sources checked on 2026-10-26

- [Steam Workshop overview](https://partner.steamgames.com/doc/features/workshop): platform model and integration context.
- [Steam Workshop implementation](https://partner.steamgames.com/doc/features/workshop/implementation): folder payload, item identity, agreement, upload/update flow, SteamCMD testing and logs. Developer-side Steamworks setup instructions apply to the game's publisher, not automatically to a community mod author.
- [ISteamUGC preview](https://partner.steamgames.com/doc/api/ISteamUGC#SetItemPreview): web-readable image formats; additional image APIs require below 1 MB. Prepared cover is 1254×1254 JPG and package thumbnail is 512×512 PNG, both below the project's conservative 1,000,000-byte budget. These dimensions are project choices, not verified universal EU5 rules.
- [Steam visibility enum](https://partner.steamgames.com/doc/api/ISteamRemoteStorage#ERemoteStoragePublishedFileVisibility): public 0, friends 1, private 2, unlisted 3. Unlisted is still accessible by link.
- [Steam Subscriber Agreement, §6](https://store.steampowered.com/subscriber_agreement/): UGC/Workshop terms; a game's specific terms can also apply.
- [Paradox User Agreement, §5](https://legal.paradoxplaza.com/eula): mod creation/publication and responsibility for rights; distribution is non-commercial under these terms.
- [Wikimedia Terms of Use, §7](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use#7._Licensing_of_Content): reused text, attribution and applicable licenses.
- [GitHub repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits): ordinary Git single-object 100 MB enforcement; generated databases/caches belong outside the source tree.

Additional official research in this preparation round: [UGC email verification and moderation](https://help.steampowered.com/en/wizard/HelpWithUGCSubmission), [Steam Online Conduct](https://store.steampowered.com/online_conduct/), [title/description byte constants](https://partner.steamgames.com/doc/api/ISteamRemoteStorage#constants) and [Steam page language](https://partner.steamgames.com/doc/api/ISteamUGC#SetItemUpdateLanguage). See [STEAM_REQUIREMENTS.md](STEAM_REQUIREMENTS.md) for limits of access and how each requirement is applied.

EU5-specific controls and field names were also checked against the installed game's own `game/main_menu/gui/mod_tools.gui`, `game/main_menu/localization/english/caesar_tools_l_english.yml` and Clausewitz UGC localization. These files are not redistributed. The EU5 wiki returned HTTP 401 during this research; it has not been used as verified instructions. No actual upload, account-capability test or game interface operation has occurred.
