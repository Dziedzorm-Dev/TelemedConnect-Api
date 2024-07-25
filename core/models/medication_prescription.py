from core.database import db
from .base_model import BaseModel
from datetime import datetime
from core.utils.utils_ import generate_id


class MedicationPrescription(BaseModel):
    id = db.Column(db.String(20), primary_key=True, default=generate_id)
    treatment_plan_id = db.Column(db.String(20), db.ForeignKey('treatment_plan.id', name='fk_medication_prescription_treatment_plan_id'), nullable=False)
    dispensing_officer_id = db.Column(db.String(20), db.ForeignKey('account.user_id', name='fk_medication_prescription_dispensing_officer_id'), nullable=False)
    prescription_details = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    dispensing_date = db.Column(db.DateTime)
    dispensing_url = db.Column(db.String(255))
    prescription_url = db.Column(db.String(255))
    is_dispensed = db.Column(db.Boolean, default=False)

    treatment_plan = db.relationship(
        'TreatmentPlan',
        foreign_keys=[treatment_plan_id],
        back_populates='prescriptions'
    )

    @staticmethod
    def __name__():
        return "MedicationPrescription"

    def __delete__(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
