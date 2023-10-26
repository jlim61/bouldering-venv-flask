from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import create_access_token

from schemas import AuthUserSchema, UserSetterSchema
from . import bp
from .UserModel import UserModel

# create user
@bp.post('/register')
@bp.arguments(UserSetterSchema)
@bp.response(201, UserSetterSchema)
def register_user(user_data):
    if UserModel.query.filter_by(username=user_data['username']).first() or UserModel.query.filter_by(email=user_data['email']).first():
        abort(400, message='Username or Email already taken')
    user = UserModel()
    user.from_dict(user_data)
    try:
        user.save()
        return user_data
    except IntegrityError:
        abort(400, message='Username or Email already taken')

# create setter
# @bp.post('/register_setter')
# @bp.arguments(UserSetterSchema)
# @bp.response(201, UserSetterSchema)
# def register_user(user_data):
#     if UserModel.query.filter_by(username=user_data['username']).first() or UserModel.query.filter_by(email=user_data['email']).first():
#         abort(400, message='Username or Email already taken')
#     user = UserModel()
#     user.from_dict(user_data)
#     try:
#         user.save()
#         return user_data
#     except IntegrityError:
#         abort(400, message='Username or Email already taken')

@bp.post('/login')
@bp.arguments(AuthUserSchema)
def login(login_info):
    if 'username' not in login_info:
        abort(400, message="Please include username.")
    user = UserModel.query.filter_by(username=login_info['username']).first()
    if user and user.check_password(login_info['password']):
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token,
                'setter': user.setter,
                'id': user.id}
    abort(400, message='Invalid Username or Password')

# @bp.routes('/logout')
# def logout():
#     pass