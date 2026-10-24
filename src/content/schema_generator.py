"""
IncuBrix Content Engine: Schema Generator (Phase 4)
Produces valid, search-engine-compliant JSON-LD structured data.
Supports Article, HowTo, FAQPage, SoftwareApplication, and BreadcrumbList schemas.
"""

from typing import Dict, Any, List
import json


class SchemaGenerator:
    """Generates and validates JSON-LD schemas for Phase 4 publish-ready pages."""

    @staticmethod
    def generate_breadcrumb_schema(page_url: str, page_title: str, category_name: str) -> Dict[str, Any]:
        """Generates BreadcrumbList JSON-LD."""
        return {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": 1,
                    "name": "Home",
                    "item": "https://incubrix.com"
                },
                {
                    "@type": "ListItem",
                    "position": 2,
                    "name": category_name,
                    "item": f"https://incubrix.com/{category_name.lower().replace(' ', '-')}"
                },
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": page_title,
                    "item": page_url
                }
            ]
        }

    @staticmethod
    def generate_article_schema(
        page_url: str,
        headline: str,
        description: str,
        date_published: str = "2026-10-24",
        date_modified: str = "2026-10-24"
    ) -> Dict[str, Any]:
        """Generates standard Article / BlogPosting schema."""
        return {
            "@type": "Article",
            "@id": f"{page_url}#article",
            "isPartOf": {
                "@type": "WebPage",
                "@id": page_url
            },
            "headline": headline,
            "description": description,
            "url": page_url,
            "datePublished": date_published,
            "dateModified": date_modified,
            "author": {
                "@type": "Organization",
                "name": "IncuBrix Editorial Team",
                "url": "https://incubrix.com"
            },
            "publisher": {
                "@type": "Organization",
                "name": "IncuBrix Private Limited",
                "url": "https://incubrix.com",
                "logo": {
                    "@type": "ImageObject",
                    "url": "https://incubrix.com/assets/incubrix-logo.jpg"
                }
            },
            "mainEntityOfPage": {
                "@type": "WebPage",
                "@id": page_url
            }
        }

    @staticmethod
    def generate_howto_schema(
        name: str,
        description: str,
        steps: List[Dict[str, str]],
        total_time: str = "PT10M"
    ) -> Dict[str, Any]:
        """Generates HowTo schema with structured steps."""
        schema_steps = []
        for idx, s in enumerate(steps, 1):
            schema_steps.append({
                "@type": "HowToStep",
                "position": idx,
                "name": s["title"],
                "text": s["instruction"],
                "url": s.get("step_url", "")
            })

        return {
            "@type": "HowTo",
            "name": name,
            "description": description,
            "totalTime": total_time,
            "step": schema_steps
        }

    @staticmethod
    def generate_faq_schema(faq_items: List[Dict[str, str]]) -> Dict[str, Any]:
        """Generates FAQPage schema."""
        main_entity = []
        for item in faq_items:
            main_entity.append({
                "@type": "Question",
                "name": item["question"],
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": item["answer"]
                }
            })
        return {
            "@type": "FAQPage",
            "mainEntity": main_entity
        }

    @staticmethod
    def generate_software_schema(
        name: str = "IncuBrix CreatorOps Studio",
        url: str = "https://app.incubrix.com",
        description: str = "AI-powered video repurposing and CreatorOps operating system."
    ) -> Dict[str, Any]:
        """Generates SoftwareApplication schema."""
        return {
            "@type": "SoftwareApplication",
            "name": name,
            "operatingSystem": "Web, Chrome, Edge, Safari",
            "applicationCategory": "MultimediaApplication",
            "offers": {
                "@type": "Offer",
                "price": "0.00",
                "priceCurrency": "USD",
                "description": "Free plan includes 300 credits with no credit card required"
            },
            "url": url,
            "description": description
        }

    @classmethod
    def assemble_page_schema(
        cls,
        page_url: str,
        headline: str,
        description: str,
        category: str,
        content_type: str,
        custom_elements: Dict[str, Any]
    ) -> str:
        """Assembles unified @graph JSON-LD script block."""
        graph = [
            cls.generate_article_schema(page_url, headline, description),
            cls.generate_breadcrumb_schema(page_url, headline, category)
        ]

        if "How-to" in content_type or "Workflow" in content_type:
            if "steps" in custom_elements:
                graph.append(cls.generate_howto_schema(headline, description, custom_elements["steps"]))
        elif "FAQ" in content_type:
            if "faq_items" in custom_elements:
                graph.append(cls.generate_faq_schema(custom_elements["faq_items"]))
        elif "Comparison" in content_type:
            graph.append(cls.generate_software_schema())

        schema_payload = {
            "@context": "https://schema.org",
            "@graph": graph
        }

        json_text = json.dumps(schema_payload, indent=2)
        return f'<script type="application/ld+json">\n{json_text}\n</script>'


if __name__ == "__main__":
    sample_schema = SchemaGenerator.assemble_page_schema(
        page_url="https://incubrix.com/guides/sample",
        headline="Sample Headline",
        description="Sample Description",
        category="Content repurposing",
        content_type="How-to Guide",
        custom_elements={"steps": [{"title": "Step 1", "instruction": "Do something"}]}
    )
    print("Sample Schema generated successfully, length:", len(sample_schema))
