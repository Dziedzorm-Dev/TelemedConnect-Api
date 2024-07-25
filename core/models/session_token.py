import uuid

from flask_jwt_extended import create_access_token
from .base_model import BaseModel
from .otp import OTP
from core.database import db
from datetime import datetime, timedelta
from ..utils.utils_ import generate_id


class SessionToken(BaseModel):
    id = db.Column(db.String, primary_key=True, default=generate_id)
    user_id = db.Column(db.String(20), db.ForeignKey('account.user_id', name='fk_session_user_id'), nullable=False)
    session_token = db.Column(db.String, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    @staticmethod
    def create_token(user_id, role, use, exp_time):

        if exp_time is None:
            access_token = create_access_token(
                identity=user_id,
                fresh=True,
                additional_claims={'role': role, 'use': use}
            )
        else:

            expiration = timedelta(minutes=exp_time)
            access_token = create_access_token(
                identity=user_id,
                expires_delta=expiration,
                additional_claims={'role': role, 'use': use}
            )

        session = SessionToken(
            user_id=user_id,
            session_token=access_token,
            is_active=True
        )

        session.create()
        return access_token

    @staticmethod
    def clean_expired_tokens():
        expiration_time = datetime.utcnow() - timedelta(minutes=10)
        expired_tokens = OTP.query.filter(OTP.date_created < expiration_time).all()
        for token in expired_tokens:
            db.session.delete(token)
        db.session.commit()

    @staticmethod
    def __name__():
        return "SessionToken"
