"""
IncuBrix Citation Engine: Target Validator (Phase 5)
Validates completeness, URL syntax, ID formatting, uniqueness, and question mapping
for all 30 third-party citation opportunities.
"""

from typing import List, Dict, Any, Tuple
import re
from urllib.parse import urlparse
import pandas as pd


REQUIRED_FIELDS = [
    "target_id",
    "publisher_name",
    "page_title",
    "page_url",
    "page_type",
    "related_question_ids",
    "target_question",
    "market",
    "discovery_method",
    "observed_in_google",
    "observed_in_ai_answer",
    "citation_evidence",
    "competing_brands_mentioned",
    "page_relevance",
    "editorial_context",
    "potential_inclusion_angle",
    "suggested_ethical_action",
    "priority",
    "date_checked",
    "evidence_reference",
    "verification_status"
]

VALID_PRIORITIES = {"Critical", "High", "Medium", "Low"}


class TargetValidator:
    """Validates citation targets and imported CSV records."""

    @staticmethod
    def validate_url(url: str) -> bool:
        """Validates that a URL is well-formed with scheme and netloc."""
        if not url or not isinstance(url, str):
            return False
        parsed = urlparse(url)
        return bool(parsed.scheme in ("http", "https") and parsed.netloc)

    @classmethod
    def validate_target_dict(cls, target: Dict[str, Any]) -> List[str]:
        """Validates a single target dictionary against all schema rules."""
        errors = []
        tid = target.get("target_id", "UNKNOWN")

        # 1. Check all required fields present and non-empty
        for field in REQUIRED_FIELDS:
            if field not in target:
                errors.append(f"Target {tid} missing required field: '{field}'")
            elif target[field] is None or str(target[field]).strip() == "":
                errors.append(f"Target {tid} field '{field}' is empty")

        # 2. Check target_id format (C01 to C99)
        if not re.match(r"^C\d{2}$", tid):
            errors.append(f"Target ID '{tid}' is improperly formatted (expected C01..C99)")

        # 3. Check URL validity
        url = target.get("page_url", "")
        if not cls.validate_url(url):
            errors.append(f"Target {tid} has invalid URL: '{url}'")

        # 4. Check priority
        prio = target.get("priority", "")
        if prio not in VALID_PRIORITIES:
            errors.append(f"Target {tid} has invalid priority: '{prio}'")

        # 5. Check related question IDs
        qids = target.get("related_question_ids", [])
        if not isinstance(qids, list) or len(qids) == 0:
            errors.append(f"Target {tid} must contain at least one related question ID in a list")

        return errors

    @classmethod
    def validate_dataset(cls, targets: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validates an entire dataset of citation targets."""
        all_errors = []
        target_ids = []
        urls = []

        for t in targets:
            errs = cls.validate_target_dict(t)
            all_errors.extend(errs)
            target_ids.append(t.get("target_id", ""))
            urls.append(t.get("page_url", ""))

        # Check uniqueness of IDs
        id_counts = pd.Series(target_ids).value_counts()
        duplicates_id = id_counts[id_counts > 1].index.tolist()
        if duplicates_id:
            all_errors.append(f"Duplicate Target IDs detected: {duplicates_id}")

        # Check uniqueness of URLs
        url_counts = pd.Series(urls).value_counts()
        duplicates_url = url_counts[url_counts > 1].index.tolist()
        if duplicates_url:
            all_errors.append(f"Duplicate Target URLs detected: {duplicates_url}")

        return {
            "total_targets": len(targets),
            "is_valid": len(all_errors) == 0,
            "errors": all_errors,
            "unique_ids_count": len(set(target_ids)),
            "unique_urls_count": len(set(urls))
        }


if __name__ == "__main__":
    from src.citations.discover_targets import TargetDiscoverer
    targets = TargetDiscoverer.get_all_targets()
    val = TargetValidator.validate_dataset(targets)
    print(f"Dataset Validation: {'PASS' if val['is_valid'] else 'FAIL'}")
    print(f"Total: {val['total_targets']} targets | Unique IDs: {val['unique_ids_count']} | Unique URLs: {val['unique_urls_count']}")
    if val["errors"]:
        print("Errors:", val["errors"])
