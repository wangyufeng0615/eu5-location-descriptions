"""Find an exported location by ID, source title or English/Chinese text. Read-only."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import unicodedata

ROOT = Path(__file__).resolve().parents[1]


def normalize(value):
    return " ".join("".join(c for c in unicodedata.normalize("NFKD", value.casefold()) if not unicodedata.combining(c)).replace("_", " ").replace("-", " ").split())


def find(root, query, limit=5):
    query = normalize(query)
    if not query:
        raise ValueError("Enter a location name, ID or text / 请输入名称、ID或文本")
    hits = []
    for path in sorted((root / "data/descriptions").glob("*.jsonl")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            row = json.loads(line)
            key = normalize(row["id"])
            titles = [normalize(s["title"]) for s in row["sources"]]
            score = 100 if key == query else 80 if query in titles else 60 if query in key else 40 if any(query in title for title in titles) else 10 if query in normalize(row["english"] + " " + row["simp_chinese"]) else 0
            if score:
                hits.append({"score": score, "id": row["id"], "file": path.relative_to(root).as_posix(), "line": line_number, "category": row["category"], "english_preview": row["english"][:180], "simp_chinese_preview": row["simp_chinese"][:100]})
    return sorted(hits, key=lambda item: (-item["score"], item["id"]))[:limit]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if not 1 <= args.limit <= 20:
        parser.error("--limit must be between 1 and 20")
    hits = find(ROOT, args.query, args.limit)
    if args.json:
        print(json.dumps(hits, ensure_ascii=False, indent=2))
    else:
        for item in hits:
            print(f"{item['id']} | {item['file']}:{item['line']}\nEN: {item['english_preview']}\n中文: {item['simp_chinese_preview']}\n")
        if not hits:
            print("No match. Try another spelling or a nearby source title. / 未找到，请换译名或相关来源名称。")


if __name__ == "__main__":
    main()
