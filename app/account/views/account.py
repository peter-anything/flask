from flask import Blueprint, request
from app.account.models import User
from app import db
account_bp = Blueprint('account', __name__)


@account_bp.route('/queryone', methods=['POST', 'GET'])
def index():
    print('query one')
    user = User(username='peter')
    db.session.add(user)
    db.session.commit()
    return 'Hello, administrative user!'
