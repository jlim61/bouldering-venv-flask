from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import abort
from sqlalchemy.exc import IntegrityError
from resources.moonboard_boulders.MoonboardBoulderModel import MoonboardBoulderModel
from resources.users.UserModel import UserModel

from schemas import AuthUserSchema, ProjectedBoulderSchema, UpdateUserSetterSchema, UserSchemaNested, UserSetterSchema

from . import bp
from .UserModel import UserBoulderProjects, UserModel
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
        user = None
        if user_id.isdigit():
            user = UserModel.query.get(user_id)
        if not user:
            user = UserModel.query.filter_by(username=user_id).first()
        if user:
            moonboards_info = []
            for element in user.projected:
                moonboard_info = {'attempts': element.attempts,
                                'completed': element.completed,
                                'boulder_id': element.boulder_id}
                element = element.moonboard_boulders
                boulder_info = {}
                boulder_info['boulder_name'] = element.boulder_name
                boulder_info['grade'] = element.grade
                boulder_info['id'] = element.id
                boulder_info['setter_id'] = element.setter_id
                moonboard_info['boulder_info'] = boulder_info
                moonboards_info.append(moonboard_info)
                user.moonboard_info = moonboards_info
            return user
        abort(400, message='Please enter valid username or id')



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

@bp.route('/user/project/<projected_id>')
class ProjectBoulder(MethodView):
    # Project a boulder
    @jwt_required()
    @bp.response(200, UserSetterSchema(many=True))
    def post(self, projected_id):
        projector_id = get_jwt_identity()
        user = UserModel.query.get(projector_id)
        boulder_to_project = MoonboardBoulderModel.query.get(projected_id)
        if user and boulder_to_project:
            user.add_project(boulder_to_project)
            return user.projected
        abort(400, message="Invalid Boulder Info")

    # stop projecting a boulder
    @jwt_required()
    def put(self, projected_id):
        user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)
        boulder_to_remove = UserBoulderProjects.query.get(projected_id)
        if user and user.id == boulder_to_remove.user_id:
            user.remove_project(boulder_to_remove)
            return {'message': f'Boulder removed from projects: {boulder_to_remove}'}, 202
        abort(400, message="Invalid Boulder Info")

@bp.route('/project/attempts/<projected_id>/<amount>')
class ProjectBoulderAttempts(MethodView):
    # adjust amount
    @jwt_required()
    @bp.response(200, ProjectedBoulderSchema)
    def put(self, projected_id, amount):
        user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)
        boulder_to_update = UserBoulderProjects.query.get(projected_id)
        if user and user.id == boulder_to_update.user_id:
            boulder_to_update.attempts = amount
            db.session.commit()
            return boulder_to_update
        else:
            abort(400, message="Invalid Boulder Info")

@bp.route('/project/completed/<projected_id>/<status>')
class ProjectBoulderCompleted(MethodView):
    # adjust completion status
    @jwt_required()
    @bp.response(200, ProjectedBoulderSchema)
    def put(self, projected_id, status):
        user_id = get_jwt_identity()
        user = UserModel.query.get(user_id)
        boulder_to_update = UserBoulderProjects.query.get(projected_id)
        if user and user.id == boulder_to_update.user_id:
            if status.lower() == 'true':
                boulder_to_update.completed = True
                db.session.commit()
            return boulder_to_update
        else:
            abort(400, message="Invalid Boulder Info")