from flask import Flask, request, jsonify
import smtplib
import os

app = Flask(__name__)

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json
    receiver_email = data.get('receiver_email')
    subject = data.get('subject')
    body_text = data.get('body_text')

    if not receiver_email or not subject or not body_text:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        smtp_host = os.getenv('SMTP_HOST')
        smtp_port = int(os.getenv('SMTP_PORT'))
        smtp_user = os.getenv('SMTP_USER')
        smtp_pass = os.getenv('SMTP_PASS')

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            message = f"Subject: {subject}\n\n{body_text}"
            server.sendmail(smtp_user, receiver_email, message)

        return jsonify({'message': 'Email sent successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
