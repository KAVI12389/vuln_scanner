import ssl, socket

def check(url):
    try:
        hostname = url.replace("http://", "").replace("https://", "").split("/")[0]
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=hostname) as s:
            s.settimeout(5)
            s.connect((hostname, 443))
            cert = s.getpeercert()
            return f"[+] SSL Certificate Valid: {cert['subject']}"
    except Exception as e:
        return f"[ERROR] SSL Check Failed: {e}"
