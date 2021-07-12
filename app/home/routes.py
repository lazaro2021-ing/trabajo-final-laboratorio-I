from flask import Blueprint,session,request,render_template,render_template,redirect,url_for,flash,jsonify,make_response
from flask_assets import Environment, Bundle
from app.config import *


mod=Blueprint("home",__name__,static_folder="static",template_folder="templates",static_url_path="/%s" % __name__)


js = Bundle("home/js/home.js",output="gen/home_js.js")
bundles["home_js"]=js

css = Bundle("home/css/home.css",output="gen/home_css.css")
bundles["home_css"]=css

css = Bundle("home/css/menu.css",output="gen/menu_css.css")
bundles["menu_css"]=css



@mod.route('/', methods=['GET'])
@mod.route('/home', methods=['GET'])
def home(): 
    
    return render_template("home.html")