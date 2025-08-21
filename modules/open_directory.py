import requests, re, os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

WORDLIST = "wordlist.txt"

def check(url):
    analysis = []
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "DirScanner/1.0"})
        status = resp.status_code
        size = len(resp.content)

        # Base info
        analysis.append(f"[+] {status} | {size} bytes | {url}")

        content = resp.text.lower()
        soup = BeautifulSoup(resp.text, "html.parser")

        indicators = ["index of", "parent directory", "last modified", 
                      "directory listing", "nginx autoindex", "apache server at"]
        found = [w for w in indicators if w in content]

        if found:
            links = []
            for a in soup.find_all("a", href=True):
                href = a["href"]
                if href in ["../", "/", "#"]:
                    continue
                abs_url = urljoin(url, href)
                links.append(abs_url)

            links = list(dict.fromkeys(links))
            if links:
                preview = ", ".join(links[:10])
                if len(links) > 10:
                    preview += " ..."
                analysis.append(f"[!!] Open Directory Listing at {url}")
                analysis.append(f"     Files/Folders ({len(links)}): {preview}")
            else:
                analysis.append(f"[!!] Suspicious signature found at {url} (No links extracted)")

        return analysis

    except Exception as e:
        return [f"[ERROR] {url} -> {str(e)}"]


def scan_target(base_url, recursive=False, depth=2):
    results = []
    visited = set()

    if not base_url.endswith("/"):
        base_url += "/"

    if not os.path.exists(WORDLIST):
        return [f"[ERROR] Wordlist {WORDLIST} not found!"]

    with open(WORDLIST, "r") as f:
        dirs = [line.strip() for line in f if line.strip() and not line.startswith("#")]

    for d in dirs:
        target = urljoin(base_url, d + "/")
        if target in visited:
            continue
        visited.add(target)

        # Collect results
        result = check_directory(target)
        results.extend(result)

        # Recursive scanning
        if recursive and depth > 1:
            inner = scan_target(target, recursive=True, depth=depth-1)
            results.extend(inner)

    return results


if __name__ == "__main__":
    base = "http://testphp.vulnweb.com/"
    final_results = scan_target(base, recursive=True, depth=2)

    print("\n=== Final Analysis Report ===\n")
    for line in final_results:
        print(line)

