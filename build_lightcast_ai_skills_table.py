#!/usr/bin/env python3
"""Build slim Lightcast AI skills payload for the report.

Uses the new 4-category + tags classification from categorize_ai_skills.py.
"""

from __future__ import annotations

import json
import re
import sqlite3
from pathlib import Path

import numpy as np
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
INPUT_XLSX = BASE_DIR / "ai_skills_2026_lightcast_scraped.xlsx"
OUTPUT_JS = BASE_DIR / "assets" / "lightcast_ai_skills_data.js"
MATCH_SCORES_NPZ = BASE_DIR / "lightcast_aiml" / "ai_skill_match_scores.npz"
EMBEDDINGS_NPZ = BASE_DIR / "lightcast_aiml" / "lightcast_ai_skills_voyage4.npz"
MATCH_THRESHOLD = 0.55
JOBS_DB = BASE_DIR / "jobs_database.db"

CATEGORY_ORDER = [
    "Machine Learning & Predictive AI",
    "Generative AI",
    "Robotics & Autonomous Systems",
    "AI Governance, Risk & Strategy",
]


def clean_text(value: object) -> str:
    if pd.isna(value):
        return ""
    return " ".join(str(value).strip().split())


STOPWORDS = {
    "and", "the", "for", "with", "using", "use", "in", "of", "to",
    "a", "an", "or", "on", "ai", "artificial", "intelligence", "skill", "skills",
}


def tokenize(text: str) -> list[str]:
    return [
        token for token in re.findall(r"[a-zA-Z0-9+#.-]{3,}", text.lower())
        if token not in STOPWORDS
    ]


def split_segments(text: str) -> list[str]:
    raw_parts = re.split(r"[\n\r•]+|(?<=[.!?;])\s+", text)
    segments = []
    for part in raw_parts:
        cleaned = clean_text(part)
        if 20 <= len(cleaned) <= 260:
            segments.append(cleaned)
    return segments


def choose_best_excerpt(
    skill_name: str, text_blocks: list[tuple[str, str]]
) -> tuple[str, str, float, int, int]:
    skill_name_clean = clean_text(skill_name)
    skill_name_lower = skill_name_clean.lower()
    skill_tokens = set(tokenize(skill_name_clean))

    best_excerpt = ""
    best_source = ""
    best_score = -1.0
    best_contains_full = 0
    best_overlap = 0

    for source, text in text_blocks:
        for segment in split_segments(text):
            segment_lower = segment.lower()
            segment_tokens = set(tokenize(segment))
            overlap = len(skill_tokens & segment_tokens)
            contains_full = 1 if skill_name_lower in segment_lower else 0
            contains_partial = sum(1 for token in skill_tokens if token in segment_tokens)
            score = contains_full * 10 + overlap * 3 + contains_partial * 1.5
            if score > best_score:
                best_excerpt = segment
                best_source = source
                best_score = score
                best_contains_full = contains_full
                best_overlap = overlap

    return best_excerpt, best_source, best_score, best_contains_full, best_overlap


