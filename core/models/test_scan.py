from core.database import db
from .base_model import BaseModel
from datetime import datetime
from core.utils.utils_ import generate_id


class TestScan(BaseModel):
    id = db.Column(db.String(20), primary_key=True, default=generate_id)
    medical_record_id = db.Column(db.String(20), db.ForeignKey('medical_record.id', name="fk_test_scan_medical_record_id"), nullable=False)
    technician_id = db.Column(db.String(20), db.ForeignKey('account.user_id', name='fk_test_scan_technician_id'), nullable=False)
    test_results = db.Column(db.String(255), nullable=False)
    test_date = db.Column(db.Date)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    test_results_url = db.Column(db.String(255))
    description = db.Column(db.String(255))

    medical_record = db.relationship(
        'MedicalRecord',
        foreign_keys=[medical_record_id],
        back_populates='test_scan'
    )

    @staticmethod
    def __name__():
        return "TestScan"

    def __delete__(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

