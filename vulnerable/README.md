# Vulnerable Flask API

**DO NOT USE IN PRODUCTION**

This version intentionally demonstrates OWASP Top 10 vulnerabilities.

## Vulnerabilities Present
- **A01: Broken Access Control** — No auth on `/order`, no authorization on `/admin/users`
- **A03: Injection** — SQL injection in authentication and order endpoints
- **A02: Cryptographic Failures** — Passwords stored in plaintext, weak session secret

## Run
```bash
pip install -r requirements.txt
python app.py
