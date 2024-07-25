from core.database import db
from dateutil import parser
from datetime import datetime
from .base_model import BaseModel
from core.models.appointment import Appointment
from core.models.availability import Availability
from core.models.medical_record import MedicalRecord
from core.models.transaction import Transaction
from core.utils.utils_ import generate_id, hash_password
from core.models.medical_officer_information import MedicalOfficerInformation


class Account(BaseModel):

    user_id = db.Column(db.String(20), primary_key=True, default=generate_id)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    primary_phone = db.Column(db.String(15))
    secondary_phone = db.Column(db.String(15))
    status = db.Column(db.Integer, default=0)  # 0:not_activated, 1:activated, 2:suspended
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    role = db.Column(db.Integer, default=0)  # 0:patient, 1:doctor
    availability_status = db.Column(db.Integer, default=0)  # 0:not_available, 1:busy, 2:available
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    dob = db.Column(db.Date)
    gender = db.Column(db.Integer)  # 0:male, 1:female, 2:other
    address = db.Column(db.String(255))
    pp_url = db.Column(db.String(255))

    patients = db.relationship(
        'MedicalRecord',
        foreign_keys='MedicalRecord.doctor_id',
        back_populates='doctor'
    )

    medical_records = db.relationship(
        'MedicalRecord',
        foreign_keys='MedicalRecord.patient_id',
        back_populates='patient',
        overlaps='doctor'
    )

    sent_transactions = db.relationship(
        'Transaction',
        foreign_keys='Transaction.sender_id',
        back_populates='sender'
    )

    received_transactions = db.relationship(
        'Transaction',
        foreign_keys='Transaction.receiver_id',
        back_populates='receiver'
    )

    organised_appointments = db.relationship(
        'Appointment',
        foreign_keys='Appointment.organiser_id',
        back_populates='organiser'
    )

    invited_appointments = db.relationship(
        'Appointment',
        foreign_keys='Appointment.invitee_id',
        back_populates='invitee'
    )

    professional_information = db.relationship(
        'MedicalOfficerInformation',
        foreign_keys='MedicalOfficerInformation.user_id',
        back_populates='account'
    )

    availabilities = db.relationship(
        'Availability',
        back_populates='account'
    )

    @staticmethod
    def __name__():
        return "Account"

    def create(self):
        self.password = hash_password(self.password)
        db.session.add(self)
        db.session.commit()

    def sign_up(self):
        credits()
        if self.role != 0:
            professional_info = MedicalOfficerInformation(user_id=self.user_id)
            professional_info.create()

        return self, 200

    @staticmethod
    def sign_in(email, password, role):
        account = Account.query.filter_by(email=email).first()
        if not account or account.password != hash_password(password):
            return None, 401

        if role != 0 and role != account.role:
            return None, 404

        return account, 200

    def sign_out(self, session):
        pass
    
    def update(self, updates=None):
        updatable_keys = [
            "primary_phone",
            "secondary_phone",
            "status",
            "availability_status",
            "first_name",
            "last_name",
            "dob",
            "gender",
            "address",
            "pp_url"
        ]
        
        if updates is not None:
            for key in updates.keys():
                if updates[key] is not None and key in updatable_keys:
                    value = updates[key]
                    if key == "dob":
                        try:
                            date_obj = parser.parse(value)
                            value = date_obj.date()
                        except (ValueError, parser.ParserError):
                            return 1

                    setattr(self, key, value)

        super().update()

        return 0

    def get_details(self):
        keys_to_remove = ['password', 'user_id', 'last_updated']
        details = self.to_dict()
        for key in keys_to_remove:
            del details[key]
        return details

    def create_availability(self, start, end):
        availability = Availability(user_id=self.user_id, start_time=start, end_time=end)
        availability.create()

    def create_medical_record(self, doctor_id):
        record = MedicalRecord(patient_id=self.user_id, doctor_id=doctor_id)
        return record.create()

    def book_appointment(self, invitee_id, mode, location, coordinates, start_time, end_time, purpose):

        appointment = Appointment(
            organiser_id=self.user_id,
            invitee_id=invitee_id,
            mode=mode,
            location=location,
            coordinates=coordinates,
            start_time=start_time,
            end_time=end_time,
            purpose=purpose,
            status='upcoming'
        )

        return appointment.create()

    def make_transaction(self, receiver_id, amount, currency, payment_method, account_number, time, reference_number,
                         description, fee, original_amount, original_currency, exchange_rate):
        transaction = Transaction(
            sender_id=self.user_id,
            receiver_id=receiver_id,
            amount=amount,
            currency=currency,
            payment_method=payment_method,
            account_number=account_number,
            time=time,
            reference_number=reference_number,
            description=description,
            fee=fee,
            original_amount=original_amount,
            original_currency=original_currency,
            exchange_rate=exchange_rate
        )

        return transaction.create()
