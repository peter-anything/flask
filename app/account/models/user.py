from app import db
from app.common import BaseModel


class User(BaseModel):
    __table__name = 'user'
    username = db.Column(db.String(64), index=True)
    sex = db.Column(db.Boolean, default=True)
    password = db.Column(db.String(128), default='')
    email = db.Column(db.String(128), default='')
    info = db.Column(db.String(64))
