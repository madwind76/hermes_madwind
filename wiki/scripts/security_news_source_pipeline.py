#!/usr/bin/env python3
"""Aggregate security news source-collection files.

Pipeline goal
-------------
1. Read every `*_security_news_source_collection*.md` file.
2. Extract article rows from both table-based and bullet-based snapshots.
3. Normalize source aliases.
4. Produce two views:
   - raw snapshot totals (row counts across all snapshots)
   - unique-URL totals (deduped by original_article_url)

This script is intentionally dependency-free so it can run in the same
lightweight environment used for wiki maintenance.
"""

from __future__ import annotations

import argparse
import glob
import json
import re
from collections import Counter, OrderedDict, defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable


# Canonical source-name aliases. Keep this list short and explicit so counts do
# not drift when the same outlet appears with multiple labels.
ALIASES = {
    "Fortinet Blog": "Fortinet",
    "Fortinet Blogs": "Fortinet",
    "Fortinet Threat Research": "Fortinet",
    "CISA": "CISA",
    "CISA News": "CISA",
    "National Cyber Security Centre": "UK NCSC",
    "UK NCSC All RSS feeds": "UK NCSC",
    "KISA KrCERT": "KISA KrCERT",
    "KISA KrCERT 보안공지": "KISA KrCERT",
    "KISA KrCERT 취약점 정보": "KISA KrCERT",
}


@dataclass(frozen=True)
class Record:
    """One extracted article row."""

    file: str
    source: str
    url: str


@dataclass
class Summary:
    """Computed totals for both raw and unique views."""

    raw_total: int
    unique_total: int
    raw_counts: Counter
    unique_counts: Counter
    files: list[str]
    normalized_aliases: dict[str, str]


def normalize_source(source: str) -> str:
    """Map source aliases to a canonical outlet name."""

    return ALIASES.get(source, source)


def iter_paths(patterns: list[str]) -> list[Path]:
    """Expand glob patterns and keep only real files."""

    paths: list[Path] = []
    for pattern in patterns:
        for item in glob.glob(pattern):
            p = Path(item)
            # Skip obvious templates/examples so they do not pollute counts.
            if p.is_file() and "example" not in p.name.lower():
                paths.append(p)
    # Stable ordering helps make diffs repeatable.
    return sorted({p.resolve() for p in paths})


def parse_bullet_snapshot(path: Path) -> list[Record]:
    """Parse the older bullet-based snapshot format.

    Expected structure:
      - **source_name:** ...
      - **original_article_url:** ...
    """

    records: list[Record] = []
    current_source: str | None = None

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()

        m = re.match(r"^- \*\*source_name:\*\*\s*(.+?)\s*$", line)
        if m:
            current_source = m.group(1)
            continue

        m = re.match(r"^- \*\*original_article_url:\*\*\s*(.+?)\s*$", line)
        if m and current_source:
            records.append(Record(file=path.name, source=current_source, url=m.group(1)))
            current_source = None

    return records


def parse_table_snapshot(path: Path) -> list[Record]:
    """Parse the table-based snapshot formats.

    Supported row shapes in the current files:
    - Standard article row:
      | 제목 | 매체 | 태그 | 발행일 | 원본 기사 URL | 분류 | 요약 |
    - KISA/KrCERT CVE row:
      | CVE | 제목 | 제목 | 출처 | 발행일 | URL | 분류 | ... |

    The parser does not rely on a fixed number of columns; it looks for the
    table cells that are actually used for source and URL.
    """

    records: list[Record] = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if not raw_line.startswith("|"):
            continue

        cells = [cell.strip() for cell in raw_line.rstrip("\n").split("|")[1:-1] if cell.strip()]
        if not cells or cells[0] in {"제목", "---"}:
            continue

        # KISA-style rows begin with CVE IDs.
        if cells[0].startswith("CVE-"):
            # Current files place the outlet in the 4th logical cell and the URL
            # in the 6th logical cell.
            if len(cells) >= 6:
                source = cells[3]
                url = cells[5]
            else:
                continue
        else:
            # Standard rows place outlet in the 2nd logical cell and URL in the 5th.
            if len(cells) >= 5:
                source = cells[1]
                url = cells[4]
            else:
                continue

        if source.startswith("http") or not url.startswith("http"):
            continue

        records.append(Record(file=path.name, source=source, url=url))

    return records


