import json
import shopify
from django.http import HttpResponse
import logging
import os
from ..models import ShopifySite
from ..models import ShopifyWebhook
from jmespath import search as jpath
from .graphql_common import Orders
from .common import SearchableDict
from .operations import Operation

logger = logging.getLogger(__name__)

class WebhookBase(Operation):
    def __init__(self, request):
        super().__init__(request)
        self.operations = []
        
    def addOperation(self,operationName,status,message,errors=[]):
        self.operations.append({
            "operation":operationName,
            "status":status,
            "message":message,
            "errors":errors
            }
        )
    def operationsResponse(self):
        return HttpResponse(json.dumps({"operations":self.operations}),content_type="application/json",status=200)
    def startWebhook(self):
        self.log("starting")
        eventId = self.request.headers.get("X-Shopify-Event-Id")
        details,created =  ShopifyWebhook.objects.get_or_create(webhook_id=eventId)
        if created:
            details.webhook_status = "created"
            if os.environ.get("PRESERVE_WEBHOOK_PAYLOADS","no")=="yes":
                details.webhook_payload = json.dumps(self.json())
                
            details.save()
        self.webhookDetails = details
        self.webhookDetails.save()
    def getWebhookStatus(self):
        return self.webhookDetails.webhook_status
    def updateWebhookStatus(self,status):
        self.webhookDetails.webhook_status = status
        self.webhookDetails.save()
    def run(self):
        self.startWebhook()
        
        status =  self.getWebhookStatus()
        
        match status:
            case "processing":
                return self.response({"msg":"processing"})
            case "processed":
                return self.response({"msg":"already processed"})
        
        self.updateWebhookStatus("processing")
        try:
            ret = self.process()
            self.updateWebhookStatus("processed")
            if len(self.operations)<1:
                if isinstance(ret,HttpResponse) and ret is not None:
                    return ret
                else:
                    return self.response({"msg":"processed"})
            else:
                return self.operationsResponse()
        except:
            self.updateWebhookStatus("retry")
            return self.error("unable to process")
        
        
    
class Shopify():
    def install(self,shopify,topic,path):
        hook = shopify.Webhook.create(
            {
                'topic':topic,
                'address':f"{os.getenv('APP_URL')}{path}"
            }
        )
        hook.save()
    def uninstall(self,shopify,path):
        for hook in shopify.Webhook.find():
            if (path in hook.address):
                hook.destroy()
    
    def list(self,shopify):
        ret = []
        for hook in shopify.Webhook.find():
            ret.append(hook.to_dict()) 
        return ret

class RechargeWebhooks:
    def __init__(self,request):
        self.request = request
        self.recharge = Recharge(os.environ.get("RECHARGE_TOKEN"))
        
    def error(self,error,status:500):
        return HttpResponse(json.dumps({"msg":error}),content_type="application/json",status=status)
    def retry(self):
        return HttpResponse(json.dumps({"msg":"Unable to fulfill request. Please try again later."}),content_type="application/json",status=418)
    def response(self,payload):
        logger.error(payload)
        return HttpResponse(json.dumps(payload),content_type="application/json",status=200)
    def json(self):
        try:
            return json.loads(self.request.body.decode("utf-8"))
        except Exception as e:
            logger.error(e)
            return None
        
    def install(self,topic,path):
        hook = self.recharge.post(
            "webhooks",
            {
                'topic':topic,
                'address':f"{os.getenv('APP_URL')}{path}"
            }
        )
    def uninstall(self):
        for hook in self.list():
            self.recharge.delete(f"webhooks/{hook.get('id')}")
            
        return []
    def list(self):
        ret = []
        for hook in self.recharge.get("webhooks").get("webhooks",[]):
            ret.append(hook) 
        return ret