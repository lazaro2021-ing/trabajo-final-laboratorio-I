from app.apis_key import *

bundles = {}

data={
     'coin':{'ETH':{'red':['BNB','BSC','ETH'],
                    'available':False,
                    'max_withdraw':0},
             'ETC':{'red':['BNB','BSC','ETH'],
                    'available':False,
                    'max_withdraw':0},
             'BNB':{'red':['BNB','BSC'],
                    'available':True,
                    'max_withdraw':0.02},
             'USDT':{'red':['BNB','BSC','ETH','TRX'],
                    'available':False,
                    'max_withdraw':0},
             'BTC':{'red':['BNB','BSC','ETH','BTC'],
                    'available':False,
                    'max_withdraw':0},
             },
      'red_url_tx':{"ETH":"https://etherscan.io/tx/",
                    "BNB":"https://bscscan.com/tx/",
                    "BTC":"",
                    "TRX":"https://tronscan.org/#/transaction/",
                    "ETC":"https://etc.tokenview.com/es/tx/"},    

      'ganancia':0.20,
      'noticias':"",

}

mongo_config={
    'user_name':'test',
    'password':'test12345',
    'cluster_name':'cluster0',
    'db_name':'crypto',
    'proyect_name':'laboratorio1',
}

