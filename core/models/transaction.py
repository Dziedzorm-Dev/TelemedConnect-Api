from core.database import db
from datetime import datetime
from .base_model import BaseModel
from core.utils.utils_ import generate_id


class Transaction(BaseModel):
    id = db.Column(db.String(20), primary_key=True, default=generate_id)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    status = db.Column(db.String(20), default='Pending', nullable=False)
    sender_id = db.Column(db.String(36), db.ForeignKey('account.user_id', name='fk_transaction_sender_id'), nullable=False)
    receiver_id = db.Column(db.String(36), db.ForeignKey('account.user_id', name='fk_transaction_receiver_id'), nullable=False)
    payment_method = db.Column(db.String(36), nullable=False)
    account_number = db.Column(db.String(50), nullable=False)
    reference_number = db.Column(db.String(50), nullable=False, unique=True, default=generate_id)
    description = db.Column(db.String(255))
    fee = db.Column(db.Float, nullable=False)
    exchange_rate = db.Column(db.Float, nullable=False)
    original_amount = db.Column(db.Float, nullable=False)
    original_currency = db.Column(db.String(3), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    sender = db.relationship(
        'Account', foreign_keys=[sender_id], back_populates='sent_transactions'
    )

    receiver = db.relationship(
        'Account', foreign_keys=[receiver_id], back_populates='received_transactions'
    )

    @staticmethod
    def __name__():
        return "Transaction"

    def __delete__(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