def parse_file(path: Path) -> list[Record]:
    """Dispatch based on the snapshot format present in the file."""

    text = path.read_text(encoding="utf-8")
    if "- **source_name:**" in text:
        return parse_bullet_snapshot(path)
    return parse_table_snapshot(path)


def build_summary(paths: list[Path]) -> Summary:
    """Build raw and unique totals from a set of source-collection files."""

    raw_counts: Counter[str] = Counter()
    unique_counts: Counter[str] = Counter()
    seen_urls: dict[str, str] = OrderedDict()
    processed_files: list[str] = []

    for path in paths:
        processed_files.append(path.name)
        for record in parse_file(path):
            normalized = normalize_source(record.source)
            raw_counts[normalized] += 1
            # Deduplicate by URL across all snapshots.
            if record.url not in seen_urls:
                seen_urls[record.url] = normalized
                unique_counts[normalized] += 1

    return Summary(
        raw_total=sum(raw_counts.values()),
        unique_total=len(seen_urls),
        raw_counts=raw_counts,
        unique_counts=unique_counts,
        files=processed_files,
        normalized_aliases=ALIASES,
    )


def markdown_report(summary: Summary) -> str:
    """Render a human-readable report for wiki/raw/articles."""

    lines: list[str] = []
    now = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    lines.append("---")
    lines.append("title: Security News Source Summary")
    lines.append(f"generated: {now}")
    lines.append("type: source-summary")
    lines.append("sources: [wiki/scripts/security_news_source_pipeline.py]")
    lines.append("---")
    lines.append("")
    lines.append("# Security News Source Summary")
    lines.append("")
    lines.append("## Processed files")
    for name in summary.files:
        lines.append(f"- {name}")
    lines.append("")
    lines.append("## Totals")
    lines.append(f"- Raw snapshot total: **{summary.raw_total}**")
    lines.append(f"- Unique-URL total: **{summary.unique_total}**")
    lines.append("")
    lines.append("## Unique-URL counts by source")
    lines.append("")
    lines.append("| Source | Count |")
    lines.append("|---|---:|")
    for source, count in summary.unique_counts.most_common():
        lines.append(f"| {source} | {count} |")
    lines.append("")
    lines.append("## Raw snapshot counts by source")
    lines.append("")
    lines.append("| Source | Count |")
    lines.append("|---|---:|")
    for source, count in summary.raw_counts.most_common():
        lines.append(f"| {source} | {count} |")
    lines.append("")
    lines.append("## Alias normalization")
    lines.append("")
    lines.append("| Alias | Canonical |")
    lines.append("|---|---|")
    for alias, canonical in sorted(summary.normalized_aliases.items()):
        lines.append(f"| {alias} | {canonical} |")
    lines.append("")
    return "\n".join(lines)


def json_report(summary: Summary) -> dict:
    """Return a compact JSON-serializable structure."""

    return {
        "generated": datetime.now(timezone.utc).astimezone().isoformat(),
        "raw_total": summary.raw_total,
        "unique_total": summary.unique_total,
        "processed_files": summary.files,
        "unique_counts": dict(summary.unique_counts.most_common()),
        "raw_counts": dict(summary.raw_counts.most_common()),
        "aliases": summary.normalized_aliases,
    }


def now_kst_stamp() -> str:
    """Return a current local timestamp string suitable for frontmatter."""

    return datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")


