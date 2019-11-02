from apps import db
from apps.common import BaseModel


class Event(BaseModel):
    __tablename__ = 'gitlab_event'
    project_id = db.Column(db.Integer)
    project_name = db.Column(db.String(32), index=True)
    push_data_ref = db.Column(db.String(32), default='')
    push_data_action = db.Column(db.String(32), index=True)
    gitlab_created_at = db.Column(db.TIMESTAMP, nullable=True)
    is_handled = db.Column(db.Boolean, default=True)
