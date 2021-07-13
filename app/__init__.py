# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 23:44:15 2020

@author: lzr
"""

from flask import Flask,render_template,request,redirect,url_for,jsonify,make_response,Response,session,flash
import os
from flask_assets import Environment, Bundle
from app.config import *
from flask_pymongo import PyMongo

flask_app = Flask(__name__, static_url_path='/static')
flask_app.config['SECRET_KEY'] = '15da6d4asd21a3d1a6s41da1das31da3s2d1a3s2d1a65s1d3a2sd'  
flask_app.config['MONGO_URI']=f"mongodb+srv://{mongo_config['user_name']}:{mongo_config['password']}@{mongo_config['cluster_name']}.pwm5a.mongodb.net/{mongo_config['db_name']}?retryWrites=true&w=majority"
flask_app.config['MONGO_DBNAME']=f"{mongo_config['proyect_name']}"

mongo=PyMongo(flask_app)


from app.buy.routes import mod
from app.home.routes import mod
from app.notice.routes import mod



flask_app.register_blueprint(buy.routes.mod,url_prefix='/buy')
flask_app.register_blueprint(home.routes.mod)
flask_app.register_blueprint(notice.routes.mod,url_prefix='/notice')

assets = Environment(flask_app)
assets.init_app(flask_app)
assets.register(bundles)
