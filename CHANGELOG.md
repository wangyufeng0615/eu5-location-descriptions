# Changelog

## 1.1.1 — 2026-11-12

- Fixed the later-city line for Seattle: it now sits on the east shore of Puget Sound (Puyallup) instead of the Kitsap side (Twana). Thanks to the player who reported it.
- Fixed the later-city line for Olympia: moved from Chehalis to Nisqually.
- Locations that are themselves a city or town (Caracas, Phnom Penh, Ouagadougou, Suakin, Ternate and 26 others) now say "The later city of X also lies here."
- Rewrote the Chiquimula description to cover the Spanish conquest, the colonial corregimiento and the 1765 earthquake, and removed post-1837 content.
- Chinese: Sing Buri now uses its standard Chinese name.

## 1.1.0 — 2026-11-11

- Add a closing line to 788 locations in the Americas, Oceania, Sub-Saharan Africa, Southeast Asia and Siberia whose tribal or indigenous names hide a well-known later city, for example "The later city of Denver lies here."
- Where the city sits on the border between two locations, the line says it lies nearby.
- This line is the only place where the descriptions name cities founded after 1837. Suggested by a player.

## 1.0.9 — 2026-11-04

- Revise 50 high-profile locations after a source-checked spot review.
- Rewrite Xiangyang, Yangqu, Panyu, Agra, Niani and Malacca with sourced histories of the 1337-1837 era.
- Correct facts and Chinese name renderings in about 40 more entries, including Kunming, Xi'an, Medina, Vilnius, Oxford, Berlin, Jiangdu and Marseille.

## 1.0.8 — 2026-11-03

- Revise ten English and Simplified Chinese descriptions after checking place identities, historical sources and the game map.
- Correct misplaced subjects in Budjanga, Abitau, Lhakang, Nanlang and Fraserburgh; distinguish Abidos from the later town of Canakkale.
- Replace unsupported town-specific stories in Dzingcho and Sesheke with regional descriptions, and refine Mayumba and Mauna Loa.
- Add a one-line history of each public release to the Workshop description.

## 1.0.7 — 2026-11-03

- Correct 19 English and Simplified Chinese location descriptions whose subjects did not match their map locations.
- Rewrite Bone for the Bugis kingdom of South Sulawesi, and correct misplaced towns, regional identities and coastal settings across Asia, Europe, Australia and the Americas.

## 1.0.6 — 2026-11-02

- Fix ten locations whose description was about a different place with the same or a similar name, found in an identity audit of about 600 high-risk entries: Baofeng (was the Gaocheng observatory in Dengfeng), Lai'an (was Sicheng), Büren (was Buren in the Netherlands), Pingshan in Huidong (was Pingshan in Shenzhen), the upper Burdekin (was its delta), the upper Mezen (was the town of Mezen), the upper Ingul (was Mykolaiv), Banda (was the Bandanese villages on Kei), Altyntobe (was Shymkent) and Araban (was Araban in Gaziantep).
- Update the bundled FAQ and compatibility notes: achievements stay available, the mod can be added to an existing save, and multiplayer needs the same mods.

## 1.0.5 — 2026-11-02

- Fix Wuchang: the game's Wuchang is the old Wuchang county, modern Ezhou, not the city with the Yellow Crane Tower. It now covers Sun Quan's capital, the bream of Fankou and Su Shi's pavilion on the West Hill. Reported by a player.
- Rework Jiangxia, the county of Wuchang city: the seat of Huguang province under the Yuan, the Yellow Crane Tower and the Ming princes of Chu.

## 1.0.4 — 2026-11-01

- Rewrite Wuxi: the old text presented the "exhausted tin mines" story as the origin of the name, which is a later folk explanation. It now covers the town's Song-era fairs, its rise to a prefecture in 1295 and the Donglin Academy in more detail. Reported by a player.

## 1.0.3 — 2026-11-01

- Fix the name of the pigment in Wallerfangen: it is "Wallerfanger blue" (German "Wallerfanger Blau"), and it was traded as far as Italy. Reported by a player.

## 1.0.2 — 2026-10-31

