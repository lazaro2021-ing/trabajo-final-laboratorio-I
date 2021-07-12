from flask import Blueprint, session, request, render_template, render_template, redirect, url_for, flash, jsonify, make_response
from flask.wrappers import Response
from flask_assets import Environment, Bundle
from app.config import *
from app.apis.binance import Binance
from app.apis.mp import MercadoPago
from bs4 import BeautifulSoup
import requests
import json
from app import mongo
import time



mod = Blueprint("buy", __name__, static_folder="static",
                template_folder="templates", static_url_path="/%s" % __name__)


js = Bundle("buy/js/buy.js","buy/js/modal.js", output="gen/buy_js.js")
bundles["buy_js"] = js

css = Bundle("buy/css/buy.css", output="gen/buy_css.css")
bundles["buy_css"] = css

API_KEY = apis['binance']['API_KEY']
SECRET_KEY = apis['binance']['SECRET_KEY']

binance = Binance(API_KEY, SECRET_KEY)
binance.servers_status()


@mod.route('/', methods=['GET'])
def index():
    return render_template("buy.html", data=data)


@mod.route('/price_coin', methods=['GET'])
def get_price():

    data = request.args
    response = binance.get_price_by_symbol({'symbol': data['symbol']})

    return response


@mod.route('/get_info', methods=['GET'])
def get_info():
    
    #consulta precio del dolar
    page = requests.get("https://www.dolarsi.com/api/api.php?type=valoresprincipales")
    html = BeautifulSoup(page.text, 'html.parser')
    string = html.text
    dolar_price = json.loads(string)[1]['casa']['venta'].replace(',', '.')

    #consulta precio del dolar
    data_req = request.args

    #consulta el precio de la coin
    response1 = binance.get_price_by_symbol({'symbol': data_req['coin']+'USDT'})

    #consulta las redes para la coin
    response = binance.get_coin_red(data_req['coin'])
    red = response['red']
    #filtro solo devuelve los datos de la red del request
    red_info = [{'fees': item['withdrawFee'], 'withdrawMin':item['withdrawMin']}for item in red if item['network'] == data_req['network']][0]
    red_info['price'] = response1['price']
    red_info['dolar'] = dolar_price

    return red_info

@mod.route('/historial', methods=['GET'])
def get_historial():
    #consulta precio del dolar
    address = request.args['address']
    existing_user = mongo.db.address.find_one({"address": address})
    #print(existing_user)
    historial=[]
    if existing_user != None:
        historial=existing_user['historial']

    
    return {"historial":historial}


@mod.route('/pay', methods=['POST'])
def create_url_pay():
    #set mp variables
    print("entro pay",request.form)

    mp = MercadoPago(apis['mercadopago']['ACCESS_TOKEN'])
    mp.set_urls(apis['mercadopago']['notification_url'],apis['mercadopago']['back_urls'])
    
    # get datos del form
    coin = request.form.get('coin')
    red = request.form.get('red')
    address = request.form.get('address')
    amount_coin = request.form.get('amount_coin')
    amount_pesos = request.form.get('amount_pesos')
    data_coin = {'coin': coin, 'red': red,'address': address, 'cantidad': amount_coin,
                'pref_id':'','status':'pendiente','binance_id':''}

    #crea una orden de pago
    #mp.create_pay("COMPRAR "+coin, float(amount_pesos), "COMPRA:"+amount_coin+coin,data_coin)
    mp.create_pay("COMPRAR "+coin, 5.0, "COMPRA:"+amount_coin+coin, data_coin)

    # obtiene el pref id
    pref_id = mp.payment_created['response']['id']
    data_coin['pref_id']=pref_id

    #insert en la db el pref_id de la orden de pago y le pone como status false
    mongo.db.pref_id.insert_one({'pref_id': pref_id, 'status': False,'url_tx':'','address':address})

    #busca en la db la addres
    existing_user = mongo.db.address.find_one({"address": address})
    if existing_user == None:
        # si no esta la addres en la db la inserta y le agrega los datos de la transaccion
        mongo.db.address.insert_one({"address": address, "historial": []})
        mongo.db.address.find_one_and_update({"address": address}, {"$push": {'historial': data_coin}})
    else:
        # si no esta la address en la db solo agrega los datos de la transaccion
        mongo.db.address.find_one_and_update({"address": address}, {"$push": {'historial': data_coin}})

    #return redirect(mp.payment_created['response']['init_point'])
    return jsonify({'url_redirect':mp.payment_created['response']['init_point']})


