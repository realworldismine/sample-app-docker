from flask import Flask, request, jsonify
import os
import requests
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route('/notify', methods=['POST'])
def notify_user():
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
    app.run(port=5003, debug=True)
