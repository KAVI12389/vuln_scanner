import requests

def check(url):
    common_files = [
        "robots.txt", ".env", ".git/config", ".git/HEAD", ".svn/entries",
        "backup.zip", "db.sql", "config.php", "wp-config.php", "adminer.php",
        "phpinfo.php", "composer.json", "composer.lock", "package.json",
        "yarn.lock", ".htaccess", ".DS_Store"
    ]

    found = []
    base = url.rstrip("/")

    try:
        for f in common_files:
            target = f"{base}/{f}"
            try:
                resp = requests.get(target, timeout=5, headers={"User-Agent": "AdvancedScanner/1.0"})
                if resp.status_code == 200:
                    content_type = resp.headers.get("Content-Type", "")
                    # Filter: must not be empty or generic
                    if len(resp.text.strip()) > 0 and "text/html" not in content_type.lower():
                        found.append(target)
            except requests.RequestException:
                continue

        if found:
            return "[!] Sensitive files exposed:\n - " + "\n - ".join(found)
        return "[+] No sensitive files found"

    except Exception as e:
        return f"[ERROR] {e}"

