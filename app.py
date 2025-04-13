from flask import Flask, request, make_response
import pickle
import os
import subprocess
from utils import get_db_connection

app = Flask(__name__)

# Hardcoded credentials (Security vulnerability)
DB_USER = "admin"
DB_PASS = "SuperSecretPassword123!"

@app.route('/')
def index():
    return "Welcome to the Vulnerable App!"

# SQL Injection vulnerable endpoint
@app.route('/search')
def search():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = request.args.get('q')
    
    # UNSAFE: Direct string concatenation (SQL Injection)
    cursor.execute(f"SELECT * FROM users WHERE name = '{query}'")
    return str(cursor.fetchall())

# Command Injection vulnerable endpoint
@app.route('/ping')
def ping():
    host = request.args.get('host')
    
    # UNSAFE: Shell injection possible
    output = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return output

# Insecure Deserialization
@app.route('/deserialize')
def deserialize():
    data = request.args.get('data')
    
    # UNSAFE: Pickle deserialization
    obj = pickle.loads(bytes.fromhex(data))
    return str(obj)

# XSS vulnerable endpoint
@app.route('/comment')
def comment():
    user_comment = request.args.get('comment')
    return f"<html><body>Your comment: {user_comment}</body></html>"

if __name__ == '__main__':
    # UNSAFE: Debug mode in production
    app.run(debug=True, host='0.0.0.0')