"""Prepare bilingual Workshop copy, offline previews and a private test config. Never uploads."""
from __future__ import annotations

import argparse
import base64
import html
import json
from pathlib import Path
import re
import shutil

try:
    from tools import build, preflight
except ModuleNotFoundError:
    import build
    import preflight

ROOT = Path(__file__).resolve().parents[1]


def render_bbcode(text):
    preflight.check_bbcode(text)
    rendered = html.escape(text)
    for tag in ("h1", "h2", "h3", "b", "i", "u"):
        rendered = rendered.replace(f"[{tag}]", f"<{tag}>").replace(f"[/{tag}]", f"</{tag}>")
    return rendered.replace("\n", "<br>\n")


def page_html(title, text, language, image):
    return ('<!doctype html><html lang="' + language + '"><meta charset="utf-8"><title>' + html.escape(title) + '</title>'
            '<style>body{max-width:1060px;margin:40px auto;padding:20px;color:#25282a;background:#f8f8f6;font:17px/1.75 "Segoe UI","Microsoft YaHei",sans-serif}h1{font-size:30px}h2{font-size:23px;margin-top:28px}img{float:right;width:240px;margin:18px 0 30px 36px}aside{font-size:13px;color:#666;border-bottom:1px solid #bbb;padding-bottom:12px;margin-bottom:20px}</style>'
            '<aside>Local copy preview / 本地文案预览 · Not a published Steam page or game screenshot</aside>'
            '<img alt="Mod cover" src="data:image/jpeg;base64,' + image + '">' + render_bbcode(text) + '</html>')


def quote_vdf(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def prepare(root, candidate, output):
    if output.exists():
        raise FileExistsError("Choose a new launch-pack directory")
    if output.resolve().is_relative_to(candidate.resolve()):
        raise ValueError("Launch copy must be outside the candidate directory")
    report = preflight.check(root, candidate)
    config = json.loads((root / "project.json").read_text(encoding="utf-8"))
    page = json.loads((root / "workshop/page.json").read_text(encoding="utf-8"))
    receipt = build.verify_build(root, candidate)
    output.mkdir(parents=True)
    image = base64.b64encode(build.project_file(root, config["cover_file"]).read_bytes()).decode("ascii")
    languages = {"english": "en", "schinese": "zh-CN"}
    for steam_language, html_language in languages.items():
        text = build.project_file(root, page["descriptions"][steam_language]).read_text(encoding="utf-8")
        (output / f"workshop-{steam_language}.html").write_text(page_html(page["titles"][steam_language], text, html_language, image), encoding="utf-8")
    fallback = build.project_file(root, page["fallback_description"]).read_text(encoding="utf-8")
    (output / "workshop-bilingual.html").write_text(page_html(config["name"], fallback, "en", image), encoding="utf-8")
    copy_files = list(page["descriptions"].values()) + [page["fallback_description"], "workshop/announcement.en.txt", "workshop/announcement.zh-CN.txt", "workshop/changenotes.en.txt", "workshop/changenotes.zh-CN.txt"]
    copy_files += [p.relative_to(root).as_posix() for p in sorted((root / "workshop/discussions").glob("*.txt"))]
    for name in copy_files:
        target = output / name.removeprefix("workshop/")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / name, target)
    published_id = page.get("publishedfileid") or "0"
    if not re.fullmatch(r"0|[1-9][0-9]*", str(published_id)):
        raise ValueError("Invalid stored Workshop item ID")
    fields = {"appid": str(config["steam_app_id"]), "publishedfileid": str(published_id), "contentfolder": (candidate / config["mod_id"]).as_posix(), "previewfile": (root / config["cover_file"]).as_posix(), "visibility": "2", "title": page["titles"]["english"], "description": fallback.replace("\n", " "), "changenote": config["version"] + " — English and Simplified Chinese alpha; private validation"}
    (output / "private-test.local.vdf").write_text('// SteamCMD TEST FALLBACK ONLY. No credentials. Preserve the actual item ID after first upload.\n"workshopitem"\n{\n' + "".join("    " + quote_vdf(k) + " " + quote_vdf(v) + "\n" for k, v in fields.items()) + "}\n", encoding="utf-8")
    evidence = {"schema_version": 1, "archive_sha256": receipt["archive_sha256"], "mod_version": receipt["version"], "game_build": receipt["baseline_build"], "workshop_item_id": page.get("publishedfileid"), "checks": {key: {"status": "pending", "record_file": None, "sha256": None} for key in preflight.EVIDENCE_CHECKS}}
    build.write_json(output / "release-evidence.json", evidence)
    manifest = {"display_name": config["name"], "version": config["version"], "archive_sha256": receipt["archive_sha256"], "game_build": receipt["baseline_build"], "one_workshop_item_for_both_languages": True, "steam_to_game_languages": page["game_languages"], "initial_visibility": "private", "publishedfileid": page.get("publishedfileid"), "github_url": page.get("github_url"), "local_checks_passed": True, "publication_ready": False, "operations_performed": ["local_files_only"], "files_sha256": {p.relative_to(output).as_posix(): build.digest(p) for p in sorted(output.rglob("*")) if p.is_file()}}
    build.write_json(output / "launch-manifest.json", manifest)
    build.write_json(output / "local-preflight.json", report)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--build", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    manifest = prepare(ROOT, args.build.resolve(), args.output.resolve())
    print(json.dumps({key: manifest[key] for key in ("display_name", "version", "archive_sha256", "one_workshop_item_for_both_languages", "local_checks_passed", "publication_ready")}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
