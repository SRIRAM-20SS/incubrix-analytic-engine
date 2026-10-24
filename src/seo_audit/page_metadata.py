"""
Page Metadata Auditor Module
Analyzes page titles, meta descriptions, Open Graph protocol, Twitter Cards,
robots directives, and mobile browser metadata.
"""

from typing import Dict, Any, List
from bs4 import BeautifulSoup


class MetadataAuditor:
    @staticmethod
    def audit_html(html_text: str, page_url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html_text, "html.parser")
        findings = []

        # 1. Title Audit
        title_tag = soup.find("title")
        title_str = title_tag.get_text().strip() if title_tag else ""
        if not title_str:
            findings.append({"type": "TitleMissing", "severity": "High", "message": "Missing <title> tag."})
        elif len(title_str) < 30:
            findings.append({"type": "TitleTooShort", "severity": "Medium", "message": f"Title is short ({len(title_str)} chars): '{title_str}'."})
        elif len(title_str) > 65:
            findings.append({"type": "TitleTooLong", "severity": "Low", "message": f"Title may truncate in SERP ({len(title_str)} chars)."})

        # 2. Meta Description Audit
        meta_desc = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "description"})
        desc_str = meta_desc.get("content", "").strip() if meta_desc else ""
        if not desc_str:
            findings.append({"type": "MetaDescriptionMissing", "severity": "High", "message": "Missing meta description."})
        elif len(desc_str) < 100:
            findings.append({"type": "MetaDescriptionShort", "severity": "Medium", "message": f"Meta description is short ({len(desc_str)} chars)."})
        elif len(desc_str) > 165:
            findings.append({"type": "MetaDescriptionLong", "severity": "Low", "message": f"Meta description may truncate ({len(desc_str)} chars)."})

        # 3. Twitter Card & Open Graph Audit
        tw_card = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "twitter:card"})
        tw_img = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "twitter:image"})
        og_img = soup.find("meta", attrs={"property": lambda x: x and x.lower() == "og:image"})
        og_title = soup.find("meta", attrs={"property": lambda x: x and x.lower() == "og:title"})

        if not tw_card:
            findings.append({"type": "TwitterCardMissing", "severity": "Medium", "message": "Missing twitter:card meta tag."})
        if not tw_img and not og_img:
            findings.append({"type": "SocialImageMissing", "severity": "Medium", "message": "Missing social sharing preview image (og:image / twitter:image)."})
        if not og_title:
            findings.append({"type": "OGTitleMissing", "severity": "Low", "message": "Missing og:title tag."})

        # 4. Robots Meta Tag Audit
        robots_meta = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "robots"})
        if not robots_meta:
            findings.append({
                "type": "RobotsMetaMissing",
                "severity": "Medium",
                "message": "Missing robots meta tag with snippet length controls (max-snippet:-1, max-image-preview:large)."
            })

        # 5. Mobile & App Icon Audit
        apple_icon = soup.find("link", attrs={"rel": lambda x: x and "apple-touch-icon" in x.lower()})
        manifest = soup.find("link", attrs={"rel": lambda x: x and "manifest" in x.lower()})
        if not apple_icon:
            findings.append({"type": "AppleTouchIconMissing", "severity": "Low", "message": "Missing apple-touch-icon link for iOS home screen bookmarks."})
        if not manifest:
            findings.append({"type": "ManifestMissing", "severity": "Low", "message": "Missing web app manifest.json."})

        return {
            "page_url": page_url,
            "title": title_str,
            "title_length": len(title_str),
            "meta_description": desc_str,
            "meta_description_length": len(desc_str),
            "findings_count": len(findings),
            "findings": findings
        }
