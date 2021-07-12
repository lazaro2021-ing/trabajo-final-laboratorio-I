# -*- coding: utf-8 -*-
"""
Created on Sat Dec 19 03:04:28 2020

@author: lazar
"""
import sys
import ssl
import json
import requests
from datetime import datetime
import hmac
import hashlib
import urllib
from time import gmtime, strftime,sleep

class Binance:
    def __init__(self,api_key,secret_key):
        self.api_key=api_key
        self.secret_key=secret_key
        self.interval_enable=['1m','3m','5m','15m','30m',
                              '1h','2h','4h','6h','8h','8h','12h',
                              '1d','3d',
                              '1w',
                              '1M']
        
    def servers_status(self):
        
        self.servers_online=[]
        for k in ["",1,2,3]:
            try :
                url=f"https://api{k}.binance.com"
                server = requests.get(url)
                code=server.status_code
                
                if code==200:
                    print(f"Server {url} online")
                    self.servers_online.append(url)
                    
            except :
                print(f"Server {url} offline")
                
    def server_exchangeinfo(self):
        url = f'{self.servers_online[0]}/api/v3/exchangeInfo'  
        
        page = requests.get(url, headers={'X-MBX-APIKEY': self.api_key})
        info=json.loads(page.content)
        
        self.symbols=[symbol['symbol'] for symbol in info['symbols']]
        
                
    def get_server_timestamp(self):
        servertime = requests.get(self.servers_online[0]+"/api/v1/time")
        servertimeobject = json.loads(servertime.text)
        server_timestamp = servertimeobject['serverTime']
        return server_timestamp
    
    def signature(self,query):
        hashedsig = hmac.new(self.secret_key.encode('utf-8'), query.encode('utf-8'), hashlib.sha256).hexdigest()
        return hashedsig
    
    def jsonquery_to_str(self,query):
        query_str=""
        for key,value in query.items():
            query_str+=f"{key}={value}&"
            
        return query_str[:-1]
            
    
    def get_coin_data(self,symbols,interval):
        
        if not hasattr(self, 'symbols'):
            self.server_exchangeinfo()
        
        if interval in self.interval_enable:
            if symbols in self.symbols:
                query_string=f"symbol={symbols}&interval={interval}"
                url = f'{self.servers_online[0]}/api/v3/klines?{query_string}'  
                page = requests.get(url, headers={'X-MBX-APIKEY': self.api_key})
                content=json.loads(page.content)
                data_coin={'time':[],'open':[],'high':[],'low':[],'close':[],'volume':[]}
                
                for index,key in enumerate(data_coin.keys()):
                    data_coin[key]=[ resp[index] for resp in content]
                    
                return data_coin
                
            else:
                raise NameError(f"Symbol coin {symbols} is not available")    
            
        else:
             
            raise NameError(f"Interval {interval} is not available")
            
    # order={symbol,type(LIMIT, MARKET),side(BUY/SELL),price,quantity,timeInForce=(GTC)}
    def create_order(self,order):
        if not hasattr(self, 'symbols'):
            self.server_exchangeinfo()
            
        order['timestamp']=self.get_server_timestamp()
        
        if order['symbol'] in self.symbols:
            try:
                query_str=self.jsonquery_to_str(order)
                signature=self.signature(query_str)
                url = f'{self.servers_online[0]}/api/v3/order?{query_str}&signature={signature}'  
                page = requests.post(url, headers={'X-MBX-APIKEY': self.api_key})
                content=json.loads(page.content)
                return content
                
            except requests.ConnectionError:
                print("Error request")
                
        else:
            raise NameError(f"Symbol coin {order['symbol']} is not available")
           
    # order={symbol,orderId}
    def delete_order(self,order):
        if not hasattr(self, 'symbols'):
            self.server_exchangeinfo()
            
        order['timestamp']=self.get_server_timestamp()
        
        if order['symbol'] in self.symbols:
            try:
                query_str=self.jsonquery_to_str(order)
                signature=self.signature(query_str)
                url = f'{self.servers_online[0]}/api/v3/order?{query_str}&signature={signature}'  
                page = requests.delete(url, headers={'X-MBX-APIKEY': self.api_key})
                content=json.loads(page.content)
                print(content)
            except requests.ConnectionError:
                print("Error request")
                
        else:
            raise NameError(f"Symbol coin {order['symbol']} is not available")
            
    # order={symbol_filter}
    def get_order_by_symbol(self,order):
        order['timestamp']=self.get_server_timestamp()
        
        results=[]
        try:
            query_str=self.jsonquery_to_str(order)
            signature=self.signature(query_str)
            url = f'{self.servers_online[0]}/api/v3/openOrders?{query_str}&signature={signature}'  
            page = requests.get(url, headers={'X-MBX-APIKEY': self.api_key})
            content=json.loads(page.content)
            print(content)
            results=[result for result in content if result["symbol"]==order['symbol']]
            
        except requests.ConnectionError:
            print("Error request")
            
        return results
    
    
    #order={symbol_filter}
    def get_price_by_symbol(self,order):
        
        page = requests.get('https://api.binance.com/api/v3/ticker/price', headers={'X-MBX-APIKEY': self.api_key})
        try:
           
            url = f'{self.servers_online[0]}/api/v3/ticker/price'  
            page = requests.get(url, headers={'X-MBX-APIKEY': self.api_key})
            content=json.loads(page.content)
            results=[result for result in content if result["symbol"]==order['symbol']]
            
        except requests.ConnectionError:
            print("Error request")
            
        return results[0]     

    def get_coin_red(self,coin):
        order={}
        order['timestamp']=self.get_server_timestamp()
        
        #if order['symbol'] in self.symbols:
        try:
            query_str=self.jsonquery_to_str(order)
            signature=self.signature(query_str)
            url = f'{self.servers_online[0]}/sapi/v1/capital/config/getall?{query_str}&signature={signature}'  
            page = requests.get(url, headers={'X-MBX-APIKEY': self.api_key})
            content=json.loads(page.content)
            red_info=[item for item in content if item['coin']==coin][0]['networkList']

            return {'red':red_info}
            
        except requests.ConnectionError:
            print("Error request")
        

    
    def withdraw(self,order):
        order['timestamp']=self.get_server_timestamp()
        
        #if order['symbol'] in self.symbols:
        try:
            query_str=self.jsonquery_to_str(order)
            signature=self.signature(query_str)
            url = f'{self.servers_online[0]}/sapi/v1/capital/withdraw/apply?{query_str}&signature={signature}'  
            page = requests.post(url, headers={'X-MBX-APIKEY': self.api_key})
            content=json.loads(page.content)
            return content
            
        except requests.ConnectionError:
            print("Error request")
                
        #else:
        #    raise NameError(f"Symbol coin {order['symbol']} is not available")
        
    def find_binance_id(self,idd):
        order={}
        order['timestamp']=self.get_server_timestamp()
        try:
            query_str=self.jsonquery_to_str(order)
            signature=self.signature(query_str)
            url = f'{self.servers_online[0]}/sapi/v1/capital/withdraw/history?{query_str}&signature={signature}'  
            page = requests.get(url, headers={'X-MBX-APIKEY': self.api_key})
            content=json.loads(page.content)
            tx_info=[item for item in content if item['id']==idd][0]

            return tx_info['txId']
            
        except requests.ConnectionError:
            print("Error request")
        

