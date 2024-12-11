from flask import Flask, request, jsonify
from prometheus_client import Counter, Histogram, generate_latest
import os
import requests
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'Request latency', ['endpoint'])

@app.route('/metrics')
def metrics():
    return generate_latest(), 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/notify', methods=['POST'])
def notify_user():
    with REQUEST_LATENCY.labels(endpoint='/post').time():
        REQUEST_COUNT.labels(method=request.method, endpoint='/post').inc()

        data = request.get_json()
        email_server_address = os.environ.get('EMAIL_SERVER_ADDRESS','')
        email_server_from = os.environ.get('EMAIL_SERVER_FROM','')
        email_server_key = os.environ.get('EMAIL_SERVER_KEY','')
        email_server_port = os.environ.get('EMAIL_SERVER_PORT','')

        # User 서비스로부터 사용자 정보 조회
        response = requests.get(f'http://user-service:5001/users/{data["userid"]}')
        #response = requests.get(f'http://127.0.0.1:5001/users/{data["userid"]}')
        if response.status_code == 200:
            user = response.json()
            print(f'Sending notification to {user["email"]}: New post titled "{data["title"]}"')

            server = smtplib.SMTP(email_server_address, email_server_port)
            server.starttls()

            try:
                server.login(email_server_from, email_server_key)

                msg = MIMEMultipart()
                msg["From"] = email_server_from
                msg["To"] = user["email"]
                msg["Subject"] = data["title"]
                msg.attach(MIMEText(data["content"], 'plain'))

                server.sendmail(email_server_from, user["email"], msg.as_string())

                return jsonify({'message': 'Notification sent'}), 200

            except smtplib.SMTPAuthenticationError as e:
                return jsonify({'error': 'Email Server not valid'}), 404

        else:
            return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)

