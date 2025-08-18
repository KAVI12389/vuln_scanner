import requests

def check(url):
    base = url.replace("http://", "").replace("https://", "").split("/")[0]
    found = set()  # avoid duplicates

    try:
        with open("wordlists/subdomains.txt") as f:
            subs = [s.strip() for s in f if s.strip()]
    except FileNotFoundError:
        return "[ERROR] wordlists/subdomains.txt missing"

    for sub in subs:
        target_domain = f"{sub}.{base}"
        for scheme in ["http://", "https://"]:
            target = f"{scheme}{target_domain}"
            try:
                resp = requests.get(target, timeout=3, headers={"User-Agent": "AdvancedScanner/1.0"})
                if resp.status_code < 400:
                    found.add(target)
            except requests.RequestException:
                continue

    if found:
        return "[!] Subdomains found:\n - " + "\n - ".join(sorted(found))
    return "[+] No subdomains discovered"

