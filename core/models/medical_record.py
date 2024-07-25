from core.database import db
from datetime import datetime
from .base_model import BaseModel
from core.models.test_scan import TestScan
from core.models.treatment_plan import TreatmentPlan
from core.utils.utils_ import generate_id


class MedicalRecord(BaseModel):
    id = db.Column(db.String(20), primary_key=True, default=generate_id)
    patient_id = db.Column(db.String(20), db.ForeignKey('account.user_id', name='fk_medical_record_patient_id'), nullable=False)
    doctor_id = db.Column(db.String(20), db.ForeignKey('account.user_id', name='fk_medical_record_doctor_id'), nullable=False)
    diagnosis = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    previous_consultation = db.Column(db.String(20), db.ForeignKey('medical_record.id', name='fk_medical_record_previous_consultation'))
    symptoms = db.Column(db.String(255))
    first_aid = db.Column(db.String(255))
    blood_pressure = db.Column(db.String(20))
    heart_rate = db.Column(db.Integer)
    respiratory_rate = db.Column(db.Integer)
    temperature = db.Column(db.Float)
    oxygen_saturation = db.Column(db.Float)

    doctor = db.relationship(
        'Account',
        foreign_keys=[doctor_id],
        back_populates='patients'
    )

    patient = db.relationship(
        'Account',
        foreign_keys=[patient_id],
        back_populates='medical_records'
    )

    test_scan = db.relationship(
        'TestScan',
        foreign_keys='TestScan.medical_record_id',
        back_populates='medical_record'
    )

    treatment_plan = db.relationship(
        'TreatmentPlan',
        foreign_keys='TreatmentPlan.medical_record_id',
        back_populates='medical_record'
    )

    @staticmethod
    def __name__():
        return "MedicalRecord"

    def creat_test_scan(self):
        test_scan = TestScan(medical_record_id=self.id)
        test_scan.create()

        return test_scan

    def create_treatment_plan(self):
        treatment_plan = TreatmentPlan(medical_record_id=self.id)
        treatment_plan.create()

        return treatment_plan
