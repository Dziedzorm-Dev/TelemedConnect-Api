import uuid

from flask import jsonify

from core.database import db
from datetime import datetime, timedelta
from .base_model import BaseModel
from core.utils.utils_ import generate_token
from core.utils.email_service import send_email


class OTP(BaseModel):
    id = db.Column(db.String, primary_key=True)
    user_id = db.Column(db.String(20), db.ForeignKey('account.user_id', name='fk_otp_user_id'), nullable=False)
    otp_token = db.Column(db.String(12), nullable=False)
    otp_code = db.Column(db.String(4), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    @staticmethod
    def __name__():
        return "OTP"

    @staticmethod
    def generate_otp(account):
        otp_token = generate_token()
        otp_code = str(uuid.uuid4().int)[:4]

        new_otp = OTP(
            id=generate_token(),
            user_id=account.user_id,
            otp_token=otp_token,
            otp_code=otp_code
        )

        new_otp.create()

        subject = "TelemedConnect OTP"
        message = "Your OTP code is {}".format(otp_code)
        send_email(account.email, subject, message)

        return otp_token

    @staticmethod
    def resend_otp(code, email):
        subject = "TelemedConnect OTP"
        message = "Your OTP code is {}".format(code)
        send_email(email, subject, message)

    def is_expired(self):
        return datetime.utcnow() - self.date_created > timedelta(minutes=5)
