from flask import Flask, render_template, request, redirect, session
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'workora_security_2024'

failed_attempts = {}
lockouts = {}
security_logs = []
USERS = {"admin": "admin123", "poojitha": "poojitha123", "test": "test123"}

MAX_ATTEMPTS = 5
LOCKOUT_MINUTES = 15

def log_event(username, ip, status, reason=""):
    log = f"[{datetime.now()}] USER={username} IP={ip} STATUS={status} REASON={reason}"
    security_logs.append(log)
    os.makedirs("logs", exist_ok=True)
    with open("logs/security_audit.log", "a") as f:
        f.write(log + "\n")
    print(log)

def is_locked(username):
    if username in lockouts:
        if datetime.now() < lockouts[username]:
            return True, lockouts[username]
        else:
            del lockouts[username]
            failed_attempts[username] = 0
    return False, None

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ""
    ip = request.remote_addr
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        locked, until = is_locked(username)
        if locked:
            remaining = (until - datetime.now()).seconds // 60
            message = f"⛔ ACCOUNT LOCKED! Try after {remaining} mins."
            log_event(username, ip, "LOCKED_ATTEMPT", f"Locked till {until}")
            return render_template('login.html', message=message, logs=security_logs[-5:])
        if username in USERS and USERS[username] == password:
            failed_attempts[username] = 0
            log_event(username, ip, "SUCCESS", "Login successful")
            session['user'] = username
            return redirect('/dashboard')
        else:
            failed_attempts[username] = failed_attempts.get(username, 0) + 1
            count = failed_attempts[username]
            if count >= MAX_ATTEMPTS:
                lockouts[username] = datetime.now() + timedelta(minutes=LOCKOUT_MINUTES)
                message = f"🔒 LOCKED for {LOCKOUT_MINUTES} mins after {count} fails!"
                log_event(username, ip, "LOCKOUT", f"Locked after {count}")
            else:
                message = f"❌ Wrong password! {count}/{MAX_ATTEMPTS}. {MAX_ATTEMPTS-count} left."
                log_event(username, ip, "FAILED", f"Attempt {count}")
    return render_template('login.html', message=message, logs=security_logs[-10:], attempts=failed_attempts, lockouts=lockouts)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return render_template('dashboard.html', user=session['user'], logs=security_logs)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
