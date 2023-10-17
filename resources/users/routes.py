from flask import request

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
    user_data['boulders'] = []
    users.append(user_data)
    return users, 201

# edit a user
@app.put('/user')
def update_user():
    user_data = request.get_json()
    user = list(filter(lambda user: user["username"] == user_data["username"], users))[0]
    user['username'] = user_data['new username']
    return user, 200

# delete a user
@app.delete('/user')
def delete_user():
    user_data = request.get_json()
    for i, user in enumerate(users):
        if user['username'] == user_data['username']:
            users.pop(i)
    return {'message': f'{user_data["username"]} deleted'}, 202