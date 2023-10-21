from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from resources.users.UserModel import UserModel

from schemas import AuthUserSchema, UpdateUserSetterSchema, UserSchemaNested, UserSetterSchema

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

    # delete a user
    @jwt_required()
    @bp.arguments(AuthUserSchema)
    def delete(self, user_data):
        user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)
        if user and user.username == user_data['username'] and user.check_password(user_data['password']):
            user.delete()
            return {'message':f'{user_data["username"]} deleted'}, 202
        abort(400, message='Username or Password Invalid')

    # Edit a user
    @jwt_required()
    @bp.arguments(UpdateUserSetterSchema)
    @bp.response(200, UpdateUserSetterSchema)
    def put(self, user_data):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id, description='User not found')
        if user and user.check_password(user_data['password']):
            try:
                user.from_dict(user_data)
                user.save()
                return user
            except IntegrityError:
                abort(400, message='Username or Email already taken.')


@bp.route('/user/<user_id>')
class User(MethodView):
    # get a single user
    @bp.response(200, UserSchemaNested)
    def get(self, user_id):
        return UserModel.query.get_or_404(user_id, description='User not found')



@bp.route('/user/follow/<followed_id>')
class FollowUser(MethodView):
    # follow a user
    @jwt_required()
    @bp.response(200, UserSetterSchema(many=True))
    def post(self, followed_id):
        follower_id = get_jwt_identity()
        user = UserModel.query.get(follower_id)
        user_to_follow = UserModel.query.get(followed_id)
        if user and user_to_follow:
            user.follow_user(user_to_follow)
            return user.followed.all()
        abort(400, message="Invalid User Info")

    # unfollow a user
    @jwt_required()
    def put(self, followed_id):
        follower_id = get_jwt_identity()
        user = UserModel.query.get(follower_id)
        user_to_unfollow = UserModel.query.get(followed_id)
        if user and user_to_unfollow:
            user.unfollow_user(user_to_unfollow)
            return {'message': f'Unfollowed user: {user_to_unfollow.username}'}, 202
        abort(400, message="Invalid User Info")