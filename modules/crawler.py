import requests, re

def check(url):
    try:
        resp = requests.get(url, timeout=5)
        links = re.findall(r'href=[\'"]?([^\'" >]+)', resp.text)
        links = list(set(links))
        return f"[+] Found {len(links)} links:\n" + "\n".join(links[:20])
    except Exception as e:
        return f"[ERROR] {e}"
