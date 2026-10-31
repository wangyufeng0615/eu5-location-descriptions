# Changelog

## 1.0.1 — 2026-10-31

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
