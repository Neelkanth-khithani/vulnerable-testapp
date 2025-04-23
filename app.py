from flask import Flask, request, make_response
import pickle
import os
import subprocess
from utils import get_db_connection

app = Flask(__name__)

DB_USER = "admin"
DB_PASS = "SuperSecretPassword12345"

@app.route('/')
def index():
    return "Welcome to the Vulnerable App!"

@app.route('/search')
def search():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = request.args.get('q')
    
    cursor.execute(f"SELECT * FROM users WHERE name = '{query}'")
    return str(cursor.fetchall())

@app.route('/ping')
def ping():
    host = request.args.get('host')
    
    output = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return output

@app.route('/deserialize')
def deserialize():
    data = request.args.get('data')
    
    obj = pickle.loads(bytes.fromhex(data))
    return str(obj)

@app.route('/comment')
def comment():
    user_comment = request.args.get('comment')
    return f"<html><body>Your comment: {user_comment}</body></html>"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')