import os

from flask import render_template, current_app, url_for
from flask_mail import Message

from app import create_app
from app import mail
from app.models import Serializer

def send_confirmation_email(recipient, subject, template, **kwargs):
    app = create_app(os.getenv('Config'))
    with app.app_context():
        msg = Message(
            subject='Confirm Registration',
            recipients=[recipient])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)

def send_password_email(recipient, subject, template, **kwargs):
    app = create_app(os.getenv('Config'))
    with app.app_context():
        msg = Message(
            subject='Reset Password',
            recipients=[recipient])
        msg.body = render_template(template + '.txt', **kwargs)
        msg.html = render_template(template + '.html', **kwargs)
        mail.send(msg)