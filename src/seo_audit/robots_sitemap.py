"""
Robots, Sitemap & LLMs.txt Auditor Module
Audits robots.txt directives, sitemap.xml structure, and the presence of machine discoverability standards.
"""

from typing import Dict, Any, List
import xml.etree.ElementTree as ET


class RobotsSitemapAuditor:
    @staticmethod
    def audit_robots_txt(content: str) -> Dict[str, Any]:
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        findings = []

        has_sitemap = any(l.lower().startswith("sitemap:") for l in lines)
        has_ai_bot = any("gptbot" in l.lower() or "claudebot" in l.lower() or "perplexitybot" in l.lower() for l in lines)

        if not has_sitemap:
            findings.append({"type": "SitemapDirectiveMissing", "severity": "High", "message": "robots.txt missing Sitemap declaration."})
        if not has_ai_bot:
            findings.append({
                "type": "AICrawlersUnspecified",
                "severity": "High",
                "message": "robots.txt does not specify directives for frontier AI crawlers (GPTBot, ClaudeBot, PerplexityBot)."
            })

        return {
            "total_lines": len(lines),
            "has_sitemap": has_sitemap,
            "has_ai_crawlers": has_ai_bot,
            "findings_count": len(findings),
            "findings": findings
        }

    @staticmethod
    def audit_sitemap_xml(xml_content: str) -> Dict[str, Any]:
        findings = []
        urls_count = 0
        missing_lastmod_count = 0

        try:
            root = ET.fromstring(xml_content)
            # Handle XML namespaces
            namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
            urls = root.findall("sm:url", namespace)
            if not urls:
                # Try without namespace
                urls = root.findall("url")

            urls_count = len(urls)

            for u in urls:
                lastmod = u.find("sm:lastmod", namespace) if "sm" in namespace else u.find("lastmod")
                if lastmod is None or not lastmod.text or not lastmod.text.strip():
                    missing_lastmod_count += 1

            if missing_lastmod_count > 0:
                findings.append({
                    "type": "MissingLastmodTimestamps",
                    "severity": "Medium",
                    "message": f"{missing_lastmod_count} of {urls_count} URLs omit <lastmod> timestamps, preventing search engines from prioritizing fresh content."
                })

        except Exception as e:
            findings.append({"type": "XMLParseError", "severity": "High", "message": f"Failed to parse sitemap XML: {e}"})

        return {
            "urls_count": urls_count,
            "missing_lastmod_count": missing_lastmod_count,
            "findings_count": len(findings),
            "findings": findings
        }

    @staticmethod
    def audit_llms_txt(status_code: int, content: str = "") -> Dict[str, Any]:
        findings = []
        is_missing = status_code == 404

        if is_missing:
            findings.append({
                "type": "LLMsTxtMissing",
                "severity": "High",
                "message": "llms.txt returned HTTP 404. Generative AI engines lack a canonical markdown summary of IncuBrix capabilities."
            })
        elif len(content.strip()) < 100:
            findings.append({
                "type": "LLMsTxtTooShort",
                "severity": "Medium",
                "message": "llms.txt file is too brief to provide meaningful LLM grounding."
            })

        return {
            "status_code": status_code,
            "content_length": len(content),
            "is_missing": is_missing,
            "findings_count": len(findings),
            "findings": findings
        }
