from apps import db
import enum


class Status(enum.Enum):
    VALID = 0
    DELETED = 9


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                             server_onupdate=db.func.current_timestamp())
    status = db.Column(db.Enum(Status), default=Status.VALID)

    def save(self):
        db.session.add(self)
        db.session.commit()