def render_collection_template(
    title: str,
    created: str,
    updated: str,
    collected_at: str,
    saved_at: str,
    scope: str,
    sources: list[str],
    body_title: str,
) -> str:
    """Render a fresh source-collection markdown template."""

    lines = [
        "---",
        f"title: {title}",
        f"created: {created}",
        f"updated: {updated}",
        f"collected_at: {collected_at}",
        f"saved_at: {saved_at}",
        "type: source-collection",
        f"scope: {scope}",
        f"sources: [{', '.join(sources)}]",
        "---",
        "",
        f"# {body_title}",
        "",
        "> 기준: blogwatcher-cli로 수집한 unread 기사만 사용합니다.",
        "> RSS 피드 URL은 수집 인프라용이며, 아래 표에는 원본 기사 URL만 기록합니다.",
        "",
        "## 수집 결과",
        "",
        "- import: ",
        "- scan: ",
        "- unread_articles: ",
        "",
        "## 기사 목록",
        "",
        "| 제목 | 매체 | 태그 | 발행일 | 원본 기사 URL | 분류 | 요약 |",
        "|---|---|---|---|---|---|---|",
        "",
        "<!-- TODO: 수집된 기사 행을 여기에 추가하세요. -->",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate security news source-collection snapshots.")
    parser.add_argument(
        "--emit-template",
        type=Path,
        help="Write a fresh source-collection template to this path and exit.",
    )
    parser.add_argument(
        "--title",
        help="Title to use when emitting a template.",
    )
    parser.add_argument(
        "--body-title",
        help="Markdown heading to use when emitting a template.",
    )
    parser.add_argument(
        "--created",
        help="created value for emitted templates (defaults to today).",
    )
    parser.add_argument(
        "--updated",
        help="updated value for emitted templates (defaults to today).",
    )
    parser.add_argument(
        "--collected-at",
        dest="collected_at",
        help="collected_at value for emitted templates (defaults to now).",
    )
    parser.add_argument(
        "--saved-at",
        dest="saved_at",
        help="saved_at value for emitted templates (defaults to now).",
    )
    parser.add_argument(
        "--scope",
        default="blogwatcher-12h",
        help="Scope value for emitted templates.",
    )
    parser.add_argument(
        "--source",
        dest="sources",
        action="append",
        help="Source label for emitted templates. Repeatable.",
    )
    parser.add_argument(
        "--input-glob",
        action="append",
        default=["/home/kisec/wiki/raw/articles/*security_news_source_collection*.md"],
        help="Glob pattern(s) for source-collection markdown files.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional markdown output path.",
    )
    parser.add_argument(
        "--json-output",
        type=Path,
        help="Optional JSON output path.",
    )
    args = parser.parse_args()

    if args.emit_template:
        today = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d")
        title = args.title or f"{today.replace('-', '')} Security News Source Collection"
        body_title = args.body_title or title.replace(" Security News Source Collection", " 보안 뉴스 수집본")
        created = args.created or today
        updated = args.updated or today
        collected_at = args.collected_at or now_kst_stamp()
        saved_at = args.saved_at or now_kst_stamp()
        sources = args.sources or ["blogwatcher-cli", "direct-rss"]
        template = render_collection_template(
            title=title,
            created=created,
            updated=updated,
            collected_at=collected_at,
            saved_at=saved_at,
            scope=args.scope,
            sources=sources,
            body_title=body_title,
        )
        args.emit_template.parent.mkdir(parents=True, exist_ok=True)
        args.emit_template.write_text(template + "\n", encoding="utf-8")
        print(args.emit_template)
        return 0

    paths = iter_paths(args.input_glob)
    if not paths:
        raise SystemExit("No matching source-collection files were found.")

    summary = build_summary(paths)

    report = markdown_report(summary)
    print(report)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")

    if args.json_output:
        args.json_output.parent.mkdir(parents=True, exist_ok=True)
        args.json_output.write_text(json.dumps(json_report(summary), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
