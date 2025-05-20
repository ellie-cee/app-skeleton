import json
from .common import SearchableDict
from logging import Logger
from django.http import HttpResponse
import shopify
from django.http import HttpRequest
from ..models import ShopifySite
import os

logger = Logger(__name__)

class Operation:
    def __init__(self,request:HttpRequest,**kwargs):
        self.request = request
        self.shopify_store = os.environ.get("SHOPIFY_DOMAIN")
        self.shopfiy_details = ShopifySite.objects.get(shopify_site=self.shopify_store)
        
        session = shopify.Session(f"{self.shopify_store}/admin",os.environ.get("SHOPIFY_API_VERSION"),self.shopfiy_details.access_token)
        shopify.ShopifyResource.activate_session(session)
        self.args = SearchableDict({})
        for key,value in kwargs.items():
            self.args.set(key,value)
            
    def arg(self,key,default=None):
        
        return self.args.get(key,default)
        
    def json(self):
        try:
            return json.loads(self.request.body.decode("utf-8"))
        except Exception as e:
            logger.error(e)
            return None
    def payload(self):
        return self.json()
    def logJson(self,data):
        logger.error(json.dumps(data))    
    def searchablePayload(self):
        json = self.json()
        if json is None:
            json = {}
        return SearchableDict(json)
    def error(self,error,status:500):
        return HttpResponse(json.dumps({"msg":error}),content_type="application/json",status=status)
    def retry(self):
        return HttpResponse(json.dumps({"msg":"Unable to fulfill request. Please try again later."}),content_type="application/json",status=418)
    def response(self,payload):
        logger.error(payload)
        return HttpResponse(json.dumps(payload),content_type="application/json",status=200)    
    def file(self,name):
        return self.request.FILES.get(name)
    def log(self,message):
        logger.error(message)
    def process(self):
        pass 
    def run(self):
        try:
            ret = self.process()
            print(ret)
            if isinstance(ret,HttpResponse) and ret is not None:
                return ret
            else:
                return self.response({"msg":"processed"})
        except:
            return self.error("unable to process")
    
