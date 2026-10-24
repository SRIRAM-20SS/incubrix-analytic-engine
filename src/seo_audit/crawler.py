"""
Site Crawler Module
Inspects publicly accessible URLs across incubrix.com with configurable timeouts,
rate limits, and error handling. Extracts metadata, heading hierarchies, images, links, and schemas.
"""

import time
from typing import Dict, Any, List, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


class SiteCrawler:
    def __init__(
        self,
        base_url: str = "https://incubrix.com",
        timeout: int = 10,
        max_pages: int = 15,
        user_agent: str = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) IncuBrix-Audit-Bot/1.0"
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.max_pages = max_pages
        self.headers = {"User-Agent": user_agent}

    def inspect_url(self, url: str) -> Dict[str, Any]:
        """
        Inspects a single URL and extracts SEO, semantic, and accessibility signals.
        """
        result = {
            "url": url,
            "status_code": None,
            "redirect_chain": [],
            "content_type": None,
            "title": None,
            "meta_description": None,
            "canonical_url": None,
            "h1_tags": [],
            "empty_h1_count": 0,
            "h2_tags": [],
            "total_images": 0,
            "images_missing_alt": 0,
            "internal_links_count": 0,
            "json_ld_count": 0,
            "error": None,
            "inspected": False
        }

        try:
            r = requests.get(url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
            result["status_code"] = r.status_code
            result["content_type"] = r.headers.get("Content-Type", "")
            if r.history:
                result["redirect_chain"] = [h.url for h in r.history]

            if r.status_code == 200 and "text/html" in result["content_type"]:
                soup = BeautifulSoup(r.text, "html.parser")
                result["inspected"] = True

                # Title
                if soup.title and soup.title.string:
                    result["title"] = soup.title.string.strip()

                # Meta Description
                meta_desc = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "description"})
                if meta_desc and meta_desc.get("content"):
                    result["meta_description"] = meta_desc["content"].strip()

                # Canonical
                canon = soup.find("link", attrs={"rel": "canonical"})
                if canon and canon.get("href"):
                    result["canonical_url"] = canon["href"].strip()

                # Headings
                h1s = soup.find_all("h1")
                for h1 in h1s:
                    text = h1.get_text().strip()
                    result["h1_tags"].append(text)
                    if not text:
                        result["empty_h1_count"] += 1

                result["h2_tags"] = [h2.get_text().strip() for h2 in soup.find_all("h2") if h2.get_text().strip()]

                # Images & Alt
                imgs = soup.find_all("img")
                result["total_images"] = len(imgs)
                missing_alt = 0
                for img in imgs:
                    alt = img.get("alt")
                    if alt is None or alt.strip() == "":
                        missing_alt += 1
                result["images_missing_alt"] = missing_alt

                # Internal Links
                base_domain = urlparse(self.base_url).netloc
                links = soup.find_all("a", href=True)
                internal_count = 0
                for link in links:
                    href = link["href"]
                    parsed = urlparse(urljoin(url, href))
                    if parsed.netloc == base_domain:
                        internal_count += 1
                result["internal_links_count"] = internal_count

                # JSON-LD
                json_lds = soup.find_all("script", type="application/ld+json")
                result["json_ld_count"] = len(json_lds)

        except Exception as e:
            result["error"] = str(e)

        return result

    def crawl_core_pages(self) -> List[Dict[str, Any]]:
        """
        Crawls key public marketing and app pages for auditing.
        """
        core_urls = [
            f"{self.base_url}/",
            f"{self.base_url}/pricing",
            f"{self.base_url}/faq",
            f"{self.base_url}/manifesto",
            f"{self.base_url}/about",
            f"{self.base_url}/how-it-works",
            "https://app.incubrix.com/"
        ]

        results = []
        for u in core_urls[:self.max_pages]:
            data = self.inspect_url(u)
            results.append(data)
            time.sleep(0.1)  # Respect rate limits

        return results


if __name__ == "__main__":
    crawler = SiteCrawler()
    pages = crawler.crawl_core_pages()
    for p in pages:
        print(f"{p['url']} -> Status: {p['status_code']}, JSON-LD: {p['json_ld_count']}, Empty H1: {p['empty_h1_count']}")
