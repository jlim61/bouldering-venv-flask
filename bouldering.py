from flask import Flask, request

app = Flask(__name__)

@app.route('/index')
@app.route('/')
def index():
    return 'Bouldering Capstone'

users = [
    {'username':'jlim',
    'email':'jlim@email.com',
    'boulders': [{'Location':'Movement Fountain Valley',
    'grade':'V4',
    'setter': 'Matteo',
    'completed': True,
    'attempts': 2}]},
    {'username':'hlim',
    'email':'hlim@email.com',
    'boulders': [{'Location':'Movement Fountain Valley',
    'grade':'V4',
    'setter': 'Matteo',
    'completed': True,
    'attempts': 2}]},
    {'username':'rlim',
    'email':'rlim@email.com',
    'boulders': [{'Location':'Movement Fountain Valley',
    'grade':'V4',
    'setter': 'Matteo',
    'completed': True,
    'attempts': 2}]}
]


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
    pass


# time in video: w6d1 PM lecture