@mod.route('/ipn', methods=['GET', 'POST'])
def notification():
    print('hola caroa')
    response_data = {"sucess": False,"status_code": 404}

    print('request key',request.args.keys())
    keys=list(request.args.keys())
    if 'id'in keys:
        mp_id = request.args['id']
        print(request.args['id'])
    if 'data.id'in keys:
        mp_id = request.args['data.id']
        print(request.args['data.id'])
    
    mp = MercadoPago(apis['mercadopago']['ACCESS_TOKEN'])
    status = mp.check_pay(mp_id)

    print(status)
    
    '''
    data_coin = {'coin': 'BNB', 'red': 'BSC','address': '0x91eC66Bd1fc66Ef25F1f0ec26B73B2d444D9D769', 'cantidad': 0.02,
                'pref_id':'114310878-d423e160-1d62-4183-844e-97f72150b6a9','status':'pendiente','binance_id':''}

    status={'status':True,'pref_id':'114310878-d423e160-1d62-4183-844e-97f72150b6a9','data_coin':data_coin}
    '''

    existing_id = mongo.db.pref_id.find_one({"pref_id": status['pref_id']})
    print('existing_id', existing_id)
    if existing_id != None:
        # es decir se acredito el pago y no se hizo la transf y si la coin esta habilitada
        if status['status'] == True and existing_id['status'] == False:

            if  data['coin'][status['data_coin']['coin']]['available']==True and float(status['data_coin']['cantidad'])<=data['coin'][status['data_coin']['coin']]['max_withdraw']:
                #cambiamos el estado de la db a true para evitar las doble transferencias
                mongo.db.pref_id.find_one_and_update({"pref_id": status['pref_id']}, {"$set": {'status': True}})
               
                '''
                # ejecuta la transferencia
                content = binance.withdraw({"coin": status['data_coin']['coin'],
                                            "address": status['data_coin']['address'],
                                            "amount": status['data_coin']['cantidad'],
                                            "network": status['data_coin']['red'],
                                            })
                '''
                content={'id':'1fc26329db91416cbe120194885c2f64'}
                if 'id' in content.keys():
                    address=mongo.db.address.find_one({"address": status['data_coin']['address']})
                    if address:
                        new_historial=address['historial']
                       
                        for k,tx in enumerate(address['historial']):
                           
                            if tx['pref_id']==status['pref_id']:
                                new_historial[k]['status']='exitosa'
                                new_historial[k]['binance_id']=content['id']
                                url_tx=data['red_url_tx'][status['data_coin']['coin']]+binance.find_binance_id(content["id"])
                                new_historial[k]['tx_id']=url_tx
                                mongo.db.pref_id.find_one_and_update({"pref_id": status['pref_id']}, {"$set": {'url_tx': url_tx}})
                                mongo.db.address.find_one_and_update({"address": status['data_coin']['address']}, {"$set": {'historial': new_historial}})
                                break
                        
                        
                response_data = {"sucess": True,"status_code": 200}

    return jsonify(response_data)


    

@mod.route('/success', methods=['GET', 'POST'])
def success():
    pref_id=request.args.get('preference_id')
    existing_id = mongo.db.pref_id.find_one({"pref_id": pref_id})
    if existing_id:
        url_tx=existing_id['url_tx']

    
    return redirect(url_tx)

