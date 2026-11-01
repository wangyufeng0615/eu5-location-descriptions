"""Prepare a release: set the version, add a CHANGELOG entry, run every check and build.

    python -B tools/release.py 1.2.3 --note "Fix the pigment name in Wallerfangen."
    python -B tools/release.py 1.2.3 --notes-file notes.txt --game-root "<EU5 install>" --install --commit
    python -B tools/release.py --dry-run

Uploading stays manual: the script prints the folder to give EU5's Mod Tools.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOD_ID = "location_descriptions_enhanced"
VERSION_RE = re.compile(r"[0-9]+\.[0-9]+\.[0-9]+")
CHANGELOG_HEAD = "# Changelog\n\n"


def parse_version(text: str) -> tuple[int, int, int]:
    if not VERSION_RE.fullmatch(text):
        raise ValueError(f"Version must be plain x.y.z, got {text!r}")
    return tuple(int(part) for part in text.split("."))


def set_project_version(text: str, old: str, new: str) -> str:
    pattern = re.compile(r'("version"\s*:\s*")' + re.escape(old) + '"')
    result, count = pattern.subn(lambda m: m.group(1) + new + '"', text)
    if count != 1:
        raise ValueError("project.json must contain exactly one version field")
    return result


def add_changelog_entry(text: str, version: str, date: str, notes: list[str]) -> str:
    if not text.startswith(CHANGELOG_HEAD):
        raise ValueError("CHANGELOG.md must start with '# Changelog' and a blank line")
    if re.search(rf"^## {re.escape(version)}\b", text, re.M):
        raise ValueError(f"CHANGELOG.md already has an entry for {version}")
    if not notes or not all(note.strip() for note in notes):
        raise ValueError("At least one non-empty --note is required")
    entry = f"## {version} — {date}\n\n" + "".join(f"- {note.strip()}\n" for note in notes) + "\n"
    return CHANGELOG_HEAD + entry + text[len(CHANGELOG_HEAD):]


def commit_subject(note: str, limit: int = 72) -> str:
    """First sentence of a CHANGELOG note, short enough for a commit subject."""
    first = re.split(r"(?<=[.!?:])\s", note.strip(), maxsplit=1)[0].rstrip(".:")
    return first if len(first) <= limit else first[: limit - 1].rstrip() + "…"


def tree_hashes(root: Path) -> dict[str, str]:
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(root.rglob("*")) if path.is_file()
    }


def is_mod_folder(path: Path) -> bool:
    metadata = path / ".metadata" / "metadata.json"
    try:
        return json.loads(metadata.read_text(encoding="utf-8-sig")).get("id") == MOD_ID
    except (OSError, ValueError):
        return False


def mirror(source: Path, target: Path) -> None:
    """Replace target with a copy of source. Only an existing copy of this mod is ever removed."""
    if target.exists():
        if not is_mod_folder(target):
            raise ValueError(f"{target} exists but is not a copy of {MOD_ID}; not replacing it")
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    if tree_hashes(source) != tree_hashes(target):
        raise RuntimeError(f"Installed copy at {target} differs from the build")


def default_install_dir() -> Path:
    home = Path(os.environ.get("USERPROFILE") or Path.home())
    return home / "Documents" / "Paradox Interactive" / "Europa Universalis V" / MOD_ID


def run_python(*args: str, capture: bool = False) -> str:
    print("+ python -B " + " ".join(args), flush=True)
    result = subprocess.run([sys.executable, "-B", *args], cwd=ROOT, check=True, text=True,
                            stdout=subprocess.PIPE if capture else None)
    return result.stdout or ""


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, text=True, stdout=subprocess.PIPE).stdout


def check_git_clean_except_data() -> None:
    dirty = [line[3:] for line in git("status", "--porcelain").splitlines()]
    other = [path for path in dirty if not path.startswith("data/")]
    if other:
        raise SystemExit("Uncommitted changes outside data/: " + ", ".join(other))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("version", nargs="?", help="new version, plain x.y.z")
    parser.add_argument("--note", action="append", default=[], help="CHANGELOG line in English; repeat for several")
    parser.add_argument("--notes-file", type=Path, help="UTF-8 file with one CHANGELOG line per non-empty line")
    parser.add_argument("--game-root", type=Path, help="EU5 install folder, to compare game files in the preflight check")
    parser.add_argument("--install", action="store_true", help="mirror the built mod folder into EU5's user mod folder")
    parser.add_argument("--install-dir", type=Path, default=None, help="override the folder used by --install")
    parser.add_argument("--commit", action="store_true", help="commit project.json, CHANGELOG.md and data/")
    parser.add_argument("--dry-run", action="store_true", help="check and build only; change nothing")
    args = parser.parse_args()
    if args.notes_file:
        args.note += [line.strip() for line in args.notes_file.read_text(encoding="utf-8-sig").splitlines() if line.strip()]

    project_path, changelog_path = ROOT / "project.json", ROOT / "CHANGELOG.md"
    project_text = project_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    changelog_text = changelog_path.read_text(encoding="utf-8").replace("\r\n", "\n")
    current = json.loads(project_text)["version"]

    if args.dry_run:
        if args.install or args.commit:
            raise SystemExit("--dry-run cannot be combined with --install or --commit")
        version = current
        output = ROOT / "dist" / f"dryrun-{datetime.datetime.now():%Y%m%d-%H%M%S}"
    else:
        if not args.version:
            raise SystemExit("Give the new version, or use --dry-run")
        if parse_version(args.version) <= parse_version(current):
            raise SystemExit(f"{args.version} is not newer than the current {current}")
        version = args.version
        output = ROOT / "dist" / f"release-{version}"
        if args.commit:
            check_git_clean_except_data()
        new_changelog = add_changelog_entry(changelog_text, version, datetime.date.today().isoformat(), args.note)
        new_project = set_project_version(project_text, current, version)
    preflight_output = output.with_name(output.name + "-preflight.json")
    for path in (output, preflight_output):
        if path.exists():
            raise SystemExit(f"{path.relative_to(ROOT)} already exists; builds never overwrite earlier output")

    if not args.dry_run:
        project_path.write_text(new_project, encoding="utf-8", newline="")
        changelog_path.write_text(new_changelog, encoding="utf-8", newline="")
    try:
        run_python("-m", "unittest", "discover", "-s", "tests")
        run_python("tools/build.py", "--check")
        run_python("tools/build.py", "--output", str(output))
        verified = json.loads(run_python("tools/build.py", "--verify", str(output), capture=True))
        preflight = ["tools/preflight.py", "--build", str(output), "--output", str(preflight_output)]
        if args.game_root:
            preflight += ["--game-root", str(args.game_root)]
        run_python(*preflight, capture=True)
        report = json.loads(preflight_output.read_text(encoding="utf-8"))
        if not report.get("local_checks_passed"):
            raise RuntimeError("Preflight local checks did not pass")
    except BaseException:
        if not args.dry_run:
            project_path.write_text(project_text, encoding="utf-8", newline="")
            changelog_path.write_text(changelog_text, encoding="utf-8", newline="")
            print("Restored project.json and CHANGELOG.md", file=sys.stderr)
        raise

    mod_folder = output / MOD_ID
    files = [path for path in mod_folder.rglob("*") if path.is_file()]
    summary = {
        "version": version,
        "build": str(output.relative_to(ROOT)),
        "files": len(files),
        "bytes": sum(path.stat().st_size for path in files),
        "archive_sha256": verified["archive_sha256"],
        "locations_per_language": report.get("locations_per_language"),
        "game_files_matched": (report.get("game_baseline") or {}).get("source_files_matched"),
        "upload_folder": str(mod_folder),
    }
    if args.install:
        target = args.install_dir or default_install_dir()
        mirror(mod_folder, target)
        summary["upload_folder"] = str(target)
    if args.commit:
        git("add", "project.json", "CHANGELOG.md", "data")
        git("commit", "-q", "-m", f"Version {version}: {commit_subject(args.note[0])}")
        summary["commit"] = git("rev-parse", "--short", "HEAD").strip()
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
