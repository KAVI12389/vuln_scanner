import requests

def check(url):
    try:
        resp = requests.get(url + "/", timeout=10)
        if "Index of /" in resp.text:
            return "[!] Open Directory Listing Found"
        else:
            return "[+] No open directory listing"
    except Exception as e:
        return f"[ERROR] {e}"
