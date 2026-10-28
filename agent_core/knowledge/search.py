"""Xếp hạng nút tri thức theo từ khóa: không phân biệt dấu, bỏ chữ nhiễu, trọng số IDF, cụm từ, đồng nghĩa.

Chỉ dùng thư viện chuẩn. Dùng bởi `scripts/knowledge.py query` và hook gợi ý.
"""

from __future__ import annotations

import json
import math
import os
import re
import unicodedata
from typing import Dict, List, Optional, Tuple

STOPWORDS = {
    # tiếng Việt (đã bỏ dấu)
    "cua", "va", "la", "cho", "cac", "mot", "nhung", "de", "khi", "voi", "nay", "nao", "thi", "bi", "duoc", "trong",
    "ve", "tu", "da", "se", "nhu", "co", "can", "phai", "hay", "nen", "o", "ra", "vao", "tren", "duoi", "cung", "rat",
    "hon", "the", "khong", "toi", "minh", "ban", "gi", "sao", "lam", "dung", "cai", "theo", "chi", "mau", "xem",
    # động từ chung của tài liệu kỹ thuật, xuất hiện ở khắp nơi nên không phân biệt được nút
    "thiet", "ke", "viet", "giua", "chung",
    # tiếng Anh
    "a", "an", "of", "to", "for", "in", "on", "and", "or", "is", "how", "do", "i", "my", "with", "when", "what",
}
# Trọng số theo trường của nút.
FIELD_WEIGHTS = {"id": 3.0, "title": 3.0, "keywords": 3.0, "headings": 1.5, "summary": 1.0, "body": 0.4}


def normalize(text: str) -> str:
    text = (text or "").lower().replace("n+1", "nplus1")
    text = unicodedata.normalize("NFD", text).replace("đ", "d")
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", " ", text).strip()


def tokens_of(text: str, drop_stop: bool = True) -> List[str]:
    toks = normalize(text).split()
    if drop_stop:
        kept = [t for t in toks if t not in STOPWORDS and len(t) > 1]
        return kept or toks
    return toks


def load_synonyms(root_dir: str, rel: str = "agents/knowledge/synonyms.json") -> Dict[str, List[str]]:
    path = os.path.join(root_dir, rel)
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = json.load(fh)
    except (OSError, ValueError):
        return {}
    return {normalize(k): tokens_of(v, drop_stop=False) for k, v in raw.items() if not k.startswith("_")}


def _outline(text: str) -> Tuple[str, List[str]]:
    summary = ""
    for line in text.splitlines():
        t = line.strip()
        if not t or t.startswith(("#", ">", "|", "---", "```", "<!--", "- [", "!")):
            continue
        summary = re.sub(r"[`*_]", "", t)[:220]
        break
    heads = [re.sub(r"^#+\s*", "", ln).strip() for ln in text.splitlines() if ln.startswith("## ")]
    return summary, heads


def _field_sets(node, root_dir: str) -> Dict[str, set]:
    body = summary = ""
    heads: List[str] = []
    if node.content_ref:
        path = os.path.join(root_dir, node.content_ref)
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                body = fh.read()
            summary, heads = _outline(body)
    fields = {
        "id": node.id.split(":", 1)[-1].replace("-", " "),
        "title": node.title,
        "keywords": node.raw_data.get("keywords") or "",
        "headings": " ".join(heads),
        "summary": (node.raw_data.get("summary") or "") + " " + summary,
        "body": body,
    }
    return {k: set(normalize(v).split()) for k, v in fields.items()}, {k: " " + normalize(v) + " " for k, v in fields.items()}


def _has(token: str, tokset: set) -> bool:
    if token in tokset:
        return True
    return len(token) >= 4 and any(w.startswith(token) or (len(w) >= 4 and token.startswith(w)) for w in tokset)


def rank(catalog, root_dir: str, query: str, role: Optional[str] = None) -> List[Tuple[int, object]]:
    q_tokens = tokens_of(query)
    if not q_tokens:
        return []
    synonyms = load_synonyms(root_dir)
    q_norm = " " + normalize(query) + " "
    extra: List[str] = []
    for phrase, terms in synonyms.items():
        if f" {phrase} " in q_norm:
            extra += [t for t in terms if t not in q_tokens]
    all_tokens = [(t, 1.0) for t in q_tokens] + [(t, 0.7) for t in dict.fromkeys(extra)]
    bigrams = [f"{a} {b}" for a, b in zip(q_tokens, q_tokens[1:])]

    docs = {}
    for nid, node in catalog.nodes.items():
        docs[nid] = _field_sets(node, root_dir)
    n_docs = max(1, len(docs))

    def idf(token):
        # Độ hiếm tính trên id, tiêu đề, từ khóa, mục, tóm tắt (không tính thân bài, nơi chữ phổ biến xuất hiện ở khắp nơi).
        df = sum(1 for sets, _ in docs.values() if any(_has(token, v) for f, v in sets.items() if f != "body"))
        return math.log(1 + n_docs / max(1, df))

    idf_cache = {t: idf(t) for t, _ in all_tokens}

    scored = []
    for nid, node in catalog.nodes.items():
        sets, texts = docs[nid]
        score, matched = 0.0, 0
        for token, w in all_tokens:
            hit = [FIELD_WEIGHTS[f] for f, s in sets.items() if _has(token, s)]
            if hit:
                matched += 1 if w == 1.0 else 0
                score += idf_cache[token] * w * min(5.0, sum(hit))
        for bg in bigrams:
            if any(bg in texts[f] for f in ("title", "keywords", "headings", "id")):
                score += 3.0
        if score <= 0:
            continue
        score *= (matched / len(q_tokens)) ** 0.5 if matched else 0.5
        if role and (node.owner_role == role or any(r.target == f"Role:{role}" for r in node.relations)):
            score += 1.5
        scored.append((int(round(score * 10)), node))
    scored.sort(key=lambda x: (-x[0], x[1].id))
    return scored
