from .base import *

class Orders(GraphQL):
    
    def orderEditBegin(self,id):
        return self.run(
            """
                mutation orderEditBegin($id: ID!) {
                    orderEditBegin(id: $id) {
                        calculatedOrder {
                            id
                        }
                        userErrors {
                        field
                        message
                        }
                    }
                }
            """,
            {"id":id}
        )
    def orderEditClose(self,id,staffNote="Added Bundle Items"):
        return self.run(
            """
            mutation orderEditCommit($id: ID!,$staffNote:String) {
                orderEditCommit(id: $id,staffNote:$staffNote) {
                    order {
                        id
                        currentSubtotalPriceSet {
                            presentmentMoney {
                                amount
                            }
                            shopMoney {
                                amount
                            }
                        }
                        
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }
            """,
            {
                "id":id,
                "notifyCustomer": False,
                "staffNote": staffNote
            }
        )
    def orderEditAdd(self,id,variant,quantity):
        return self.run(
            """
            mutation orderEditAddVariant($id: ID!, $quantity: Int!, $variantId: ID!) {
                orderEditAddVariant(id: $id, quantity: $quantity, variantId: $variantId) {
                    calculatedLineItem {
                        id
                    }
                    userErrors {
                    field
                    message
                    }
                }
            }
            """,
            {
                "allowDuplicates": True,
                "id": id,
                "quantity": quantity,
                "variantId": variant
            }
            
        )
    def orderEditAddCustom(self,calculatedOrderId,customItem):
        return self.run(
            """
            mutation orderEditAddCustomItem($id: ID!, $price: MoneyInput!, $quantity: Int!, $requiresShipping: Boolean, $taxable: Boolean, $title: String!) {
                orderEditAddCustomItem(id: $id, price: $price, quantity: $quantity, requiresShipping: $requiresShipping, taxable: $taxable, title: $title) {
                    calculatedLineItem {
                        id
                    }
                    calculatedOrder {
                        id
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }        
            """,
            {
                "id":calculatedOrderId,
                "price":{
                    "amount":customItem.get("price"),
                    "currencyCode":"USD"
                },
                "quantity":customItem.get("quantity"),
                "requiresShipping":False,
                "taxable":False,
                "title":customItem.get("title")
            }
        )
    def orderItemDiscount(self,id,line_item,percentValue=100,description="Bundle Discount"):
        return self.run(
            """
            mutation orderEditAddLineItemDiscount($discount: OrderEditAppliedDiscountInput!, $id: ID!, $lineItemId: ID!) {
                orderEditAddLineItemDiscount(discount: $discount, id: $id, lineItemId: $lineItemId) {
                    addedDiscountStagedChange {
                        id
                    }
                    calculatedLineItem {
                        id
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }""",
            {
                "discount": {
                    "description": description,
                    "percentValue": percentValue
                },
                "id": id,
                "lineItemId": line_item
            }
        )
    def addNote(self,payload,note):
        return requests.put(
            f"https://{os.getenv('SHOPIFY_SITE')}.myshopify.com/admin/api/2024-04/orders/{payload.get('id')}.json",
            json={"order":{"id":payload.get(id),"note":f"{payload.get('note','')}\n{note}"}},
            headers={
                "Content-type":"application/json",
                "X-Shopify-Access-Token":os.getenv("SHOPIFY_TOKEN")
            }
        ).json()
    def update(self,input):
        return self.run(
            """
            mutation updateOrderMetafields($input: OrderInput!) {
                orderUpdate(input: $input) {
                    order {
                        id
                    }
                    userErrors {
                        message
                        field
                    }
                }
            }
            """,
           input
        )