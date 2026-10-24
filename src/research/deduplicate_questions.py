"""
Question Deduplication Module
Implements string normalization, exact duplicate detection, and token-based near-duplicate detection.
Preserves original wording and source references.
Follows IncuBrix 2027 Growth Engineer Phase 1 specifications.
"""

import re
import string
from typing import List, Dict, Any, Tuple, Set
import pandas as pd


def normalize_question_text(text: str) -> str:
    """
    Normalizes a question string for canonical comparison:
    - Lowercase
    - Removes punctuation and symbols
    - Normalizes internal whitespace to single spaces
    - Strips leading/trailing whitespace
    """
    if not isinstance(text, str):
        return ""
    # Lowercase
    cleaned = text.lower().strip()
    # Replace punctuation with spaces
    cleaned = re.sub(r"[^\w\s]", " ", cleaned)
    # Collapse multiple whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned


def tokenize_question(text: str, remove_stopwords: bool = True) -> Set[str]:
    """
    Tokenizes normalized question text into a word set, optionally removing common interrogative stopwords.
    """
    normalized = normalize_question_text(text)
    raw_tokens = normalized.split()
    tokens = set()
    stopwords = {
        "a", "an", "the", "in", "on", "at", "to", "for", "of", "with",
        "is", "are", "can", "how", "what", "why", "which", "do", "does",
        "and", "or", "from", "by"
    } if remove_stopwords else set()

    for t in raw_tokens:
        if t in stopwords:
            continue
        # Lightweight suffix stemming for plurals (e.g. videos -> video, tools -> tool)
        if len(t) > 3 and t.endswith("s") and not t.endswith("ss"):
            t = t[:-1]
        tokens.add(t)
    return tokens


def calculate_jaccard_similarity(text1: str, text2: str) -> float:
    """
    Calculates Jaccard similarity between two question token sets:
    J(A, B) = |A ∩ B| / |A ∪ B|
    """
    tokens1 = tokenize_question(text1)
    tokens2 = tokenize_question(text2)
    if not tokens1 or not tokens2:
        return 0.0
    intersection = tokens1.intersection(tokens2)
    union = tokens1.union(tokens2)
    return len(intersection) / len(union)


def deduplicate_dataset(
    df: pd.DataFrame,
    similarity_threshold: float = 0.85
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Identifies exact and near duplicates in a DataFrame of questions.
    Returns:
        - deduplicated DataFrame (first occurrence preserved)
        - duplicate analysis report dictionary
    """
    if df.empty:
        return df, {"total": 0, "unique": 0, "exact_duplicates": [], "near_duplicates": []}

    df_work = df.copy()
    question_col = "question_text" if "question_text" in df_work.columns else "question"
    id_col = "question_id" if "question_id" in df_work.columns else "id"

    # Compute normalized text
    df_work["normalized_text"] = df_work[question_col].apply(normalize_question_text)

    # 1. Exact Duplicates
    seen_normalized: Dict[str, str] = {}
    exact_duplicate_indices: List[int] = []
    exact_duplicates_info: List[Dict[str, Any]] = []

    for idx, row in df_work.iterrows():
        norm = row["normalized_text"]
        q_id = str(row[id_col])
        orig_text = str(row[question_col])

        if norm in seen_normalized:
            exact_duplicate_indices.append(idx)
            exact_duplicates_info.append({
                "duplicate_id": q_id,
                "original_id": seen_normalized[norm],
                "duplicate_text": orig_text,
                "normalized": norm
            })
        else:
            seen_normalized[norm] = q_id

    # 2. Near Duplicates (Semantic / Jaccard similarity on non-exact duplicates)
    near_duplicates_info: List[Dict[str, Any]] = []
    unique_rows = df_work.drop(exact_duplicate_indices)
    rows_list = unique_rows[[id_col, question_col, "normalized_text"]].to_dict(orient="records")

    for i in range(len(rows_list)):
        for j in range(i + 1, len(rows_list)):
            q1 = rows_list[i]
            q2 = rows_list[j]
            sim = calculate_jaccard_similarity(q1[question_col], q2[question_col])
            if sim >= similarity_threshold:
                near_duplicates_info.append({
                    "id_1": q1[id_col],
                    "text_1": q1[question_col],
                    "id_2": q2[id_col],
                    "text_2": q2[question_col],
                    "similarity": round(sim, 3)
                })

    # Drop exact duplicates from result
    cleaned_df = df_work.drop(exact_duplicate_indices).drop(columns=["normalized_text"]).reset_index(drop=True)

    report = {
        "total_records": len(df),
        "unique_records": len(cleaned_df),
        "exact_duplicates_count": len(exact_duplicates_info),
        "near_duplicates_count": len(near_duplicates_info),
        "exact_duplicates": exact_duplicates_info,
        "near_duplicates": near_duplicates_info,
    }

    return cleaned_df, report


if __name__ == "__main__":
    from src.research.collect_questions import get_verified_questions

    df = pd.DataFrame(get_verified_questions())
    cleaned, report = deduplicate_dataset(df)
    print(f"Total: {report['total_records']}, Unique: {report['unique_records']}")
    print(f"Exact duplicates found: {report['exact_duplicates_count']}")
    print(f"Near duplicates found (threshold 0.85): {report['near_duplicates_count']}")
