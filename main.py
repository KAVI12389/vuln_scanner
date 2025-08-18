import os
import sys
from modules import open_directory, security_headers, http_methods, sensitive_files
from modules import xss_sql, ssl_check, subdomain_enum, crawler

REPORT_FILE = "reports/output.txt"
# main.py


# 🔹 Banner Function
def banner():
    print(r"""
  ██╗  ██╗ █████╗ ██╗   ██╗██╗
  ██║ ██╔╝██╔══██╗██║   ██║██║
  █████╔╝ ███████║██║   ██║██║
  ██╔═██╗ ██╔══██║╚██╗ ██╔╝██║
  ██║  ██╗██║  ██║ ╚████╔╝ ██║
  ╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝
  
        🚀 Advanced Web Vulnerability Scanner 🚀
        ----------------------------------------
                 Developed by: KAVI
    """)

def write_report(title, result):
    with open(REPORT_FILE, "a") as f:
        f.write(f"\n=== {title} ===\n{result}\n")


def menu():
    print("""
    [1] Check Open Directory Listings
    [2] Identify Missing Security Headers
    [3] Detect Insecure HTTP Methods
    [4] Check Exposed Robots.txt & Sensitive Files
    [5] Basic XSS & SQL Injection Testing
    [6] TLS/SSL Certificate Validation
    [7] Subdomain Enumeration
    [8] Crawl Internal Links
    [9] Run All Tests
    [0] Exit
    """)


if __name__ == "__main__":
    banner()   # 🔹 Banner show here

    if not os.path.exists("reports"):
        os.makedirs("reports")
    open(REPORT_FILE, "w").close()  # clear old report

    url = input("Enter target URL: ").strip()
    while True:
        menu()
        choice = input("Select option: ").strip()

        if choice == "1":
            result = open_directory.check(url)
            print(result); write_report("Open Directory Listings", result)

        elif choice == "2":
            result = security_headers.check(url)
            print(result); write_report("Security Headers", result)

        elif choice == "3":
            result = http_methods.check(url)
            print(result); write_report("HTTP Methods", result)

        elif choice == "4":
            result = sensitive_files.check(url)
            print(result); write_report("Sensitive Files", result)

        elif choice == "5":
            result = xss_sql.check(url)
            print(result); write_report("XSS & SQL Injection", result)

        elif choice == "6":
            result = ssl_check.check(url)
            print(result); write_report("SSL/TLS Check", result)

        elif choice == "7":
            result = subdomain_enum.check(url)
            print(result); write_report("Subdomain Enumeration", result)

        elif choice == "8":
            result = crawler.check(url)
            print(result); write_report("Crawler", result)

        elif choice == "9":
            for mod, title in [
                (open_directory, "Open Directory Listings"),
                (security_headers, "Security Headers"),
                (http_methods, "HTTP Methods"),
                (sensitive_files, "Sensitive Files"),
                (xss_sql, "XSS & SQL Injection"),
                (ssl_check, "SSL/TLS Check"),
                (subdomain_enum, "Subdomain Enumeration"),
                (crawler, "Crawler")
            ]:
                result = mod.check(url)
                print(f"\n{title}:\n{result}")
                write_report(title, result)

        elif choice == "0":
            print("Exiting... Report saved in reports/output.txt")
            sys.exit()
        else:
            print("Invalid option, try again!")
