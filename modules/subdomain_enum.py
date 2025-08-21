# modules/subdomain_enum.py
import requests
import socket
import concurrent.futures
from datetime import datetime
from urllib.parse import urlparse

def check(url):
    """
    Advanced Subdomain Enumeration
    - Input: full URL (http://example.com)
    - Extract domain & check subdomains
    - Return report string
    """
    # --- Extract domain from URL ---
    parsed = urlparse(url)
    domain = parsed.netloc if parsed.netloc else parsed.path

    # Default subdomain list
    subdomains = [
        'www','mail','ftp','admin','api','test','dev','blog',
        'shop','portal','cdn','static','img','video','forum',
        'support','docs','status','vpn','db','app','stage','prod',
        'demo','backup','old','beta','alpha'
    ]

    results = []
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; SubdomainScanner/1.0)'})

    timeout = 3
    threads = 30

    def check_single(sub):
        full_domain = f"{sub}.{domain}"
        data = {'subdomain': full_domain, 'methods': [], 'timestamp': datetime.now().isoformat()}
        found = False

        # DNS resolution
        try:
            ip = socket.gethostbyname(full_domain)
            data['ip'] = ip
            data['methods'].append('dns')
            found = True
        except:
            return None

        # HTTP probing
        for proto in ['https', 'http']:
            url = f"{proto}://{full_domain}"
            try:
                r = session.get(url, timeout=timeout, allow_redirects=True)
                data['status'] = r.status_code
                data['url'] = r.url
                data['methods'].append('http')
                break
            except:
                continue

        return data if found else None

    # Multithreading
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(check_single, s) for s in subdomains]
        for f in concurrent.futures.as_completed(futures):
            res = f.result()
            if res: results.append(res)

    # Format report
    if results:
        report = [f"[+] Subdomain Enumeration for {domain}", "="*60]
        for r in sorted(results, key=lambda x: x['subdomain']):
            methods = '+'.join(r['methods'])
            extras = []
            if 'ip' in r: extras.append(f"IP: {r['ip']}")
            if 'status' in r: extras.append(f"HTTP: {r['status']}")
            report.append(f"  • {r['subdomain']} ({methods}{', ' if extras else ''}{', '.join(extras)})")
        return "\n".join(report)
    else:
        return f"[-] No subdomains found for {domain}"
