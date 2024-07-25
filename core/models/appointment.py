from core.database import db
from datetime import datetime
from core.utils.utils_ import generate_id
from .base_model import BaseModel


class Appointment(BaseModel):
    id = db.Column(db.String(20), primary_key=True, default=generate_id)
    organiser_id = db.Column(db.String(20), db.ForeignKey('account.user_id', name='fk_appointment_organiser'), nullable=False)
    invitee_id = db.Column(db.String(20), db.ForeignKey('account.user_id', name='fk_appointment_invitee'), nullable=False)
    mode = db.Column(db.String(255), nullable=False)  # virtual or in-person
    location = db.Column(db.String(255), nullable=True)
    coordinates = db.Column(db.String(255), nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    purpose = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='upcoming')
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    organiser = db.relationship(
        'Account',
        foreign_keys=[organiser_id],
        back_populates='organised_appointments'
    )

    invitee = db.relationship(
        'Account',
        foreign_keys=[invitee_id],
        back_populates='invited_appointments'
    )

    @staticmethod
    def __name__():
        return "Appointment"
