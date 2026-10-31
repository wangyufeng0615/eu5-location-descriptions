"""Build the text-only EU5 mod using Python's standard library. Never uploads."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
LANGUAGES = ("english", "simp_chinese")
LICENSE_FILES = ("LICENSE", "LICENSES/MIT.txt", "LICENSES/CC-BY-SA-4.0.txt")
PLAYER_DOCUMENTS = {
    "README.md": "workshop/player-readme.en.md",
    "README.zh-CN.md": "workshop/player-readme.zh-CN.md",
    "CONTRIBUTING.md": "CONTRIBUTING.md",
    "CONTRIBUTING.zh-CN.md": "CONTRIBUTING.zh-CN.md",
    "docs/FAQ.md": "docs/FAQ.md",
    "docs/FAQ.zh-CN.md": "docs/FAQ.zh-CN.md",
    "docs/COMPATIBILITY.md": "docs/COMPATIBILITY.md",
}
# Game files shipped as-is. Seas, lakes and impassable locations use their own vanilla tooltips
# without a flavour-text block; this GUI file redefines those two templates with the block added.
GAME_FILES = {
    "in_game/gui/zz_lde_location_tooltips.gui": "workshop/gui/zz_lde_location_tooltips.gui",
}


def project_file(root, relative):
    path = (root / relative).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"Missing or external project file: {relative}")
    return path


def validate_config(config):
    if config.get("mod_id") != "location_descriptions_enhanced" or config.get("game_id") != "eu5" or config.get("steam_app_id") != 3450310:
        raise ValueError("Unexpected or unsafe mod identity")
    title = config.get("name", "")
    if not isinstance(title, str) or not 3 <= len(title) <= 60 or len(title.encode("utf-8")) > 128 or any(ord(c) < 32 for c in title):
        raise ValueError("Invalid EU5/Steam title")
    if not re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", config.get("version", "")):
        raise ValueError("Invalid package version")
    if not isinstance(config.get("short_description"), str) or not config["short_description"].strip() or "\x00" in config["short_description"]:
        raise ValueError("Missing short description")
    if config.get("tags") != ["Historical", "Translation"]:
        raise ValueError("Unexpected EU5 tags")
    if config.get("licenses") != {"tools": "MIT", "descriptions": "CC-BY-SA-4.0"} or config.get("license_status") != "selected":
        raise ValueError("License selection differs from owner instruction")
    if config.get("first_release_languages") != ["english", "simp_chinese"]:
        raise ValueError("First release must include English and Simplified Chinese together")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


def load(root):
    config = json.loads((root / "project.json").read_text(encoding="utf-8"))
    validate_config(config)
    baseline = json.loads((root / "data/baseline.json").read_text(encoding="utf-8"))
    targets = set(baseline["target_ids"])
    protected = set(baseline["protected_ids"])
    if len(targets) != len(baseline["target_ids"]) or len(protected) != len(baseline["protected_ids"]) or targets & protected:
        raise ValueError("Invalid or overlapping baseline IDs")
    records = {}
    for path in sorted((root / "data/descriptions").glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            row = json.loads(line)
            key = row["id"]
            if not re.fullmatch(r"[A-Za-z0-9_]+", key) or key in records or key not in targets:
                raise ValueError(f"Duplicate, official or unknown location ID: {key}")
            if row["review_status"] not in ("bilingual_first_pass", "bilingual_reviewed"):
                raise ValueError(f"Invalid review status: {key}")
            for language in LANGUAGES:
                value = row[language]
                if not isinstance(value, str) or not value.strip() or any(ord(c) < 32 and c not in "\n\r\t" for c in value):
                    raise ValueError(f"Empty or invalid {language} text: {key}")
                if value.startswith(("Research and description pending", "地点 ID ")):
                    raise ValueError(f"Placeholder remains: {key}")
            if not row["sources"]:
                raise ValueError(f"No source attribution: {key}")
            for source in row["sources"]:
                # Sources are any public web page (Wikipedia in many languages, UNESCO, local gazetteers...).
                # Revision pins are kept when the research export provides them, but are not required.
                parsed = urlsplit(source["url"])
                if parsed.scheme not in ("https", "http") or not parsed.hostname or parsed.username or parsed.password:
                    raise ValueError(f"Unexpected source URL: {key}")
                if not source.get("title"):
                    raise ValueError(f"Untitled source: {key}")
                revision = source.get("revision_id")
                if revision is not None and (type(revision) is not int or revision <= 0):
                    raise ValueError(f"Invalid source revision: {key}")
            records[key] = row
    if set(records) != targets:
        raise ValueError(f"Coverage differs from baseline: {len(records)}/{len(targets)}")
    if len(targets) + len(protected) != baseline["map_location_count"]:
        raise ValueError("Map total differs from target/protected sets")
    return config, baseline, [records[key] for key in sorted(records)]


def quote(value):
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("\r", "").replace("\n", "\\n")


def localization_bytes(language, chunk):
    lines = [f"l_{language}:"] + [f' {row["id"]}_desc: "{quote(row[language])}"' for row in chunk]
    return ("\n".join(lines) + "\n").encode("utf-8-sig")


def expected_payload(root, config, rows):
    metadata = {key: config[key] for key in ("name", "version", "game_id", "supported_game_version", "short_description", "tags")}
    metadata.update(id=config["mod_id"], relationships=[], game_custom_data={})
    files = {".metadata/metadata.json": (json.dumps(metadata, ensure_ascii=False, indent=2) + "\n").encode("utf-8")}
    for language in LANGUAGES:
        for offset in range(0, len(rows), 500):
            # in_game/, not main_menu/: main_menu/localization is listed in the game's checksum manifest.
            name = f"in_game/localization/{language}/lde_{offset // 500 + 1:03d}_l_{language}.yml"
            files[name] = localization_bytes(language, rows[offset:offset + 500])
    for name in ("CREDITS.md", "NOTICE.md", *LICENSE_FILES):
        files[name] = project_file(root, name).read_bytes()
    for target, source in GAME_FILES.items():
        files[target] = project_file(root, source).read_bytes()
    for target, source in PLAYER_DOCUMENTS.items():
        files[target] = project_file(root, source).read_bytes()
    files[".metadata/thumbnail.png"] = project_file(root, config["thumbnail_file"]).read_bytes()
    files["ARTWORK.md"] = (
        "# Promotional illustration\n\n"
        "The thumbnail was generated for this project with the built-in image_gen tool on 2026-10-26. "
        "It is an original AI-assisted promotional illustration, not a game screenshot or an official game asset. "
        "The project's MIT tool and CC BY-SA text licenses do not grant a separate blanket reuse license for this artwork. "
        "No endorsement by Valve, Paradox or Wikimedia is implied.\n"
    ).encode("utf-8")
    for offset in range(0, len(rows), 500):
        lines = [json.dumps({"id": row["id"], "sources": row["sources"]}, ensure_ascii=False, sort_keys=True) for row in rows[offset:offset + 500]]
        files[f"sources/sources_{offset // 500 + 1:03d}.jsonl"] = ("\n".join(lines) + "\n").encode("utf-8")
    return files


def verify_payload(root, mod, config, rows):
    expected = expected_payload(root, config, rows)
    actual = {path.relative_to(mod).as_posix() for path in mod.rglob("*") if path.is_file()}
    if actual != set(expected):
        raise ValueError("Unexpected or missing package files")
    for name, content in expected.items():
        path = mod / name
        if path.is_symlink() or path.read_bytes() != content:
            raise ValueError(f"Package differs from editable source: {name}")
    return {name: hashlib.sha256(content).hexdigest() for name, content in sorted(expected.items())}


def verify_build(root, output):
    config, baseline, rows = load(root)
    files = verify_payload(root, output / config["mod_id"], config, rows)
    receipt = json.loads((output / "build_receipt.json").read_text(encoding="utf-8"))
    if receipt["files"] != files:
        raise ValueError("Receipt differs from verified package")
    if receipt["version"] != config["version"] or receipt["baseline_build"] != baseline["steam_build_id"] or receipt["licenses"] != config["licenses"] or receipt["locations_per_language"] != len(rows):
        raise ValueError("Receipt metadata differs from source")
    archive = output / f'{config["mod_id"]}-{config["version"]}.zip'
    if receipt["archive_sha256"] != digest(archive):
        raise ValueError("Archive hash differs from receipt")
    with zipfile.ZipFile(archive) as stream:
        expected_names = {f'{config["mod_id"]}/{name}' for name in files}
        if len(stream.namelist()) != len(expected_names) or set(stream.namelist()) != expected_names or stream.testzip() is not None:
            raise ValueError("Invalid archive file list or CRC")
        for name, sha in files.items():
            if hashlib.sha256(stream.read(f'{config["mod_id"]}/{name}')).hexdigest() != sha:
                raise ValueError(f"Archive member differs: {name}")
    return receipt


def build(root, output):
    root, output = root.resolve(), output.resolve()
    config, baseline, rows = load(root)
    if output.exists():
        raise FileExistsError(f"Choose a new output directory: {output}")
    output.mkdir(parents=True)
    mod = output / config["mod_id"]
    payload = expected_payload(root, config, rows)
    for name, content in payload.items():
        path = mod / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    files = verify_payload(root, mod, config, rows)
    archive = output / f'{config["mod_id"]}-{config["version"]}.zip'
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as stream:
        for name in files:
            entry = zipfile.ZipInfo(f'{config["mod_id"]}/{name}', date_time=(2026, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            stream.writestr(entry, (mod / name).read_bytes(), compresslevel=9)
    receipt = {
        "package_checks_passed": True,
        "publication_ready": False,
        "publication_status": "local_preview_only",
        "pending": ["Third-party text-reuse exceptions review", "Authentic full-text in-game screenshots and smoke test", "GitHub destination and visibility", "Steam private upload and clean subscription test"],
        "licenses": config["licenses"],
        "version": config["version"], "baseline_build": baseline["steam_build_id"],
        "locations_per_language": len(rows), "protected_locations": len(baseline["protected_ids"]),
        "review_status_counts": dict(Counter(row["review_status"] for row in rows)),
        "independent_fact_review_complete": False, "placeholder_count": 0,
        "files": files, "archive_sha256": digest(archive),
    }
    write_json(output / "build_receipt.json", receipt)
    verify_build(root, output)
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Validate source data without building")
    mode.add_argument("--verify", type=Path, help="Re-read an existing built package and ZIP and compare to source")
    parser.add_argument("--output", type=Path, default=ROOT / "dist/preview")
    args = parser.parse_args()
    if args.verify:
        receipt = verify_build(ROOT, args.verify.resolve())
        print(json.dumps({"verified": True, "files": len(receipt["files"]), "archive_sha256": receipt["archive_sha256"]}))
    elif args.check:
        _, baseline, rows = load(ROOT)
        print(json.dumps({"verified": True, "locations_per_language": len(rows), "protected_locations": len(baseline["protected_ids"]), "independent_fact_review_complete": False}))
    else:
        receipt = build(ROOT, args.output)
        print(json.dumps({key: receipt[key] for key in ("package_checks_passed", "publication_ready", "locations_per_language", "archive_sha256")}, indent=2))


if __name__ == "__main__":
    main()