- Restore paragraph breaks that an old cleanup script had merged in 124 English descriptions, and remove stray leading spaces from 182 Chinese paragraphs.
- Fix 17 English sentences that had lost the space after a full stop, and a few stray blank lines, trailing spaces and invisible characters.
- Change "early later" back to "early modern" in 40 English descriptions, and repair the remaining dates that an old script had turned into "later"/"后来".
- Remove sentences that talked about the research material instead of the place ("the excerpt records…", "所给资料…", "仍需核实"), and a few references to events after 1837.
- The exporter now cross-checks locations it believes are off the map against the game's location names.

## 1.0.1 — 2026-10-31

- Add 62 locations the exporter had skipped because their IDs sat right before a closing brace in the map file (Porto Santo, Lampedusa, part of the Ligurian Sea and others). Coverage is now 28,316 of the 28,573 map locations, plus the 257 vanilla descriptions.
- Fix punctuation in 33 descriptions (dashes replaced) and remove a corrupted closing passage from Beira Estuary.
- Adopt the four-colour Sicily covers (23 game locations, neighbours in different colours, larger title) for the Workshop cover, Chinese cover and package thumbnail; archive the Sicily-outline set.
- Remove the unused local HTML preview generator, its tests, duplicate launch packs, temporary rendering profiles and discussion templates. Keep build/validation tools, approved artwork, release candidates and manual acceptance records.
- Add short English/Chinese installation instructions and make Workshop comments the primary feedback channel, with the author's commitment to active maintenance and game-update support.
- Rename the display title to **Descriptions for Every Tile** / **所有地块的描述**; keep the stable mod ID and version.
- Adopt matching English and Chinese Sicily-outline artwork, emphasizing EVERY TILE and 所有地块. Use the English cover and thumbnail for the shared package; use the Chinese artwork in the Chinese README and additional promotional material.
- Preserve the previous artwork and release candidates. No location descriptions or source records changed in this artwork update.

## 1.0.0 — released 2026-10-31 on the Steam Workshop (item 3830305546)

- Rebuilt for game 1.4.6 (Steam build 26300913); map and vanilla description files are unchanged from 1.3. `supported_game_version` widened to `1.*`.

- Data re-exported from the research project's YAML entries for game version 1.3 (Steam build 26211608, map of 28,511 locations).
- 28,254 locations described in English and Simplified Chinese. The 257 vanilla descriptions (133 more than in build 24187685) are protected and left untouched; 62 IDs no longer on the 1.3 map are dropped.
- Cities (1337 town rank or above) rewritten with fuller local history and checked fact by fact against English and local-language Wikipedia; other entries corrected for broken text, modern-day content and English/Chinese mismatches.
- Sources may now be any public page (Wikipedia in many languages, UNESCO, local gazetteers); revision pins are optional.
- `supported_game_version` set to `1.3.*` (the bare `*` was rejected by the game as a version mismatch).
- Workshop page copy shortened; Alpha labels removed.

## 0.2.0-alpha.1 — local packaging preview, 2026-10-26

- Display name updated to **Location Descriptions for Every Tile**; replace the decorative book-and-landscape cover with a plain typographic design. The stable internal mod ID remains unchanged. Previous artwork and builds are retained as history.

- Package English and Simplified Chinese descriptions for 28,449 locations missing official text in baseline Steam build 24187685.
- Preserve the 124 officially described locations.
- Export editable bilingual text and revision-pinned source references; exclude internal databases, caches and game files.
- Add a portable standard-library build, checksums and documentation.
- Owner-selected MIT tooling and CC BY-SA 4.0 prose licenses, full license texts, attribution and original AI cover are included.
- Add post-build/ZIP verification, page/source/asset preflight, read-only game-baseline checks, Windows/Ubuntu CI, issue templates and a concrete game test/rollback plan.
- Prepare native English and Simplified Chinese Workshop copy, announcements, FAQs, contribution guides and correction discussions for one shared item. Include bilingual player documentation in the downloadable package.
- Accept feedback without requiring internal IDs or Git knowledge; content proposals return to the research ledger before export. Add a read-only location finder and explain overlapping description mods.
- Add offline page previews and a local launch-pack generator. Manual release records are bound to the candidate checksum and evidence-file hashes; missing records keep the release pending.
- Independent fact review, exceptional third-party reuse review, authentic screenshots, full-text game/subscription tests and publication remain pending. This version has not been uploaded or released.
