import requests

def check(url):
    try:
        resp = requests.options(url, timeout=10)
        methods = resp.headers.get("Allow", "")
        if any(m in methods for m in ["PUT", "DELETE"]):
            return f"[!] Insecure Methods Enabled: {methods}"
        return f"[+] Safe Methods Only: {methods}"
    except Exception as e:
        return f"[ERROR] {e}"
