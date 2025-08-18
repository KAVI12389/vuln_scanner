import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
import re

def check(url, max_depth=2, max_links=50):
    visited = set()
    found_links = []

    def crawl(current_url, depth):
        if depth > max_depth or len(found_links) >= max_links:
            return
        try:
            resp = requests.get(current_url, timeout=5, headers={"User-Agent": "AdvancedScanner/1.0"})
            if "text/html" not in resp.headers.get("Content-Type", ""):
                return
            soup = BeautifulSoup(resp.text, "html.parser")
            for a in soup.find_all("a", href=True):
                link = urldefrag(urljoin(current_url, a["href"]))[0]  # absolute path + remove fragment
                if link.startswith("http") and link not in visited:
                    visited.add(link)
                    found_links.append(link)
                    crawl(link, depth + 1)
        except Exception as e:
            pass  # ignore errors but continue

    try:
        crawl(url, 0)
        if found_links:
            result = f"[+] Found {len(found_links)} links (showing up to {max_links}):\n"
            result += "\n".join(found_links[:max_links])
            return result
        else:
            return "[OK] No internal links found"
    except Exception as e:
        return f"[ERROR] {e}"
