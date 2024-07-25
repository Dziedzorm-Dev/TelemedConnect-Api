from core.database import db
from .base_model import BaseModel


class MedicalOfficerInformation(BaseModel):
    user_id = db.Column(db.String(20), db.ForeignKey('account.user_id', name='fk_medical_officer_id_doctor_id'), primary_key=True, nullable=False)
    speciality = db.Column(db.String(255), nullable=False)
    licence = db.Column(db.String(255), nullable=False)
    years_of_experience = db.Column(db.Integer, nullable=False)
    affiliation = db.Column(db.String(255), nullable=False)

    account = db.relationship(
        'Account', foreign_keys=[user_id], back_populates='professional_information'
    )

    @staticmethod
    def __name__():
        return "MedicalOfficerInformation"

    def __delete__(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def create(self):
        db.session.add(self)
        db.session.commit()

        return self
