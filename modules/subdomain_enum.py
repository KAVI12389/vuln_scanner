import requests

def check(url):
    base = url.replace("http://", "").replace("https://", "").split("/")[0]
    found = []
    try:
        with open("wordlists/subdomains.txt") as f:
            for sub in f:
                sub = sub.strip()
                target = f"http://{sub}.{base}"
                try:
                    resp = requests.get(target, timeout=3)
                    if resp.status_code < 400:
                        found.append(target)
                except:
                    continue
    except FileNotFoundError:
        return "[ERROR] wordlists/subdomains.txt missing"
    if found:
        return "[!] Subdomains found:\n" + "\n".join(found)
    return "[+] No subdomains discovered"
