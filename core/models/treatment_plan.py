from core.database import db
from datetime import datetime
from .base_model import BaseModel
from core.models.medication_prescription import MedicationPrescription
from core.utils.utils_ import generate_id


class TreatmentPlan(BaseModel):
    id = db.Column(db.String(20), primary_key=True, default=generate_id)
    medical_record_id = db.Column(db.String(20), db.ForeignKey('medical_record.id', name='fk_treatment_plan_medical_record_id'), nullable=False)
    plan_details = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    medical_record = db.relationship(
        'MedicalRecord',
        foreign_keys=[medical_record_id],
        back_populates='treatment_plan'
    )

    prescriptions = db.relationship(
        'MedicationPrescription',
        foreign_keys='MedicationPrescription.treatment_plan_id',
        back_populates='treatment_plan'
    )

    @staticmethod
    def __name__():
        return "TreatmentPlan"

    def add_prescription(self):
        prescription = MedicationPrescription(treatment_plan_id=self.id)
        prescription.create()

        return prescription
