from flask import Blueprint,session,request,render_template,render_template,redirect,url_for,flash,jsonify,make_response
from flask_assets import Environment, Bundle
from app.config import *
from bs4 import BeautifulSoup
import requests


mod=Blueprint("notice",__name__,static_folder="static",template_folder="templates",static_url_path="/%s" % __name__)


js = Bundle("notice/js/notice.js",output="gen/notice_js.js")
bundles["notice_js"]=js


css = Bundle("notice/css/notice.css",output="gen/notice_css.css")
bundles["notice_css"]=css


@mod.route('/', methods=['GET'])
def index(): 

    page=requests.get("https://www.criptonoticias.com/")
    
    html  = BeautifulSoup(page.text, 'html.parser')
    article=html.find_all('h3',class_="jeg_post_title")

    article_dict=[]
    for k in range(0,4):
        href=article[k].find('a')['href']
        title=article[k].find('a').text
        article_dict.append({'href':href,'title':title})

    data['noticias']=article_dict
    
    return render_template("notice.html",data=data)