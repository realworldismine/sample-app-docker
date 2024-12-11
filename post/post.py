from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest
import sqlite3
import requests
import jwt
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency', ['endpoint'])

def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS post
                 (id INTEGER PRIMARY KEY, title TEXT, content TEXT, userid INTEGER)''')
    conn.commit()
    conn.close()

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

# 토큰 생성
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data['username'] == 'admin' and data['password'] == 'password':
        token = jwt.encode({'user': data['username'], 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'], algorithm='HS256')
        return jsonify({'token': token})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

# 보호된 경로
@app.route('/protected', methods=['GET'])
def protected():
    token = request.headers.get('Authorization').split()[1]
    try:
        data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({"message": "Access granted", "user": data['user']})
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401

@app.route('/post', methods=['POST'])
def post():
    with REQUEST_LATENCY.labels(endpoint='/post').time():
        REQUEST_COUNT.labels(method=request.method, endpoint='/post').inc()
        post = request.get_json()
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("INSERT INTO post (title, content, userid) VALUES (?, ?, ?)", (post['title'], post['content'], post['userid']))
        conn.commit()
        post_id = c.lastrowid
        conn.close()

    # Notification 서비스 호출
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    requests.post(f'http://notification-service:5003/notify', json=post, headers=headers)
    #requests.post('http://127.0.0.1:5003/notify', json=post, headers=headers)
    return jsonify({'id': post_id}), 201

@app.route('/post/<int:id>', methods=['GET'])
def get_post(id):
    with REQUEST_LATENCY.labels(endpoint='/post').time():
        REQUEST_COUNT.labels(method=request.method, endpoint='/post').inc()
        conn = sqlite3.connect('test.db')
        c = conn.cursor()
        c.execute("SELECT * FROM post WHERE id = ?", (id,))
        post = c.fetchone()
        conn.close()

        if post:
            return jsonify({'id': post[0], 'title': post[1], 'content': post[2], 'userid': post[3]})
        else:
            return jsonify({'error': 'Post not found'}), 404

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5002, debug=True)
