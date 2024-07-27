from flask import Flask

import redis

app = Flask(__name__)
r = redis.Redis(decode_responses=True)

from .routes import *