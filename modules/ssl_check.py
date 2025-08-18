import ssl
import socket
from datetime import datetime

def check(url):
    try:
        # Extract hostname
        if url.startswith("http://"):
            return "[!] Target does not use HTTPS"
        hostname = url.replace("https://", "").split("/")[0]

        ctx = ssl.create_default_context()
        with socket.create_connection((hostname, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()

        # Extract fields
        subject = dict(x[0] for x in cert.get("subject", []))
        issuer = dict(x[0] for x in cert.get("issuer", []))
        issued_to = subject.get("commonName", "")
        issued_by = issuer.get("commonName", "")
        not_before = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z")
        not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
        days_left = (not_after - datetime.utcnow()).days

        result = [f"[+] TLS Certificate Info for {hostname}"]
        result.append(f" - Issued To: {issued_to}")
        result.append(f" - Issued By: {issued_by}")
        result.append(f" - Valid From: {not_before}")
        result.append(f" - Valid Until: {not_after}")
        result.append(f" - Days Left: {days_left}")

        # Warnings
        if datetime.utcnow() < not_before:
            result.append("[!] Certificate is NOT YET valid")
        if datetime.utcnow() > not_after:
            result.append("[!] Certificate has EXPIRED")
        elif days_left < 30:
            result.append("[!] Certificate expiring soon (<30 days)")

        # Self-signed check
        if issued_to == issued_by:
            result.append("[!] Self-signed certificate detected")

        return "\n".join(result)

    except Exception as e:
        return f"[ERROR] {e}"
