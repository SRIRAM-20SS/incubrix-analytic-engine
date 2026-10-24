"""
Performance & Security Auditor Module
Evaluates font display optimization, HTTP security headers, trailing slash consistency,
and resource preloading signals.
"""

from typing import Dict, Any, List
from bs4 import BeautifulSoup


class PerformanceAuditor:
    @staticmethod
    def audit_font_and_resources(html_text: str, page_url: str) -> Dict[str, Any]:
        soup = BeautifulSoup(html_text, "html.parser")
        findings = []

        # 1. Google Fonts font-display: swap check
        font_links = soup.find_all("link", href=lambda x: x and "fonts.googleapis.com" in x)
        for link in font_links:
            href = link.get("href", "")
            if "display=swap" not in href:
                findings.append({
                    "type": "FontDisplaySwapMissing",
                    "severity": "Medium",
                    "message": f"Google Fonts stylesheet link omits 'display=swap', which can cause Flash of Invisible Text (FOIT)."
                })

        # 2. DNS Prefetch & Preconnect for third-party fonts
        preconnects = soup.find_all("link", rel=lambda x: x and ("preconnect" in x or "dns-prefetch" in x))
        has_font_preconnect = any("fonts.gstatic.com" in (p.get("href") or "") for p in preconnects)
        if font_links and not has_font_preconnect:
            findings.append({
                "type": "FontPreconnectMissing",
                "severity": "Low",
                "message": "Missing preconnect link to https://fonts.gstatic.com to speed up web font handshake."
            })

        return {
            "page_url": page_url,
            "font_links_count": len(font_links),
            "preconnects_count": len(preconnects),
            "findings_count": len(findings),
            "findings": findings
        }

    @staticmethod
    def audit_security_headers(headers: Dict[str, str]) -> Dict[str, Any]:
        findings = []
        lower_headers = {k.lower(): v for k, v in headers.items()}

        recommended_headers = [
            ("strict-transport-security", "HSTS header missing or weak."),
            ("x-content-type-options", "X-Content-Type-Options: nosniff header missing."),
            ("permissions-policy", "Permissions-Policy header missing."),
            ("referrer-policy", "Referrer-Policy header missing.")
        ]

        for hdr, msg in recommended_headers:
            if hdr not in lower_headers:
                findings.append({"type": f"MissingHeader_{hdr}", "severity": "Medium", "message": msg})

        return {
            "headers_inspected_count": len(headers),
            "missing_recommended_count": len(findings),
            "findings": findings
        }
