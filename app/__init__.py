from flask import Flask, request

app = Flask(__name__)

from resources.users import routes
from resources.boulders import routes