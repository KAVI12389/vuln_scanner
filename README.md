# vuln_scanner
advanced vulnerability scanner project

A simple Python-based Web Application Vulnerability Scanner to detect common misconfigurations and security issues in websites.

✨ Features

✅ Check for Open Directory Listings

✅ Identify Missing Security Headers (e.g., CSP, X-Frame-Options)

✅ Detect Insecure HTTP Methods (PUT, DELETE)

✅ Check for Exposed robots.txt and Sensitive Files (.env, .git, backup files)

✅ Basic XSS & SQL Injection Testing

✅ TLS/SSL Certificate Validation

✅ Subdomain Enumeration using a wordlist

✅ Crawl Internal Links for recursive testing

✅ Generates a report (reports/output.txt)

Installation

git clone https://github.com/your-username/vuln-scanner.git
cd vuln-scanner

Install dependencies:

pip install -r requirements.txt

Usage
Run the tool:

python main.py

Enter the target URL when prompted:

Enter target URL: http://testphp.vulnweb.com/

Select a scanning option from the menu:

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

Generated reports are saved in:

reports/output.txt

Project Structure:

vuln_scanner/
│── main.py                # Main script with menu & report
│── modules/
│   ├── open_directory.py
│   ├── security_headers.py
│   ├── http_methods.py
│   ├── sensitive_files.py
│   ├── xss_sql.py
│   ├── ssl_check.py
│   ├── subdomain_enum.py
│   ├── crawler.py
│── reports/
│   └── output.txt
│── requirements.txt
│── README.md


📦 Requirements

Python 3.x

Install from requirements.txt:

requests

beautifulsoup4

dnspython

pyOpenSSL

cryptography

pyfiglet (optional, for banner)

colorama (optional, for colored output)

tldextract















