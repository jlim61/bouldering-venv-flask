from flask import request

from app import app
from db import users

# get boulder
@app.get('/boulder')
def get_boudler():
    pass

# create boulder
@app.post('/boulder')
def create_boulder():
    pass

# edit boulder
@app.put('/boulder')
def update_boulder():
    pass

# delete boulder
@app.delete('/boulder')
def delete_boulder():
    pass

