import requests
from bs4 import BeautifulSoup

def check(url):
    try:
        if not url.endswith("/"):
            url += "/"

        resp = requests.get(url, timeout=20, allow_redirects=True)
        resp.raise_for_status()
        content = resp.text.lower()

        # --- Step 1: Check indicators ---
        indicators = ["index of", "parent directory", "last modified", "directory listing"]
        keyword_found = any(word in content for word in indicators)

        # --- Step 2: Extract file/folder links ---
        soup = BeautifulSoup(resp.text, "html.parser")
        links = [a.get("href") for a in soup.find_all("a", href=True)]

        suspicious = []
        for l in links:
            if not l:
                continue
            # ignore navigation links
            if l.lower() in ["../", "/"]:
                continue
            suspicious.append(l)

        # --- Step 3: Decision ---
        if keyword_found and suspicious:
            found = ", ".join(suspicious[:15])  # show first 15
            if len(suspicious) > 15:
                found += " ..."
            return f"[!!] Directory Listing Enabled at {url} | Open Files/Folders: {found}"

        elif keyword_found:
            return f"[!!] Possible Directory Listing Detected at {url} (but no files extracted)"
        else:
            return f"[+] No open directory listing at {url}"

    # --- Step 4: Advanced error handling ---
    except requests.exceptions.Timeout:
        return f"[ERROR] Timeout while connecting to {url}"
    except requests.exceptions.ConnectionError:
        return f"[ERROR] Connection failed for {url}"
    except requests.exceptions.HTTPError as e:
        return f"[ERROR] HTTP error {e.response.status_code} at {url}"
    except Exception as e:
        return f"[ERROR] Unexpected error at {url}: {e}"




