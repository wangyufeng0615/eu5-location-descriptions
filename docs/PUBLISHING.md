# Publishing / 发布流程

The mod is published as one Steam Workshop item, [3830305546](https://steamcommunity.com/sharedfiles/filedetails/?id=3830305546), with English and Simplified Chinese in the same package. Updates go to the same item; do not delete and recreate it.

## 1. Update `data/` if the descriptions changed

`data/` is exported from the research ledger (see [STRUCTURE.md](STRUCTURE.md)). Replace it with a fresh export before releasing; do not edit it by hand.

## 2. Prepare the release

```
python -B tools/release.py 1.2.3 --note "Fix the pigment name in Wallerfangen."
```

`tools/release.py`:

1. checks that `1.2.3` is a plain `x.y.z` version newer than `project.json`, and that `dist/release-1.2.3/` does not exist yet;
2. sets the version in `project.json` and adds a dated entry to `CHANGELOG.md` (repeat `--note` for several lines, or use `--notes-file` with one line per entry);
3. runs the unit tests, `build.py --check`, the build into `dist/release-1.2.3/`, `build.py --verify` and the preflight check (add `--game-root "<EU5 install>"` to compare with the installed game files);
4. with `--install`, mirrors the built mod folder to `<Documents>/Paradox Interactive/Europa Universalis V/location_descriptions_enhanced` and checks every file hash;
5. with `--commit`, commits `project.json`, `CHANGELOG.md` and `data/`;
6. prints the upload folder, file count and total bytes.

`--dry-run` runs the checks and builds into `dist/dryrun-<time>/` without changing the version, CHANGELOG, install folder or Git.

## 3. Upload through the signed-in Steam client (preferred)

Since 1.0.7 (2026-11-03), updates to the existing item can be uploaded without opening EU5's Mod Tools. A user request to release a version authorizes the prepared content upload; it does not authorize creating another item, changing visibility, accepting new terms or changing account permissions. Those actions remain with the owner.

`tools/steam_upload.py` reuses the Steam bindings in `steam_page.py`. It validates the requested version, complete build contents, archive and receipt, then checks that the signed-in Steam account owns item `3830305546`. Only the release's absolute mod-folder path is submitted. Titles, descriptions, cover, gallery and visibility are compared before and after. It does not read credentials.

First write the version and English notes to `workshop/changenotes.en.txt`; keep the Chinese file alongside it. The first line must be the version. Run a local-only check (safe over SSH):

```bat
python -B tools\steam_upload.py 1.0.8 --output dist/upload-1.0.8-check.json
```

The check does not connect to Steam. To upload, run the following **inside the Windows desktop session where the owner is signed in to Steam**:

```bat
python -B tools\steam_upload.py 1.0.8 --upload --notes-file workshop/changenotes.en.txt --output dist/upload-1.0.8.json
```

Use a new output filename each time. Existing records are never overwritten. Without `--upload`, nothing is submitted. Do not use Python `-O`: the reused Steam bindings contain assertions.

For remote operation, save that command in a `.cmd` file with `cd /d` pointing to the publishing checkout, `set PYTHONIOENCODING=utf-8`, an absolute Python executable, and stdout/stderr redirected to a new log. Use `query user` to identify the signed-in desktop user. Schedule the command with that user's interactive token, then start it:

```bat
schtasks /create /tn EU5Release_VERSION /tr C:\absolute\path\upload.cmd /sc once /st 23:59 /ru DESKTOP_USER /it
schtasks /run /tn EU5Release_VERSION
```

Choose a unique task name and a future scheduled time; `/run` starts it immediately. Read the JSON/log until completion. A scheduler success message only means the task started. Success requires Steam `result=1`, `metadata_unchanged=true`, and the online checks below. Once the process has finished, delete **only this temporary task** with `schtasks /delete /tn EU5Release_VERSION /f` so it cannot run again at its scheduled time. Never supply stored passwords or change the user's Steam session to make this work.

If an upload times out or its result is unknown, inspect the Workshop update time, size and record before retrying: it may already have succeeded. If Steam requires terms acceptance or the owner does not match, stop and hand that step to the owner.

### Fallback: EU5 Mod Tools

If the desktop Steam API cannot be used, open **Mod Tools**, select the existing mod, choose **Upload content from a folder**, and enter the **full path** of the installed folder printed by `release.py`. Upload only `location_descriptions_enhanced/` (with its hidden `.metadata/`), never the repository or `dist/`. A relative name has uploaded the whole working folder before.

## 4. GitHub release

Push the tag `vX.Y.Z` for the release commit (`tools/release.py` does not do this; the maintainer's release script does). `.github/workflows/release.yml` then checks that the tag matches `project.json`, runs the tests, builds and verifies the package, and attaches `location_descriptions_enhanced-X.Y.Z.zip` to a GitHub release, with the CHANGELOG entry and install steps as release notes.

## 5. Verify

Verify Steam result=1, the new update time, unchanged visibility, and the Workshop item's `file_size` from Steam's public `ISteamRemoteStorage/GetPublishedFileDetails` against the total bytes printed in step 2. Download the GitHub Release ZIP and compare every extracted file hash with the build receipt; ZIP container hashes can differ between platforms. These checks verify the release artifacts and upload, not in-game rendering or a fresh subscriber download. Steam defers downloading updates for subscribers while EU5 is running.

## 6. Change notes

The API uploader submits the English note together with content; 1.0.7 verified that this creates a real change-note entry. EU5's Mod Tools sends no note and leaves an empty entry. In either case, finish and verify both language variants in the owner's signed-in Chrome: open the Change Notes tab, choose **Edit** on the newest entry, write the English note under English and save, then switch the language to Simplified Chinese and save the Chinese note. Use `workshop/changenotes.en.txt` and `workshop/changenotes.zh-CN.txt` as the text. Submitting a note through the Steam API without new content is accepted but leaves no entry, so the website is the way to do it.

## Workshop page

Page text, covers, screenshots and badges live in `workshop/`. Edit `description.en.txt`, `description.zh-CN.txt` and the combined `description.default.txt` together.

`tools/steam_page.py` updates the existing item through the running, signed-in Steam client and EU5's own Steam API library. It reads no credentials and operates no UI. It must run in the desktop session where Steam is running, not over a remote shell. Without write flags it only reads both language variants. Use a new `--output dist/<record>.json` each time, and do not run Python with `-O` (it relies on assertions).

- Inspect: `python -B tools/steam_page.py --output dist/inspect.json`
- Descriptions: `python -B tools/steam_page.py --descriptions --output dist/descriptions.json` — sends title and description for each language together and verifies the readback. Updating a description alone was observed to clear the Simplified Chinese title.
- Artwork: `python -B tools/steam_page.py --assets [--content dist/release-x.y.z/location_descriptions_enhanced] --output dist/assets.json` — updates the main cover and the Chinese supplementary image, keeping screenshots and visibility.
- Badges: `python -B tools/steam_page.py --host-badges --output dist/badges.json` shares the two badge PNGs from Steam Cloud. The cloud file names in `workshop/page.json` back the live description images; do not delete them. Removing a gallery preview breaks old links to it, so never use gallery items as image hosting. `--clean-gallery` removes only old badge previews that no description still references.

The tool does not change visibility, create items or accept terms.

## Rollback

Rebuild a known-good earlier version (or reuse its `dist/release-x.y.z/` folder) and upload it to the same item under a new version number.

## References

- [Steam Workshop implementation](https://partner.steamgames.com/doc/features/workshop/implementation)
- [ISteamUGC](https://partner.steamgames.com/doc/api/ISteamUGC) and [ISteamRemoteStorage](https://partner.steamgames.com/doc/api/ISteamRemoteStorage)
- [Steam Subscriber Agreement](https://store.steampowered.com/subscriber_agreement/) and [Paradox User Agreement](https://legal.paradoxplaza.com/eula)
- [Wikimedia Terms of Use, §7](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use#7._Licensing_of_Content)
