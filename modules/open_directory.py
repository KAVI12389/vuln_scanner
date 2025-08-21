# modules/open_directory.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

def check(url, max_depth=2):
    """
    Advanced Open Directory Listing Detector
    - Works on big websites (timeout 20s)
    - Recursive scan up to max_depth
    - Returns full line-by-line report
    """
    scanned = set()
    report = []

    # Browser headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/114.0.0.0 Safari/537.36'
    }

    # Auto HTTPS if not specified
    if not url.startswith("http"):
        url = "https://" + url

    def scan_directory(current_url, depth):
        if depth > max_depth or current_url in scanned:
            return
        scanned.add(current_url)

        try:
            if not current_url.endswith("/"):
                current_url += "/"

            resp = requests.get(current_url, headers=headers, timeout=20, allow_redirects=True)
            resp.raise_for_status()
            content = resp.text.lower()

            indicators = ["index of", "parent directory", "last modified", "directory listing"]
            if any(word in content for word in indicators):
                report.append(f"[!!] Open Directory Listing at {current_url}")
                soup = BeautifulSoup(resp.text, "html.parser")
                links = [urljoin(current_url, a["href"]) for a in soup.find_all("a", href=True)]
                files, folders = [], []

                for link in links:
                    parsed = urlparse(link)
                    if link.endswith("/"):
                        folders.append(link)
                    else:
                        files.append(link)

                if files:
                    report.append(f"Files ({len(files)}):")
                    for f in files:
                        report.append(f"  • {f}")

                if folders:
                    report.append(f"Subfolders ({len(folders)}):")
                    for f in folders:
                        report.append(f"  • {f}")

                # Recursive scan
                for f in folders:
                    scan_directory(f, depth + 1)
            else:
                report.append(f"[?] {current_url} → 200 OK but no directory listing")

        except requests.exceptions.RequestException as e:
            report.append(f"[ERROR] Request failed for {current_url}: {e}")
        except Exception as e:
            report.append(f"[ERROR] Unexpected error at {current_url}: {e}")

    scan_directory(url, 0)
    return "\n".join(report) if report else f"No open directories found at {url}"
