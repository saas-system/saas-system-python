from flask import jsonify, g

from app.exception.error_code import DeleteSuccess
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.user import User

api = Redprint('user')


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def get_user(uid):
    user = User.query.filter_by(id=uid).first_or_404()
    return jsonify(user.to_dict())


@api.route('', methods=['DELETE'])
@auth.login_required
def delete_user():
    uid = g.user.uid   # 防止把别人删除，只删除自己的，g变量是线程隔离
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404()
        user.delete()
    return DeleteSuccess()


@api.route("", methods=['PUT'])
def update_user(uid):
    return 'update user'


@api.route('/create')
def create_user():
    return 'create user'
