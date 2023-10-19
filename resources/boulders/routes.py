from flask import request
from uuid import uuid4

from app import app
from db import boulders

# get boulder
@app.get('/boulder')
def get_boudler():
    return {'boulders': boulders}

# create boulder
@app.post('/boulder')
def create_boulder():
    boulder_data = request.get_json()
    boulders[uuid4().hex] = boulder_data
    return boulder_data, 201

# get a single boulder
@app.get('/boulder/<boulder_id>')
def get_boulder(boulder_id):
    try:
        boulder = boulders[boulder_id]
        return boulder, 200
    except KeyError:
        return {'message': 'boulder not found'}, 400

# edit boulder
@app.put('/boulder/<boulder_id>')
def update_boulder(boulder_id):
    boulder_data = request.get_json()
    try:
        boulder = boulders[boulder_id]
        boulder['grade'] = boulder_data['grade']
        return boulder, 200
    except KeyError:
        return {'message': 'Boulder not found'}, 400

# delete boulder
@app.delete('/boulder/<boulder_id>')
def delete_boulder(boulder_id):
    try:
        deleted_boulder = boulders.pop(boulder_id)
        return {'message': f'{deleted_boulder} deleted'}, 202
    except KeyError:
        return {'message': 'Boulder not found'}, 400

