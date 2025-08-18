import requests

def check(url):
    insecure = []
    try:
        resp = requests.options(url, timeout=10, headers={"User-Agent": "AdvancedScanner/1.0"})
        methods = resp.headers.get("Allow", "")
        methods_list = [m.strip() for m in methods.split(",") if m.strip()]

        # If OPTIONS didn’t return methods, try common ones manually
        if not methods_list:
            test_methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "TRACE", "CONNECT"]
            for m in test_methods:
                try:
                    r = requests.request(m, url, timeout=5)
                    if r.status_code < 400:
                        methods_list.append(m)
                except:
                    pass

        # Detect insecure methods
        dangerous = {"PUT", "DELETE", "TRACE", "CONNECT"}
        for m in methods_list:
            if m in dangerous:
                insecure.append(m)

        if insecure:
            return f"[!] Insecure Methods Enabled: {', '.join(insecure)}\n[+] All Supported: {', '.join(methods_list)}"
        elif methods_list:
            return f"[+] Safe Methods Only: {', '.join(methods_list)}"
        else:
            return "[OK] No HTTP methods detected"

    except Exception as e:
        return f"[ERROR] {e}"
