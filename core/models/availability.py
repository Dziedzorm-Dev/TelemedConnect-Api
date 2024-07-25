from core.database import db
from .base_model import BaseModel
from datetime import datetime
from core.utils.utils_ import generate_id


class Availability(BaseModel):
    id = db.Column(db.String(20), primary_key=True, default=generate_id)
    user_id = db.Column(db.String(20), db.ForeignKey('account.user_id', name='fk_availability_user_id'), nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    account = db.relationship(
        'Account',
        back_populates='availabilities'
    )

    @staticmethod
    def __name__():
        return "Availability"
