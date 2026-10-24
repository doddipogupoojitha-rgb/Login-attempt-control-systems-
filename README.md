# Login Attempt Control System 🔐

Prevents brute-force attacks by locking accounts after 5 failed attempts for 15 minutes.

## Objective
- Rate limiting
- Track failed counters by Username/IP
- Temporary lockout mechanism

## Features
- ✅ Track failed logins by Username/IP
- ✅ 15-min lockout after 5 failures
- ✅ Progressive delay (2s * attempts)
- ✅ Security audit logging to logs/security_audit.log
- ✅ Brute-force test script
- ✅ REST API: /api/status/<username> (optional)

## How to Test (Proof Required)

### 1. Run brute-force simulation:
python test_bruteforce.py

Output shows:
Attempt 1: ❌ FAILED
...
Attempt 5: 🔒 ACCOUNT LOCKED

### 2. Run web app:
pip install -r requirements.txt
python app.py

Try 5 wrong logins -> See ⛔ ACCOUNT LOCKED!

### Logs
logs/security_audit.log contains lockout events - Submit as proof

## Tech Stack
Flask, Python, Session, datetime

## Intern
Doddipogu Poojitha | Workora Internship
