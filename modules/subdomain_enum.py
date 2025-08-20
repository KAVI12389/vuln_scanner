import requests
import socket
import concurrent.futures
import argparse
import json
from datetime import datetime

def check(url):
    parser = argparse.ArgumentParser(description="Complete Subdomain Enumeration Tool")
    parser.add_argument("domain", help="Target domain to enumerate")
    parser.add_argument("-w", "--wordlist", help="Subdomain wordlist file")
    parser.add_argument("-o", "--output", help="Output file path")
    parser.add_argument("-f", "--format", choices=['txt', 'json', 'csv'], default='txt',
                       help="Output format (default: txt)")
    parser.add_argument("-t", "--threads", type=int, default=50, help="Number of threads")
    parser.add_argument("--timeout", type=int, default=3, help="Request timeout in seconds")
    parser.add_argument("--methods", nargs='+', default=['dns', 'http'],
                       choices=['dns', 'http'], help="Enumeration methods")
    parser.add_argument("--quiet", action='store_true', help="Quiet mode (no verbose output)")
    args = parser.parse_args()

    domain = args.domain
    wordlist_file = args.wordlist
    threads = args.threads
    timeout = args.timeout
    methods = args.methods
    output_file = args.output
    output_format = args.format
    verbose = not args.quiet

    # Default wordlist if none provided
    if wordlist_file is None:
        subdomains = [
            'www', 'mail', 'ftp', 'admin', 'api', 'test', 'dev', 'blog',
            'shop', 'web', 'portal', 'cdn', 'static', 'assets', 'img',
            'images', 'video', 'videos', 'download', 'uploads', 'forum',
            'support', 'help', 'docs', 'wiki', 'status', 'monitor',
            'dashboard', 'panel', 'control', 'secure', 'ssl', 'vpn',
            'remote', 'ssh', 'db', 'database', 'sql', 'nosql', 'redis',
            'cache', 'proxy', 'balancer', 'load', 'app', 'application',
            'service', 'services', 'internal', 'external', 'stage', 'staging',
            'prod', 'production', 'live', 'demo', 'backup', 'archive',
            'old', 'new', 'temp', 'tmp', 'beta', 'alpha', 'gamma', 'delta'
        ]
        if verbose:
            print("Using default wordlist with common subdomains")
    else:
        try:
            with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as f:
                subdomains = [line.strip() for line in f if line.strip() and not line.startswith('#')]
            if verbose:
                print(f"Loaded {len(subdomains)} subdomains from {wordlist_file}")
        except FileNotFoundError:
            print(f"Error: Wordlist file '{wordlist_file}' not found!")
            return 1
        except Exception as e:
            print(f"Error reading wordlist: {e}")
            return 1

    if verbose:
        print(f"Starting enumeration for {domain} with {len(subdomains)} subdomains...")
        print(f"Methods: {methods}, Threads: {threads}, Timeout: {timeout}s")

    results = []
    session = requests.Session()
    session.headers.update({'User-Agent': 'Mozilla/5.0 (compatible; SubdomainScanner/1.0)'})

    def check_single(subdomain):
        full_domain = f"{subdomain}.{domain}"
        result = {'subdomain': full_domain, 'methods': [], 'timestamp': datetime.now().isoformat()}
        found = False

        # DNS
        if 'dns' in methods:
            try:
                ip_address = socket.gethostbyname(full_domain)
                result['ip_address'] = ip_address
                result['methods'].append('dns')
                found = True
            except socket.gaierror:
                pass
            except Exception as e:
                if verbose:
                    print(f"DNS error for {full_domain}: {e}")

        # HTTP
        if 'http' in methods and not found:
            for protocol in ['https', 'http']:
                url = f"{protocol}://{full_domain}"
                try:
                    response = session.get(url, timeout=timeout, allow_redirects=True)
                    result['status_code'] = response.status_code
                    result['url'] = response.url
                    result['protocol'] = protocol
                    result['methods'].append('http')
                    result['content_length'] = len(response.content)
                    found = True
                    break
                except requests.exceptions.RequestException:
                    continue
        return result if found else None

    # Thread pool
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:
        future_to_sub = {executor.submit(check_single, s): s for s in subdomains}
        for i, future in enumerate(concurrent.futures.as_completed(future_to_sub)):
            sub = future_to_sub[future]
            try:
                result = future.result()
                if result:
                    results.append(result)
                    if verbose:
                        methods_str = '+'.join(result['methods'])
                        status = result.get('status_code', 'DNS')
                        print(f"✓ Found: {result['subdomain']} ({methods_str}, Status: {status})")
            except Exception as e:
                if verbose:
                    print(f"Error processing {sub}: {e}")
            if verbose and (i + 1) % 100 == 0:
                print(f"Processed {i+1}/{len(subdomains)} subdomains...")

    # Save results
    if output_file and results:
        try:
            if output_format == 'txt':
                with open(output_file, 'w') as f:
                    for r in results:
                        f.write(f"{r['subdomain']}\n")
            elif output_format == 'json':
                with open(output_file, 'w') as f:
                    json.dump(results, f, indent=2)
            elif output_format == 'csv':
                with open(output_file, 'w') as f:
                    f.write("subdomain,ip_address,status_code,protocol,methods,content_length\n")
                    for r in results:
                        f.write(f"{r['subdomain']},{r.get('ip_address','N/A')},"
                                f"{r.get('status_code','N/A')},{r.get('protocol','N/A')},"
                                f"{'+'.join(r.get('methods', []))},{r.get('content_length','N/A')}\n")
            if verbose:
                print(f"Results saved to {output_file} ({output_format})")
        except Exception as e:
            print(f"Error saving results: {e}")

    # Summary
    if verbose:
        print("\n" + "="*50)
        print("ENUMERATION SUMMARY")
        print("="*50)
        print(f"Target domain: {domain}")
        print(f"Subdomains checked: {len(subdomains)}")
        print(f"Subdomains found: {len(results)}")
        print(f"Success rate: {(len(results)/len(subdomains)*100):.1f}%")

        if results:
            print("\nFound subdomains:")
            for r in sorted(results, key=lambda x: x['subdomain']):
                methods_str = '+'.join(r['methods'])
                extras = []
                if 'ip_address' in r: extras.append(f"IP: {r['ip_address']}")
                if 'status_code' in r: extras.append(f"HTTP: {r['status_code']}")
                print(f"  • {r['subdomain']} ({methods_str}{', ' if extras else ''}{', '.join(extras)})")
        else:
            print("\nNo subdomains found.")

    return 0 if results else 1


if __name__ == "__main__":
    exit(url())
