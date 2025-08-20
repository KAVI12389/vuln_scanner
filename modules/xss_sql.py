import requests
import re
import os
import html

REPORT_FILE = "reports/output.txt"

def write_report(title, result):
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, "a", encoding="utf-8") as f:
        f.write(f"\n=== {title} ===\n")
        f.write(result + "\n")

def check(url):
    results = []

    xss_payloads = [
        "<script>alert(1)</script>",
        "'\"><img src=x onerror=alert(1)>",
        "<svg/onload=alert(1)>",
        "<body onload=alert(1)>"
    ]

    sqli_payloads = [
        "' OR '1'='1",
        "\" OR \"1\"=\"1",
        "' OR 1=1--",
        "' UNION SELECT null--",
        "'; DROP TABLE users--"
    ]

    sql_errors = [
        "SQL syntax.*MySQL",
        "Warning.*mysql_",
        "PostgreSQL.*ERROR",
        "Microsoft SQL Server.*Driver",
        "System.Data.SqlClient.SqlException",
        "Oracle.*ORA-"
    ]

    headers = {"User-Agent": "AdvancedScanner/1.0"}

    # --- XSS Test ---
    for payload in xss_payloads:
        try:
            r = requests.get(url, params={"q": payload}, timeout=6, headers=headers)
            page = r.text.lower()
            # raw payload or html-encoded payload check
            if payload.lower() in page or html.escape(payload).lower() in page:
                results.append(f"[!!] Reflected XSS detected with payload: {payload}")
        except requests.RequestException:
            continue

    # --- SQLi Test ---
    for payload in sqli_payloads:
        try:
            r = requests.get(url, params={"id": payload}, timeout=6, headers=headers)
            for err in sql_errors:
                if re.search(err, r.text, re.IGNORECASE):
                    results.append(f"[!!] SQL Injection error-based detected with payload: {payload}")
                    break
        except requests.RequestException:
            continue

    if results:
        final = "\n".join(results)
    else:
        final = "[+] No XSS/SQL Injection detected"

    # write into report
    write_report("XSS & SQLi Testing", final)

    return final


