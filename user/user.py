from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
    conn.commit()
    conn.close()

@app.route('/users', methods=['POST'])
def create_user():
    user = request.get_json()
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("INSERT INTO users (name, email) VALUES (?, ?)", (user['name'], user['email']))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    return jsonify({'id': user_id}), 201

@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = c.fetchone()
    conn.close()
    if user:
        return jsonify({'id': user[0], 'name': user[1], 'email': user[2]})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users', methods=['GET'])
def get_all_users():
    conn = sqlite3.connect('test.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users")
    users = c.fetchall()
    conn.close()
    return jsonify([{'id': row[0], 'name': row[1], 'email': row[2]} for row in users])

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5001)
