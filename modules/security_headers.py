import requests

def check(url):
    try:
        resp = requests.get(url, timeout=10)
        headers = resp.headers
        missing = []
        required = ["Content-Security-Policy", "X-Frame-Options", "X-Content-Type-Options","X-Frame-Options","X-XSS-Protection","Referrer-Policy","Strict-Transport-Security"]
        for h in required:
            if h not in headers:
                missing.append(h)
        if missing:
            return f"[!] Missing Headers: {', '.join(missing)}"
        return "[+] All important security headers present"
    except Exception as e:
        return f"[ERROR] {e}"
