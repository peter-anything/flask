from apps import db
from apps.common import BaseModel

import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField
from sqlalchemy import text


class Job(BaseModel):
    __tablename__ = 'jenkins_job'
    name = db.Column(db.String(8), index=True)
    pipeline_script = db.Column(db.Text)
    access_url = db.Column(db.String(128))
    synced = db.Column(db.Boolean, server_default=text('False'))
    build_parms = db.Column(db.JSON, nullable=False, default={})


class JobObject(SQLAlchemyObjectType):
    class Meta:
        model = Job
        interfaces = (graphene.relay.Node,)


class JobObjectQuery(graphene.ObjectType):
    """ query your jobs
    """
    job = graphene.Field(JobObject, username=graphene.ID(), mobile=graphene.String(), email=graphene.String())
    jobs = graphene.List(graphene.NonNull(JobObject), required=True)

    def resolve_job(self, info, **kwargs):
        user_query = JobObject.get_query(info)

        return []

    def resolve_jobs(self, info):

        return []


JobSchema = graphene.Schema(query=JobObjectQuery)
