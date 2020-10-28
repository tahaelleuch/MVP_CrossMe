#!/usr/bin/python3

from flask_mail import Mail, Message
from flask import render_template


class Mailings():
    def __init__(self, myStr = "", subj = "", user="", token=""):
        self.mail_settings = {
            "MAIL_SERVER": 'smtp.gmail.com',
            "MAIL_PORT": 465,
            "MAIL_USE_TLS": False,
            "MAIL_USE_SSL": True,
            "MAIL_USERNAME": '',
            "MAIL_PASSWORD": ''
        }
        self.myStr = myStr
        self.subj = subj
        self.receipt = user
        self.token = token
    def send(self):
        from web_front.CrossMe import app
        app.config.update(self.mail_settings)
        mail = Mail(app)
        with app.app_context():
            msg = Message(
                subject=self.subj,
                sender=('Crossme', 'crossmewebsite@gmail.com'),
                recipients=[self.receipt.email])
            msg.html = render_template(self.myStr, user=self.receipt.full_name,token=self.token)
            mail.send(msg)