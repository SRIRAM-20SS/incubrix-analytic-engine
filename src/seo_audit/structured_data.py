"""
Structured Data & Schema.org Auditor Module
Scans DOM for JSON-LD structured data, validates JSON syntax, and audits schema completeness.
"""

import json
from typing import Dict, Any, List
from bs4 import BeautifulSoup


class SchemaAuditor:
    RECOMMENDED_SCHEMAS = {
        "/": ["Organization", "WebSite"],
        "/faq": ["FAQPage"],
        "/pricing": ["Product", "AggregateOffer", "Offer"],
        "/how-it-works": ["BreadcrumbList", "HowTo"],
        "app.incubrix.com": ["SoftwareApplication"]
    }

    @staticmethod
    def audit_page_schemas(html_text: str, page_url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html_text, "html.parser")
        script_tags = soup.find_all("script", type="application/ld+json")
        findings = []
        parsed_schemas = []

        if len(script_tags) == 0:
            findings.append({
                "type": "NoStructuredData",
                "severity": "High",
                "message": f"Zero JSON-LD structured data tags found on {page_url}. Page is ineligible for rich snippets or answer boxes."
            })

        for idx, tag in enumerate(script_tags):
            raw_text = tag.string or ""
            try:
                data = json.loads(raw_text.strip())
                parsed_schemas.append(data)
                # Check context
                ctx = data.get("@context", "")
                if "schema.org" not in str(ctx).lower():
                    findings.append({
                        "type": "InvalidSchemaContext",
                        "severity": "Medium",
                        "message": f"JSON-LD block {idx+1} has invalid @context: '{ctx}'."
                    })
            except json.JSONDecodeError as e:
                findings.append({
                    "type": "MalformedJSONLD",
                    "severity": "High",
                    "message": f"Malformed JSON in block {idx+1}: {e}."
                })

        # Check recommended schemas for known paths
        for path_key, expected_types in SchemaAuditor.RECOMMENDED_SCHEMAS.items():
            if path_key in page_url:
                found_types = []
                for s in parsed_schemas:
                    if isinstance(s, dict):
                        if "@graph" in s:
                            for node in s["@graph"]:
                                found_types.append(node.get("@type"))
                        else:
                            found_types.append(s.get("@type"))

                for exp in expected_types:
                    if exp not in found_types:
                        findings.append({
                            "type": "MissingExpectedSchema",
                            "severity": "High",
                            "message": f"Expected schema @type '{exp}' missing on {page_url}."
                        })

        return {
            "page_url": page_url,
            "json_ld_blocks_count": len(script_tags),
            "parsed_schemas_count": len(parsed_schemas),
            "findings_count": len(findings),
            "findings": findings
        }
