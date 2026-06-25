# Secure Flask API

A deliberately vulnerable → secure e-commerce API demonstrating OWASP Top 10 mitigations.

## What's Inside
| Version | Status | Key Issues |
|---------|--------|-----------|
| `vulnerable/` | ❌ Intentionally broken | SQL Injection, Broken Auth, Plaintext passwords |
| `secure/` | ✅ Hardened | Parameterized queries, JWT, RBAC, Input validation |

## Quick Start
```bash
# Vulnerable (for testing)
cd vulnerable && pip install -r requirements.txt && python app.py

# Secure
cd secure && pip install -r requirements.txt && python app.py

Security Tests
pytest tests/ -v

CI/CD
Bandit (SAST) on every push
Safety (dependency scanning)
pytest security test suite


4. Commit message: `docs: update main README`
5. Click **"Commit changes"**

---

## What Your Repo Should Look Like Now

Go to `https://github.com/hum-gaire/Secure-Flask-api` and confirm you see:

secure-flask-api/
├── .github/
│   └── workflows/
│       └── security.yml
├── secure/
│   ├── app.py
│   ├── auth.py
│   ├── models.py
│   ├── validators.py
│   └── requirements.txt
├── tests/
│   ├── test_vulnerable.py
│   └── test_secure.py
├── vulnerable/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
└── README.md


---

## Next: Check the Actions Tab

1. Click the **Actions** tab at the top of your repo
2. You should see a workflow run (or click **"Enable workflows"** if prompted)
3. If it runs, you'll see green checkmarks ✅

**If you get stuck on any specific file, tell me which one and I'll help.**
