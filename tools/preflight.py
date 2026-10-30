"""Check local publication materials and a built package. Does not upload or approve release."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import struct

try:
    from tools import build as mod_build
except ModuleNotFoundError:
    import build as mod_build

ROOT = Path(__file__).resolve().parents[1]
# /home/ and /Users/ only count at the start of a path, not inside a URL such as https://example.org/en/home/science/.
PERSONAL_PATH_RE = r"(?:[A-Z]:[\\/](?:Users|UserData)[\\/]|(?<![\w.%/-])/Users/|(?<![\w.%/-])/home/)[A-Za-z0-9_.-]+[\\/]"
EVIDENCE_CHECKS = {
    "in_game_english": "English in-game display and screenshot",
    "in_game_simp_chinese": "Simplified Chinese in-game display and screenshot",
    "long_text_and_special_locations": "Long text, water and special-location checks",
    "official_text_preserved": "Official descriptions preserved in game",
    "source_rights_exceptions": "Exceptional source notices and protected quotations reviewed",
    "steam_account_terms": "Steam eligibility, terms and any required confirmation",
    "steam_private_subscription": "Private upload and real subscribed-package verification",
    "github_upload": "GitHub source upload and access verified",
}


def check_launch_materials(root, page):
    if page.get("game_languages") != {"english": "english", "schinese": "simp_chinese"}:
        raise ValueError("Steam/game language mapping is incomplete")
    if "cover_images" in page and (not isinstance(page["cover_images"], dict) or set(page["cover_images"]) != {"english", "schinese"}):
        raise ValueError("Configured page artwork must include both English and Simplified Chinese")
    required = ("README.md", "README.zh-CN.md", "CONTRIBUTING.md", "CONTRIBUTING.zh-CN.md", "docs/FAQ.md", "docs/FAQ.zh-CN.md", "docs/COMPATIBILITY.md", *mod_build.PLAYER_DOCUMENTS.values(), "workshop/announcement.en.txt", "workshop/announcement.zh-CN.txt", "workshop/changenotes.en.txt", "workshop/changenotes.zh-CN.txt")
    for name in required:
        if not mod_build.project_file(root, name).read_text(encoding="utf-8").strip():
            raise ValueError(f"Empty launch material: {name}")
    return len(set(required))


def check_release_evidence(path, receipt):
    if path is None:
        return {"provided": False, "all_recorded": False, "pending": list(EVIDENCE_CHECKS.values()), "independently_verified_by_tool": False}
    evidence = json.loads(path.read_text(encoding="utf-8"))
    if evidence.get("schema_version") != 1 or evidence.get("archive_sha256") != receipt["archive_sha256"] or evidence.get("mod_version") != receipt["version"] or evidence.get("game_build") != receipt["baseline_build"]:
        raise ValueError("Manual evidence does not identify this exact package and baseline")
    pending = []
    for key, label in EVIDENCE_CHECKS.items():
        item = evidence.get("checks", {}).get(key, {})
        if item.get("status") != "passed":
            pending.append(label)
            continue
        relative = item.get("record_file")
        expected = item.get("sha256")
        if not isinstance(relative, str) or not isinstance(expected, str):
            raise ValueError(f"Passed check has no evidence reference: {key}")
        record = (path.parent / relative).resolve()
        if not record.is_relative_to(path.parent.resolve()) or record.is_symlink() or not record.is_file() or mod_build.digest(record) != expected:
            raise ValueError(f"Missing, changed or external manual evidence: {key}")
    if not pending and not re.fullmatch(r"[1-9][0-9]*", str(evidence.get("workshop_item_id", ""))):
        raise ValueError("Completed private-upload evidence needs a real Workshop item ID")
    return {"provided": True, "all_recorded": not pending, "pending": pending, "independently_verified_by_tool": False}


def image_size(path):
    data = path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n") and data[12:16] == b"IHDR":
        return struct.unpack(">II", data[16:24])
    if not data.startswith(b"\xff\xd8"):
        raise ValueError(f"Unsupported or invalid image: {path.name}")
    position = 2
    while position < len(data):
        if data[position] != 255:
            raise ValueError("Invalid JPEG structure")
        while data[position] == 255:
            position += 1
        marker = data[position]
        position += 1
        if marker in (0xD9, 0xDA):
            break
        length = int.from_bytes(data[position:position + 2], "big")
        if length < 2:
            raise ValueError("Invalid JPEG segment")
        if marker in (0xC0, 0xC1, 0xC2):
            height, width = struct.unpack(">HH", data[position + 3:position + 7])
            return width, height
        position += length
    raise ValueError("JPEG dimensions not found")


def check_bbcode(value):
    stack = []
    for match in re.finditer(r"\[(/?)(h1|h2|h3|b|i|u|url)(?:=[^\]]+)?\]", value):
        closing, tag = match.group(1, 2)
        if closing:
            if not stack or stack.pop() != tag:
                raise ValueError("Unbalanced Workshop BBCode")
        else:
            stack.append(tag)
    if stack:
        raise ValueError("Unclosed Workshop BBCode")


def source_files(root):
    ignored = {".git", "dist", "__pycache__", ".pytest_cache"}
    return [p for p in root.rglob("*") if not (set(p.relative_to(root).parts) & ignored) and (p.is_file() or p.is_symlink())]


def check(root, output, game_root=None, evidence_path=None):
    config, baseline, rows = mod_build.load(root)
    receipt = mod_build.verify_build(root, output)
    for name in mod_build.LICENSE_FILES:
        mod_build.project_file(root, name)
    page = json.loads((root / "workshop/page.json").read_text(encoding="utf-8"))
    launch_count = check_launch_materials(root, page)
    manual = check_release_evidence(evidence_path, receipt)
    if page["initial_visibility"] != 2 or page["tags"] != config["tags"]:
        raise ValueError("Initial publication settings must use private visibility and the selected tags")
    if set(page["titles"]) != {"english", "schinese"} or set(page["descriptions"]) != set(page["titles"]):
        raise ValueError("Steam page languages differ from intended English/Simplified Chinese")
    page_metrics = {}
    for language, title in page["titles"].items():
        if not title.strip() or len(title.encode("utf-8")) > 128:
            raise ValueError("Workshop title exceeds the Steam UTF-8 byte limit")
        text = mod_build.project_file(root, page["descriptions"][language]).read_text(encoding="utf-8")
        if not text.strip() or len(text.encode("utf-8")) >= 8000:
            raise ValueError("Workshop description exceeds the conservative 7999-byte budget")
        check_bbcode(text)
        page_metrics[language] = {"title_utf8_bytes": len(title.encode("utf-8")), "description_utf8_bytes": len(text.encode("utf-8"))}
    fallback = mod_build.project_file(root, page["fallback_description"]).read_text(encoding="utf-8")
    if len(fallback.encode("utf-8")) >= 8000:
        raise ValueError("Combined bilingual fallback description exceeds byte budget")
    for name in page["descriptions"].values():
        if mod_build.project_file(root, name).read_text(encoding="utf-8").strip() not in fallback:
            raise ValueError("Combined page copy is stale")
    check_bbcode(fallback)
    artwork = {}
    image_files = [("cover", config["cover_file"]), ("thumbnail", config["thumbnail_file"])]
    image_files.extend((f"page_{language}", name) for language, name in page.get("cover_images", {}).items() if name != config["cover_file"])
    for label, name in image_files:
        path = mod_build.project_file(root, name)
        width, height = image_size(path)
        # Project budgets, stricter than an unverified game-specific primary-image limit.
        if width != height or width < 512 or path.stat().st_size >= 1_000_000:
            raise ValueError(f"{label} exceeds the project's square-image / sub-1MB budget")
        artwork[label] = {"width": width, "height": height, "bytes": path.stat().st_size, "sha256": mod_build.digest(path)}
    files = source_files(root)
    link_count = 0
    for path in files:
        if path.is_symlink() or path.suffix in (".sqlite3", ".bundle", ".gz", ".exe", ".dll") or path.stat().st_size >= 100 * 1024 * 1024:
            raise ValueError(f"Non-source or oversized file in repository: {path.relative_to(root)}")
        if path.suffix.lower() in (".jpg", ".png", ".jpeg"):
            continue
        text = path.read_text(encoding="utf-8-sig")
        for name, pattern in (
            ("private key", r"-----BEGIN (?:OPENSSH |RSA |EC )?PRIVATE KEY-----"),
            ("credential token", r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{30,}|sk-[A-Za-z0-9_-]{32,})\b"),
            ("personal path", PERSONAL_PATH_RE),
        ):
            if re.search(pattern, text):
                raise ValueError(f"Possible {name} in {path.relative_to(root)}; matched value suppressed")
        if path.suffix == ".md":
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", text):
                if target.startswith(("https://", "http://", "#")):
                    continue
                mapped = {source: target for target, source in mod_build.PLAYER_DOCUMENTS.items()}.get(path.relative_to(root).as_posix())
                link_base = (output / config["mod_id"] / mapped).parent if mapped else path.parent
                if not (link_base / target.split("#")[0].strip("<>")).exists():
                    raise ValueError(f"Broken local Markdown link in {path.relative_to(root)}")
                link_count += 1
    game = {"checked": False}
    if game_root:
        hashes = {}
        for name, expected in baseline["source_file_sha256"].items():
            relative = Path(name.replace("\\", "/"))
            if relative.parts[0] != "game":
                relative = Path("game") / relative
            source = (game_root / relative).resolve()
            if not source.is_relative_to(game_root.resolve()):
                raise ValueError("Game fingerprint path escapes installation root")
            hasher = hashlib.sha256()
            with source.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    hasher.update(block)
            if hasher.hexdigest() != expected:
                raise ValueError(f"Game source changed: {name}")
            hashes[name] = expected
        steam_manifest = game_root.parents[1] / "appmanifest_3450310.acf"
        installed_build = re.search(r'"buildid"\s+"(\d+)"', steam_manifest.read_text(encoding="utf-8"))
        if not installed_build or installed_build.group(1) != baseline["steam_build_id"]:
            raise ValueError("Installed Steam build differs from the frozen baseline")
        game = {"checked": True, "steam_build_id": installed_build.group(1), "source_files_matched": len(hashes)}
    return {
        "local_checks_passed": True, "publication_ready": manual["all_recorded"],
        "readiness_scope": "Local validation plus owner-supplied records; no publication action is authorized by this report",
        "manual_evidence": manual, "bilingual_launch_materials_checked": launch_count,
        "licenses": config["licenses"], "locations_per_language": len(rows), "protected_locations": len(baseline["protected_ids"]),
        "source_associations": sum(len(row["sources"]) for row in rows),
        "review_status_counts": dict(Counter(row["review_status"] for row in rows)),
        "independent_fact_review_complete": False,
        "package_files": len(receipt["files"]), "archive_sha256": receipt["archive_sha256"],
        "source_file_count": len(files), "source_total_bytes": sum(p.stat().st_size for p in files),
        "page_metrics": page_metrics, "fallback_description_utf8_bytes": len(fallback.encode("utf-8")),
        "artwork": artwork, "local_markdown_links_checked": link_count,
        "credential_pattern_findings": 0, "pattern_scan_is_exhaustive": False, "game_baseline": game,
        "manual_checks_pending": manual["pending"],
        "github_uploaded": "not_checked_by_this_tool", "workshop_uploaded": "not_checked_by_this_tool",
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", required=True, type=Path)
    parser.add_argument("--game-root", type=Path, help="Optional installed EU5 root; only reads seven baseline files and Steam manifest")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--evidence", type=Path, help="Owner-supplied records for this exact package; never generated as passed by this tool")
    parser.add_argument("--require-publish-ready", action="store_true", help="Exit nonzero while manual/external checks remain")
    args = parser.parse_args()
    if args.output and args.output.exists():
        raise FileExistsError("Choose a new preflight report path")
    report = check(ROOT, args.build.resolve(), args.game_root.resolve() if args.game_root else None, args.evidence.resolve() if args.evidence else None)
    if args.output:
        mod_build.write_json(args.output, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.require_publish_ready and not report["publication_ready"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
