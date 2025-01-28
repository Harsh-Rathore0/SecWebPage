from flask import Flask, request, jsonify, abort, send_from_directory, redirect, url_for, session
from flask_mysqldb import MySQL
import bcrypt
import requests
import os

# Initialize Flask app
app = Flask(__name__, static_folder='../frontend')

# Secret key for session management
app.secret_key = os.urandom(24)  # Change this to a secure key in production

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'your-database-name-here'

mysql = MySQL(app)

app.config['SESSION_COOKIE_SECURE'] = True  # Use HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# reCAPTCHA Secret Key
RECAPTCHA_SECRET_KEY = "your-secret-key-here"

# Helper function to verify reCAPTCHA
def verify_recaptcha(response_token):
    payload = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': response_token
    }
    response = requests.post("https://www.google.com/recaptcha/api/siteverify", data=payload)
    result = response.json()
    return result.get('success', False)

@app.route('/register')
def serve_register():
    return send_from_directory(app.static_folder, 'reg.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'User')  # Default is 'User'
    recaptcha_response = data.get('recaptcha_response')

    if not verify_recaptcha(recaptcha_response):
        return jsonify({"message": "reCAPTCHA verification failed"}), 400

    if not username or not email or not password:
        abort(400, "All fields are required")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    cur = mysql.connection.cursor()
    try:
        cur.execute("INSERT INTO users (username, email, password, role) VALUES (%s, %s, %s, %s)", 
                    (username, email, hashed_password.decode('utf-8'), role))
        mysql.connection.commit()
        return jsonify({"redirect": "/"}), 201  #login page to registration redirect
    except Exception as e:
        mysql.connection.rollback()
        return jsonify({"message": "Registration failed", "error": str(e)}), 500
    finally:
        cur.close()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    recaptcha_response = data.get('recaptcha_response')

    if not verify_recaptcha(recaptcha_response):
        return jsonify({"message": "reCAPTCHA verification failed"}), 400

    if not email or not password:
        abort(400, "Email and password are required")

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cur.fetchone()

    if user and bcrypt.checkpw(password.encode('utf-8'), user[3].encode('utf-8')):  # user[3] is the hashed password column
        session['user_id'] = user[0]
        session['role'] = user[4]
        
        return jsonify({"message": "Login successful", "role": user[4]}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/dashboard')
def serve_dashboard():
    if 'user_id' in session:
        if session['role'] == 'Admin':
            return send_from_directory(app.static_folder, 'admin_dashboard.html')
        else:
            return send_from_directory(app.static_folder, 'user_dashboard.html')
    return redirect(url_for('serve_login'))


@app.route('/logout')
def logout():
    session.clear()  # Clear the session on logout
    return redirect(url_for('serve_login'))

@app.route('/')
def serve_login():
    return send_from_directory(app.static_folder, 'login.html')

if __name__ == '__main__':
    app.run(debug=True)