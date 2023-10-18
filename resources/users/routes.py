from flask import request
from uuid import uuid4

from app import app
from db import users


# get all users
@app.get('/user')
def get_users():
    return {'users': users}, 200

# create a user
@app.post('/user')
def create_user():
    user_data = request.get_json()
    users[uuid4().hex] = user_data
    return users, 201

# edit a user
@app.put('/user/<user_id>')
def update_user(user_id):
    user_data = request.get_json()
    try:
        user = users[user_id]
        user['username'] = user_data['username']
        return user, 200
    except KeyError:
        return {'message': 'user not found'}, 400

# delete a user
@app.delete('/user')
def delete_user():
    user_data = request.get_json()
    for i, user in enumerate(users):
        if user['username'] == user_data['username']:
            users.pop(i)
    return {'message': f'{user_data["username"]} deleted'}, 202


# 