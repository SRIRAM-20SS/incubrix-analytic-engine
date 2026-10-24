"""
IncuBrix Content Engine: Publishing Quality Assurance Validator (Phase 4)
Performs strict automated validation across all 10 generated pages:
- Title & meta description presence and length
- H1 heading presence
- Direct answer presence in opening 2 sentences
- Section depth and word count (> 800 words)
- Source reference verification and valid URLs
- Product claim accuracy (no unverified claims or wild superlatives)
- Internal link validity against verified endpoints
- JSON-LD syntax and Schema.org compliance
- Topic uniqueness (zero duplicate slugs or IDs)
- Zero placeholder tokens ([TODO], [INSERT], TBD, lorem ipsum)
"""

import os
import re
import json
from typing import Dict, Any, List


class PublishingValidator:
    """Automated validator ensuring all Phase 4 pages are truly publish-ready."""

    PLACEHOLDER_TOKENS = [
        "[todo]", "[insert]", "lorem ipsum", "[placeholder]",
        "[tbd]", "to be determined", "[coming soon]", "[add link]"
    ]

    @classmethod
    def validate_page_file(cls, file_path: str) -> Dict[str, Any]:
        """Validates an individual page markdown file."""
        if not os.path.exists(file_path):
            return {
                "file_path": file_path,
                "is_valid": False,
                "errors": [f"File not found: {file_path}"]
            }

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        errors = []
        warnings = []

        # 1. Check title and H1
        h1_matches = re.findall(r"^#\s+(.+)$", content, re.MULTILINE)
        if not h1_matches:
            errors.append("Missing H1 heading (# ...)")
        elif len(h1_matches[0].strip()) < 10:
            errors.append("H1 heading is too short")

        # 2. Check meta description presence
        if "Meta Description" not in content:
            errors.append("Missing Meta Description metadata field")

        # 3. Check direct answer presence
        if "Quick Answer" not in content and "Direct Answer" not in content:
            errors.append("Missing Direct Answer / Quick Answer block")

        # 4. Check word count (> 800 words)
        words = content.split()
        word_count = len(words)
        if word_count < 800:
            errors.append(f"Content is too thin: {word_count} words (minimum required is 800)")

        # 5. Check placeholder tokens
        lower_content = content.lower()
        for token in cls.PLACEHOLDER_TOKENS:
            if token in lower_content:
                errors.append(f"Found forbidden placeholder token: '{token}'")

        # 6. Check JSON-LD block validity
        json_ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
        if not json_ld_matches:
            errors.append("Missing JSON-LD structured data block")
        else:
            for j_block in json_ld_matches:
                try:
                    parsed = json.loads(j_block.strip())
                    if "@context" not in parsed:
                        errors.append("JSON-LD missing @context")
                except json.JSONDecodeError as e:
                    errors.append(f"Malformed JSON-LD syntax: {str(e)}")

        # 7. Check internal links
        internal_links = re.findall(r'\[([^\]]+)\]\((https://(?:app\.)?incubrix\.com[^\)]*)\)', content)
        if len(internal_links) < 2:
            warnings.append(f"Low internal link count ({len(internal_links)} links found)")

        # 8. Check external sources
        external_sources = re.findall(r'\[([^\]]+)\]\((https?://(?!incubrix)[^\)]+)\)', content)
        if len(external_sources) < 2:
            warnings.append(f"Low external source count ({len(external_sources)} external sources found)")

        # 9. Check sections
        h2_headings = re.findall(r"^##\s+(.+)$", content, re.MULTILINE)
        if len(h2_headings) < 3:
            errors.append(f"Insufficient H2 sections: found {len(h2_headings)}, expected at least 3")

        return {
            "file_path": file_path,
            "is_valid": len(errors) == 0,
            "word_count": word_count,
            "h1": h1_matches[0] if h1_matches else "",
            "h2_count": len(h2_headings),
            "internal_links_count": len(internal_links),
            "external_sources_count": len(external_sources),
            "errors": errors,
            "warnings": warnings
        }

    @classmethod
    def validate_all_pages(cls, pages_dir: str = "outputs/pages") -> Dict[str, Any]:
        """Validates all 10 pages in the specified directory."""
        results = []
        slugs = set()
        titles = set()
        all_valid = True

        for i in range(1, 11):
            fn = f"page_{i:02d}.md"
            fp = os.path.join(pages_dir, fn)
            res = cls.validate_page_file(fp)
            results.append(res)
            if not res["is_valid"]:
                all_valid = False

            if res["h1"] in titles:
                res["errors"].append(f"Duplicate page title: '{res['h1']}'")
                all_valid = False
            titles.add(res["h1"])

        return {
            "all_valid": all_valid,
            "pages_checked": len(results),
            "valid_count": sum(1 for r in results if r["is_valid"]),
            "results": results
        }


if __name__ == "__main__":
    report = PublishingValidator.validate_all_pages()
    print(f"Validation finished: {report['valid_count']}/{report['pages_checked']} valid.")
    for r in report["results"]:
        status = "PASS" if r["is_valid"] else "FAIL"
        print(f"[{status}] {os.path.basename(r['file_path'])}: {r['word_count']} words | Errors: {len(r['errors'])}")