def main() -> None:
    df = pd.read_excel(INPUT_XLSX, sheet_name="all_skills")
    df = df[df["retrieve_status"] == "ok"].copy()
    df["skill_id"] = df["skill_id"].astype(str)

    embeddings_npz = np.load(EMBEDDINGS_NPZ, allow_pickle=True)
    embedding_ids = set(str(sid) for sid in embeddings_npz["skill_ids"])
    df = df[df["skill_id"].isin(embedding_ids)].copy()

    rows = []
    for _, row in df.sort_values(
        ["worldbank_ai_skill", "lightcast_name"], ascending=[False, True]
    ).iterrows():
        martins_neto = int(row.get("worldbank_ai_skill", 0) or 0)
        tags_str = clean_text(row.get("tags"))
        tags_list = [t.strip() for t in tags_str.split(";") if t.strip()] if tags_str else []

        rows.append({
            "skill_id": clean_text(row.get("skill_id")),
            "skill_name": clean_text(row.get("lightcast_name")),
            "description": clean_text(row.get("lightcast_description")),
            "primary_category": clean_text(row.get("primary_category")),
            "tags": tags_list,
            "subcategory": clean_text(row.get("lightcast_subcategory")),
            "skill_type": clean_text(row.get("lightcast_type")),
            "martins_neto": martins_neto,
            "lightcast_new": int(not martins_neto),
        })

    row_map = {r["skill_id"]: r for r in rows}

    # ── Category summary ──
    category_summary = {}
    for cat in CATEGORY_ORDER:
        cat_rows = [r for r in rows if r["primary_category"] == cat]
        category_summary[cat] = {
            "count": len(cat_rows),
            "martins_count": sum(r["martins_neto"] for r in cat_rows),
            "new_count": sum(r["lightcast_new"] for r in cat_rows),
        }

    # ── Tag summary ──
    tag_counts: dict[str, int] = {}
    for r in rows:
        for tag in r["tags"]:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    # ── Load match scores ──
    match_npz = np.load(MATCH_SCORES_NPZ, allow_pickle=True)
    matched_skill_ids = embeddings_npz["skill_ids"][match_npz["indices_all"]]
    matched_scores = match_npz["scores_all"]
    matched_job_ids = match_npz["job_ids"]
    valid_mask = matched_scores >= MATCH_THRESHOLD

    conn = sqlite3.connect(JOBS_DB)
    title_rows = conn.execute(
        "SELECT id, title_clean, requirements, responsibilities, description "
        "FROM job_ads WHERE title_clean IS NOT NULL"
    ).fetchall()
    conn.close()
    job_map = {
        int(jid): {
            "title": clean_text(title),
            "requirements": clean_text(req),
            "responsibilities": clean_text(resp),
            "description": clean_text(desc),
        }
        for jid, title, req, resp, desc in title_rows
    }

    ai_postings_total = int(valid_mask.sum())

    # ── Demand by category ──
    cat_demand_counts: dict[str, int] = {}
    cat_skill_counts: dict[str, dict[str, int]] = {}

    # ── Demand by tag ──
    tag_demand_counts: dict[str, int] = {}

    for skill_id_raw in matched_skill_ids[valid_mask]:
        skill_key = str(skill_id_raw)
        row = row_map.get(skill_key)
        if not row:
            continue
        cat = row["primary_category"] or "Unclassified"
        cat_demand_counts[cat] = cat_demand_counts.get(cat, 0) + 1
        cat_skill_counts.setdefault(cat, {})
        cat_skill_counts[cat][skill_key] = cat_skill_counts[cat].get(skill_key, 0) + 1

        for tag in row["tags"]:
            tag_demand_counts[tag] = tag_demand_counts.get(tag, 0) + 1

    # ── Build demand_summary by category ──
    demand_summary = []
    for cat in CATEGORY_ORDER:
        count = cat_demand_counts.get(cat, 0)
        skill_detail = cat_skill_counts.get(cat, {})
        top_skills = []
        for sid, sc in sorted(
            skill_detail.items(), key=lambda x: (-x[1], row_map[x[0]]["skill_name"])
        )[:5]:
            r = row_map[sid]
            top_skills.append({
                "skill_id": sid,
                "skill_name": r["skill_name"],
                "count": int(sc),
                "share_within_category_pct": round(sc / count * 100, 1) if count else 0.0,
                "martins_neto": r["martins_neto"],
            })
        summary = category_summary.get(cat, {"count": 0, "martins_count": 0, "new_count": 0})
        demand_summary.append({
            "category": cat,
            "count": count,
            "share_of_ai_postings_pct": round(count / ai_postings_total * 100, 1) if ai_postings_total else 0.0,
            "skills_in_category": summary["count"],
            "top_skills": top_skills,
        })

    # ── Build tag_demand_summary ──
    tag_demand_summary = []
    for tag, count in sorted(tag_demand_counts.items(), key=lambda x: -x[1]):
        tag_demand_summary.append({
            "tag": tag,
            "count": count,
            "share_of_ai_postings_pct": round(count / ai_postings_total * 100, 1) if ai_postings_total else 0.0,
            "skills_with_tag": tag_counts.get(tag, 0),
        })

    payload = {
        "meta": {
            "count_total": len(rows),
            "count_martins_neto": sum(r["martins_neto"] for r in rows),
            "count_lightcast_new": sum(r["lightcast_new"] for r in rows),
            "category_summary": category_summary,
            "tag_summary": tag_counts,
            "ai_postings_total_expanded": ai_postings_total,
            "match_threshold": MATCH_THRESHOLD,
        },
        "rows": rows,
        "demand_summary": demand_summary,
        "tag_demand_summary": tag_demand_summary,
    }

    OUTPUT_JS.write_text(
        "window.__LIGHTCAST_AI_SKILLS__ = " + json.dumps(payload, ensure_ascii=False) + ";\n",
        encoding="utf-8",
    )
    print(f"Saved {OUTPUT_JS}")
    print(json.dumps(payload["meta"], indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
