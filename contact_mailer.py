from flask import request, jsonify, Blueprint, current_app
from flask_mail import Message
import os

contact_mailer_bp = Blueprint('contact_mailer', __name__)

@contact_mailer_bp.route('/send-contact', methods=['POST'])
def send_contact():
    data = request.get_json()
    name = data.get('name', '')
    email = data.get('email', '')
    message = data.get('message', '')
    if not (name and email and message):
        return jsonify({'success': False, 'error': 'All fields required'}), 400

    # Use current_app to get the Mail instance
    mail = current_app.extensions['mail']
    msg = Message(
        subject=f"Portfolio Contact: {name}",
        recipients=[current_app.config['MAIL_USERNAME']],
        body=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
    )
    try:
        mail.send(msg)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500