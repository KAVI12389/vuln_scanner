import requests
import random

def check(url):
    common_files = [
        "robots.txt", ".env", ".git/config", ".git/HEAD", ".svn/entries",
        "backup.zip", "db.sql", "config.php", "wp-config.php", "adminer.php",
        "phpinfo.php", "composer.json", "composer.lock", "package.json",
        "yarn.lock", ".htaccess", ".DS_Store", "id_rsa", "id_rsa.pub",
        "credentials.json", "web.config", "local.settings.json",
        "db_backup.sql", "dump.sql", "error.log"
    ]

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (X11; Linux x86_64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "AdvancedScanner/1.0"
    ]

    found = []
    base = url.rstrip("/")

    try:
        for f in common_files:
            target = f"{base}/{f}"
            headers = {"User-Agent": random.choice(user_agents)}
            try:
                resp = requests.get(target, timeout=6, headers=headers, allow_redirects=True)
                status = resp.status_code
                content_type = resp.headers.get("Content-Type", "")
                size = len(resp.content)

                # Consider 200, 401, 403 as "interesting"
                if status in [200, 401, 403]:
                    # Ignore pure HTML pages
                    if "text/html" not in content_type.lower() or size > 100:
                        found.append(f"{target}  ({status}, {content_type}, {size} bytes)")

            except requests.RequestException:
                continue

        if found:
            return "[!] Sensitive files exposed:\n - " + "\n - ".join(found)
        return "[+] No sensitive files found"

    except Exception as e:
        return f"[ERROR] {e}"


