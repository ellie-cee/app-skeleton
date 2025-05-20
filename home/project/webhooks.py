from ..esc.webhooks import WebhookBase, RechargeWebhooks
from ..esc.flows import FlowBase
from ..esc.graphql import Orders,Customers,Metaobject
from jmespath import search as jpath

class FirstSubscriptionGift(WebhookBase):
        
    def getConfiguration(self):
        ret = Metaobject().get(
            "",
            "free-gift-first-subscription"
        )
        return 
        
    def process(self):
        payload = self.payload()
        self.logJson(payload)
        return self.response({"messafe":"dewqdewdeW"})
        customerId = payload.get("admin_graphql_api_customer_id")
        orderid = "admin_graphql_api_origin_order_id"
        subscriptionsCount = Customers().getCustomerSubscriptionsCount(customerId)
        if len(subscriptionsCount)>1:
            return self.response({"msg":"Customer has subscriptions"})
        
        orders = Orders()
        order = orders.get()
        
        
        if "data" not in ret:
            return self.response({"msg":"unable to process"})
        elif ret["data"]["orderEditBegin"]["calculatedOrder"] is None:
            return self.response({"msg":"unable to process"})
      
        order_edit_id = jpath("data.orderEditBegin.calculatedOrder.id",ret)
        
        for bundle in bundles:
            for component in bundle:
                self.log(f"Adding Bundle Item {component.get('id')}")
                added = orders.orderEditAdd(order_edit_id,component.get("id"),component.get("quantity"))            
                try:
                    component["lineItemId"] = jpath("data.orderEditAddVariant.calculatedLineItem.id",added)
                    discounted = orders.orderItemDiscount(order_edit_id,component.get("lineItemId"))
                 
                except Exception as e:  
                    self.logJson(ret)
                    self.log("FAILED")
                    return self.response({"msg":"unable to process"})
            
        orders.addNote(payload,"Added Bundle Items")
        ret = orders.orderEditCommit(order_edit_id)
        self.updateWebhookStatus("processed")
            