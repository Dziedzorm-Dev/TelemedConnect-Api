from core.database import db
from datetime import datetime
from core.utils.utils_ import generate_id


class Note(db.Model):
    id = db.Column(db.String(20), primary_key=True, default=generate_id)
    user_id = db.Column(db.String(20), nullable=False)
    target_id = db.Column(db.String(20), nullable=False)
    target_type = db.Column(db.String(20), nullable=False)
    note = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    anchor_id = db.Column(db.String(20), db.ForeignKey('note.id', name='fk_anchor_note'), nullable=True)

    @staticmethod
    def __name__():
        return "Note"

    def __delete__(self):
        db.session.delete(self)
        db.session.commit()

    def create(self):
        db.session.add(self)
        db.session.commit()

    def respond(self, message, user_id):
        response = Note(
            anchor_id=self.id,
            target_id=self.target_id,
            target_type=self.target_type,
            note=message,
            user_id=user_id,
        )

        response.create()

        return response
