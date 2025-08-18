import requests

def check(url):
    test_payloads = {
        "XSS": "<script>alert(1)</script>",
        "SQLi": "' OR '1'='1"
    }
    results = []
    for vuln, payload in test_payloads.items():
        try:
            resp = requests.get(url, params={"q": payload}, timeout=5)
            if payload in resp.text:
                results.append(f"[!] {vuln} possible with payload {payload}")
        except:
            continue
    if results:
        return "\n".join(results)
    return "[+] No basic XSS/SQL injection detected"
