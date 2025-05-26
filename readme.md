# 🚀 Rocket LMS - Default Credential Login Checker & File Manager Access

📌 **Product Information**  
**Platform:** Rocket LMS  
**Affected Feature:** Admin Login Endpoint  
**Tested Vulnerability:** Weak Default Credentials + Filemanager Access  
**CVE:** Not Assigned  
**Severity:** Medium (Authentication Bypass by Default Credentials)  
**CWE ID:** CWE-521  
**CWE Name:** Weak Password Requirements  
**Patched:** ❌ Not Applicable  
**Patch Priority:** 🟠 Medium  
**Date Published:** May 27, 2025  
**Researcher:** [https://medium.com/@naxtarrr/rocket-lms-shell-upload-vulnerability-c400665702f3](https://medium.com/@naxtarrr/rocket-lms-shell-upload-vulnerability-c400665702f3)

---

## ⚠️ Summary of the Vulnerability

Many Rocket LMS installations ship with **default administrator and user credentials** such as:

- `admin@demo.com : admin`
- `student@demo.com : student`
- `instructor@demo.com : instructor`

The login form located at `/admin/login` allows unauthenticated access to privileged accounts if those default credentials are not removed.

After successful login, attackers can often access sensitive endpoints like `/filemanager` or `/laravel-filemanager` without further authentication.

If exploited, this issue allows attackers to:

- Access private file manager interfaces
- Upload web shells or malicious content
- Browse sensitive server-side files

---

## 🧪 Proof of Concept (PoC)

**Sample POST Request:**

```http
POST /admin/login HTTP/2
Host: target-site.com
Cookie: XSRF-TOKEN=...; rocketlms_session=...
Content-Type: application/x-www-form-urlencoded

_token=EXTRACTED_TOKEN&email=admin@demo.com&password=admin
```

If successful, attacker is redirected to `/admin/dashboard`.

Then visit:

- `https://target-site.com/filemanager`
- `https://target-site.com/laravel-filemanager`

**Indicators of Success:**
- Status `HTTP/2 200 OK`
- HTML content includes `<title>File Manager</title>` or `cropper.min.css`

---

## 🔍 Where’s the Flaw?

- Admin panel login accepts known default emails with weak passwords.
- Developers or users often forget to delete these demo accounts.
- No brute-force protection or rate-limiting in some deployments.
- If login succeeds, the filemanager is exposed with full access.

---

## 🔐 Recommendation

- **Delete default users:** Ensure `admin@demo.com`, `student@demo.com`, and others are removed.
- **Restrict access to file managers** via authentication middleware.
- **Add rate-limiting** or WAF protection on `/admin/login`.
- **Audit for forgotten demo credentials** or staging deployments exposed publicly.
- **Change all weak passwords** and enforce strong password policies.

---

## 📁 Script Features

This repository includes a Python script that:

- Performs login attempts using default credentials.
- Checks for access to `/filemanager` or `/laravel-filemanager`.
- Classifies results based on user role:
  - `result_admin.txt`
  - `result_student.txt`
  - `result_instructor.txt`
  - `result_need_register.txt` (if all logins fail)

---

## ⚠️ Disclaimer

This script is intended for **authorized testing**, auditing, and educational purposes only.  
Do **not** use it on systems without explicit permission.  
Unauthorized exploitation may violate laws and ethical guidelines.

---
