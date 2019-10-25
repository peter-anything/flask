from app import db


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)
    created_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())
    updated_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(),
                             server_onupdate=db.func.current_timestamp())
