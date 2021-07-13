import mercadopago
import json

class MercadoPago:
    def __init__(self, acces_token):
        self.acces_token =acces_token
        
        self.sdk = mercadopago.SDK(acces_token)

    def set_urls(self,notification_url,back_urls):
        self.notification_url=notification_url
        self.back_urls=back_urls


    def create_pay(self,title,price,description,data_coin):
        
        
        preference_object = {
            "items": [
                {
                    "description": description,
                    "quantity": 1,
                    "title": title,
                    "currency_id": "ARS",
                    "unit_price": price,
                    "auto_return": "approved"
                }],
                "additional_info":json.dumps(data_coin),
                "notification_url": self.notification_url,
                "back_urls": {"success": self.back_urls},
        }

       
        self.payment_created  = self.sdk.preference().create(preference_object)
        
    def check_pay(self,mp_id):
        
        req=self.sdk.merchant_order().get(mp_id)
        if req['status']==200:
            response=req['response']
            if response[ 'order_status']=='paid':
                data_coin=json.loads(response['additional_info'])
                return {'status':True,'data_coin':data_coin,'pref_id':response['preference_id']}
        return {'status':False,'data_coin':'','pref_id':''}
                

    
   