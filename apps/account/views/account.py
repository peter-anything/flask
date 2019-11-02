from apps.account.models import User, UserSchema
from apps.account.views import blue_print

from apps.common import JSONResponse

from flask import request
from flask_graphql import GraphQLView
from werkzeug.security import generate_password_hash, \
    check_password_hash


@blue_print.route('/login', methods=['POST'])
def login():
    params = request.get_json()
    email = params['email']
    password = params['password']
    user = User.query.filter_by(email=email).first()
    if check_password_hash(user.password, password):
        return JSONResponse.success()
    else:
        return JSONResponse.error('username or password is error!')


@blue_print.route('/register', methods=['POST'])
def register():
    params = request.get_json()
    mobile = params.get('mobile')
    email = params.get('email')
    nickname = params.get('nickname')
    sex = params.get('sex')
    password = params.get('password')

    if not (email and password):

        return JSONResponse.error('email and password must be provided')
    else:
        user = User.query.filter_by(email=email).first()
        if user:
            return JSONResponse.error('username has already registered!')

        user = User(
                    mobile=mobile,
                    email=email,
                    nickname=nickname,
                    sex=sex,
                    password=generate_password_hash(password)
                    )
        user.save()

        return JSONResponse.success()


# blue_print.add_url_rule(
#     '/graphql',
#     view_func=GraphQLView.as_view(
#         'graphql',
#         schema=UserSchema,
#         graphiql=False  # for having the GraphiQL interface
#     )
# )

