from flask import request
from flask.views import MethodView
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from resources.setters.SetterModel import SetterModel

from schemas import AuthUserSchema, UpdateUserSetterSchema, UserSetterSchema

from . import bp
from .UserModel import UserModel
from app import db
from db import users



@bp.route('/user')
class UserList(MethodView):
    # get all users
    @bp.response(200, UserSetterSchema(many=True))
    def get(self):
        return UserModel.query.all()


    # create user
    @bp.arguments(UserSetterSchema)
    @bp.response(201, UserSetterSchema)
    def post(self, user_data):
        if SetterModel.query.filter_by(username=user_data['username']).first() or SetterModel.query.filter_by(email=user_data['email']).first():
            abort(400, message='Username or Email already taken')
        user = UserModel()
        user.from_dict(user_data)
        try:
            user.save()
            return user_data
        except IntegrityError:
            abort(400, message='Username or Email already taken')

    # delete a user
    # @bp.arguments(AuthUserSetterSchema)
    def delete(self):
        user_data = request.get_json()
        user = UserModel.query.filter_by(username=user_data['username']).first()
        if user and user.username == user_data['username'] and user.check_password(user_data['password']):
            user.delete()
            return {'message':f'{user_data["username"]} deleted'}, 202
        abort(400, message='Username or Password Invalid')


@bp.route('/user/<user_id>')
class User(MethodView):
    # get a single user
    @bp.response(200, UserSetterSchema)
    def get(self, user_id):
        return UserModel.query.get_or_404(user_id, description='User not found')

    # Edit a user
    @bp.arguments(UpdateUserSetterSchema)
    @bp.response(200, UpdateUserSetterSchema)
    def put(self, user_data, user_id):
        user = UserModel.query.get_or_404(user_id, description='User not found')
        if user and user.check_password(user_data['password']):
            try:
                user.from_dict(user_data)
                user.save()
                return user
            except IntegrityError:
                abort(400, message='Username or Email already taken.')

@bp.route('/user/follow/<follower_id>/<followed_id>')
class FollowUser(MethodView):
    # follow a user
    @bp.response(200, UserSetterSchema(many=True))
    def post(self, follower_id, followed_id):
        user = UserModel.query.get(follower_id)
        user_to_follow = UserModel.query.get(followed_id)
        if user and user_to_follow:
            user.follow_user(user_to_follow)
            return user.followed.all()
        abort(400, message="Invalid User Info")

    # unfollow a user
    @bp.response(202, UserSetterSchema(many=True))
    def put(self, follower_id, followed_id):
        user = UserModel.query.get(follower_id)
        user_to_unfollow = UserModel.query.get(followed_id)
        if user and user_to_unfollow:
            user.unfollow_user(user_to_unfollow)
            return {'message': f'Unfollowed user: {user_to_unfollow.username}'}
        abort(400, message="Invalid User Info")