from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config
from flask_pymongo import PyMongo,MongoClient
from flask_admin import Admin

server = Flask(__name__, instance_relative_config = True)

Bootstrap(server)


server.config.from_object(Config)
server.config.from_pyfile('config.py')

MONGO_URI = server.config["MONGO_URI"]



admin = Admin(server)

mongo = PyMongo(server)

client =  MongoClient(MONGO_URI)



db = client["mongodb"]
from . import views
