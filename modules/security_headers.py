import requests

def check(url):
    try:
        resp = requests.get(url, timeout=10, headers={"User-Agent": "AdvancedScanner/1.0"})
        headers = resp.headers

        # Recommended Security Headers (OWASP)
        required = {
            "Content-Security-Policy": "Prevents XSS and data injection attacks",
            "X-Frame-Options": "Protects against Clickjacking",
            "X-Content-Type-Options": "Prevents MIME-sniffing",
            "X-XSS-Protection": "Basic XSS filter (legacy browsers)",
            "Referrer-Policy": "Controls how much referrer info leaks",
            "Strict-Transport-Security": "Forces HTTPS connections",
            "Permissions-Policy": "Restricts powerful browser APIs (camera, mic, etc.)"
        }

        missing = []
        present = []

        for h, reason in required.items():
            if h not in headers:
                missing.append(f"{h} ({reason})")
            else:
                present.append(h)

        if missing:
            result = f"[!] Missing Security Headers:\n - " + "\n - ".join(missing)
            if present:
                result += f"\n[+] Present Headers: {', '.join(present)}"
            return result
        else:
            return "[+] All important security headers are present"

    except Exception as e:
        return f"[ERROR] {e}"
