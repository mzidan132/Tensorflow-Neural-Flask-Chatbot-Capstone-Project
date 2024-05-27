from flask import Flask, render_template, session, redirect, url_for, request
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# Dummy user data for demonstration purposes
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()
users = {'user1': '0b14d501a594442a01c6859541bcb3e8164d183d32937b851835442f69d5c94e', 'user2': 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3'}

def is_authenticated():
    return 'username' in session

@app.route('/')
def home():
    if is_authenticated():
        return redirect(url_for('chat'))
    else:
        return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    if username in users and hash_password(password) == users[username]:
        session['username'] = username
        return redirect(url_for('chat'))
    else:
        return render_template('login.html', error='Invalid username or password')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

@app.route('/chat')
def chat():
    if not is_authenticated():
        return redirect(url_for('home'))
    return render_template('index.html', username=session['username'])

@socketio.on('message')
def handleMessage(data):
    print(f'Message: {data["message"]}, Username: {session["username"]}')
    send({'message': data['message'], 'username': session['username']}, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
