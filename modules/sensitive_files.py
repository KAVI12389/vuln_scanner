import requests

def check(url):
    common_files = ["robots.txt", ".env", ".git/config", "backup.zip"]
    found = []
    for f in common_files:
        try:
            resp = requests.get(url.rstrip("/") + "/" + f, timeout=5)
            if resp.status_code == 200 and len(resp.text) > 0:
                found.append(f)
        except:
            continue
    if found:
        return f"[!] Sensitive files exposed: {', '.join(found)}"
    return "[+] No sensitive files found"
