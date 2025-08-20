import requests
import random

def check(url):
    sensitive_files = [
        "robots.txt", ".env", ".git/config", ".git/HEAD", ".svn/entries",
        "backup.zip", "backup.tar.gz", "db.sql", "database.sql", "dump.sql",
        "config.php", "wp-config.php", "adminer.php", "phpinfo.php",
        "composer.json", "composer.lock", "package.json", "yarn.lock",
        ".htaccess", ".DS_Store", "id_rsa", "id_rsa.pub",
        "credentials.json", "web.config", "local.settings.json",
        "db_backup.sql", "error.log", "access.log", "debug.log",
        "old.zip", "backup.old", "site.bak", "index.bak", "test.php"
    ]

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
        "Mozilla/5.0 (X11; Linux x86_64)",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
        "AdvancedScanner/1.1"
    ]

    base = url.rstrip("/")
    results = []

    for f in sensitive_files:
        target = f"{base}/{f}"
        headers = {"User-Agent": random.choice(user_agents)}
        try:
            resp = requests.get(target, timeout=8, headers=headers, allow_redirects=True)
            status = resp.status_code
            size = len(resp.content)
            ctype = resp.headers.get("Content-Type", "")

            # 200 = found, 401/403 = restricted but exists
            if status in [200, 401, 403]:
                results.append(f"[!!] Found: {target} ({status}, {ctype}, {size} bytes)")
        except requests.RequestException:
            continue

    if results:
        return "=== Sensitive Files ===\n" + "\n".join(results)
    else:
        return "=== Sensitive Files ===\n[+] No sensitive files found"


# Example run
if __name__ == "__main__":
    url = "http://testphp.vulnweb.com/"
    print(check_sensitive_files(url))
