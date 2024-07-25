from core.database import db
from core.models.note import Note


class BaseModel(db.Model):
    __abstract__ = True

    def __delete__(self):
        db.session.delete(self)
        return db.session.commit()

    def create(self):
        db.session.add(self)
        return db.session.commit()

    def update(self, updates=None):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def add_notes(self, user_id, message):
        note = Note(note=message, user_id=user_id, target_id=self.id, target_type=self.__name__())
        return note.create()

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}
