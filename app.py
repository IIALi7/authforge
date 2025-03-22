from flask import Flask, request, render_template, redirect, make_response
import base64
import json

app = Flask(__name__)

users = {}

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if user in users and users[user] == pwd:
            session = base64.b64encode(json.dumps({
                'user': user,
                'is_admin': user.lower() == 'admin'
            }).encode()).decode()
            resp = make_response(redirect('/dashboard'))
            resp.set_cookie('session', session)
            return resp
        return 'Invalid credentials'
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        if "admin" in user:
            return 'You cannot register with that name.'
        users[user] = pwd
        return redirect('/login')
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    session_cookie = request.cookies.get('session')
    if not session_cookie:
        return redirect('/login')
    try:
        session = json.loads(base64.b64decode(session_cookie).decode())
        return render_template('dashboard.html', username=session['user'])
    except:
        return 'Invalid session'
    
@app.route('/admin-panel')
def admin_panel():
    session_cookie = request.cookies.get('session')
    if not session_cookie:
        return redirect('/login')
    try:
        session = json.loads(base64.b64decode(session_cookie).decode())
        if session.get('user') == 'admin' and session.get('is_admin') == True:
            return render_template('admin.html', flag="D4rk{you_bypassed_auth_cookie}")
        else:
            return 'You are not admin.'
    except:
        return 'Session error.'

@app.route('/source')
def source():
    return open('app.py').read(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(debug=True)
