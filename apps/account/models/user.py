from apps import db
from apps.common import BaseModel

import graphene
from graphene import relay
from graphene_sqlalchemy import SQLAlchemyObjectType, SQLAlchemyConnectionField


class User(BaseModel):
    __table__name = 'user'
    username = db.Column(db.String(64), index=True)
    mobile = db.Column(db.String(16), index=True)
    email = db.Column(db.String(128), index=True)
    nickname = db.Column(db.String(64))
    sex = db.Column(db.Boolean, default=True)
    password = db.Column(db.String(128), default='')


class UserObject(SQLAlchemyObjectType):
    class Meta:
        model = User
        interfaces = (graphene.relay.Node,)


class UserObjectConnection(relay.Connection):
    class Meta:
        node = UserObject


class UserObjectQuery(graphene.ObjectType):
    """ query your users
    """
    user = graphene.Field(UserObject, username=graphene.ID(), mobile=graphene.String(), email=graphene.String())
    users = graphene.List(graphene.NonNull(UserObject), required=True)
    users_connection = SQLAlchemyConnectionField(UserObject)  # Want this to be required!

    def resolve_user(self, info, **kwargs):
        user_query = UserObject.get_query(info)
        if kwargs.get('username'):
            users = user_query.filter(User.username.contains(kwargs.get('username')))

        return users

    def resolve_users(self, info):
        users_query = UserObject.get_query(info)
        users = users_query.filter(User.username.contains('Green Fruits')).all()

        return users


UserSchema = graphene.Schema(query=UserObjectQuery)
