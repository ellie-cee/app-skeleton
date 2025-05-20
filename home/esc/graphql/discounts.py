from .base import *
class Discounts(GraphQL):
    def listFunctions(self):
        ret = self.run(
            """
            query {
                appDiscountTypes {
                    targetType
                    functionId
                    title
                    appKey
                }
            }
            """
        )
        ret["data"]["addDiscountTypes"] = list(
            filter(
                lambda x: x["appKey"]==os.environ.get("SHOPIFY_API_KEY"),
                ret["data"]["appDiscountTypes"]
            )
        )
        logger.error(ret)
        return ret
    
    def listAppDiscounts(self):
        return self.run(
            """
            query {
                discountNodes(first:250,query:"type:app") {
                    nodes {
                        
                        id
                        discount {
                            __typename
                            ... on DiscountAutomaticApp {
                                title
                                appDiscountType {
                                    title
                                    functionId
                                    appKey
                                }
                            }
                            ... on DiscountCodeApp {
                                title
                                codes(first:1) {
                                    nodes {
                                        code
                                        id
                                    }
                                }
                                
                            }
                        }
                        metafield(namespace:"srd",key:"config") {
                            value
                        }  
                    }
                }
            }    
            """
        )
        
    def createAppDiscount(self,input):
        return self.run("""
        mutation discountAutomaticAppCreate($input: DiscountAutomaticAppInput!) {
            discountAutomaticAppCreate(automaticAppDiscount: $input) {
                userErrors {
                    field
                    message
                }
                automaticAppDiscount {
                    discountId
                    title
                    startsAt
                    endsAt
                    status
                    appDiscountType {
                        appKey
                        functionId
                    }
                    combinesWith {
                        orderDiscounts
                        productDiscounts
                        shippingDiscounts
                    }
                }
            }
        }""",
        input)
        
    def updateDiscount(self,id,payload):
        return self.run(
            """
            mutation discountAutomaticAppUpdate($automaticAppDiscount: DiscountAutomaticAppInput!, $id: ID!) {
                discountAutomaticAppUpdate(automaticAppDiscount: $automaticAppDiscount, id: $id) {
                    automaticAppDiscount {
                        discountId
                        title
                        startsAt
                        endsAt
                        status
                        appDiscountType {
                            appKey
                            functionId
                        }
                        combinesWith {
                            orderDiscounts
                            productDiscounts
                            shippingDiscounts
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
                "id":f"gid://shopify/DiscountAutomaticNode/{id}",
                "automaticAppDiscount":payload,
            }
        )
    def getDiscountFunction(self,id):
        return self.run("""
        query getDiscountNode($id:ID!) {
            discountNode(id:$id) {
                id
                discount {
                    ... on DiscountAutomaticApp {
                        title
                        startsAt
                        endsAt
                        appDiscountType {
                            title
                            functionId  
                        }
                        combinesWith {
                           orderDiscounts
                            productDiscounts
                            shippingDiscounts
                        }                                
                    }
                }
                metafield(namespace:"srd",key:"config") {
                    value
                }  
            }
        }
        """,
        {"id":f"gid://shopify/DiscountAutomaticNode/{id}"}
    )
    def deleteAppDiscount(self,id):
        return self.run("""
        mutation discountAutomaticDelete($id: ID!) {
            discountAutomaticDelete(id: $id) {
                deletedAutomaticDiscountId
                userErrors {
                    field
                    code
                    message
                }
            }
        }                
        """,
        {
            "id":f"gid://shopify/DiscountAutomaticNode/{id}"
        })
    
    def preview(self,request):
        payload = {}
        
    def listAppDiscountCodes(self):
        return self.run(
            """
            query {
                discountNodes(first:250,query:"type:app") {
                    nodes {
                        
                        id
                        discount {
                            ... on DiscountAutomaticApp {
                                title
                                appDiscountType {
                                    title
                                    functionId
                                    appKey
                                }
                            }
                            ...
                        }
                        metafield(namespace:"srd",key:"config") {
                            value
                        }  
                    }
                }
            }    
            """
        )
        
    def createAppDiscount(self,input):
        return self.run("""
        mutation discountAutomaticAppCreate($input: DiscountAutomaticAppInput!) {
            discountAutomaticAppCreate(automaticAppDiscount: $input) {
                userErrors {
                    field
                    message
                }
                automaticAppDiscount {
                    discountId
                    title
                    startsAt
                    endsAt
                    status
                    appDiscountType {
                        appKey
                        functionId
                    }
                    combinesWith {
                        orderDiscounts
                        productDiscounts
                        shippingDiscounts
                    }
                }
            }
        }""",
        input)
        
    def updateDiscount(self,id,payload):
        return self.run(
            """
            mutation discountAutomaticAppUpdate($automaticAppDiscount: DiscountAutomaticAppInput!, $id: ID!) {
                discountAutomaticAppUpdate(automaticAppDiscount: $automaticAppDiscount, id: $id) {
                    automaticAppDiscount {
                        discountId
                        title
                        startsAt
                        endsAt
                        status
                        appDiscountType {
                            appKey
                            functionId
                        }
                        combinesWith {
                            orderDiscounts
                            productDiscounts
                            shippingDiscounts
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
                "id":f"gid://shopify/DiscountAutomaticNode/{id}",
                "automaticAppDiscount":payload,
            }
        )
    def getDiscountFunction(self,id):
        return self.run("""
        query getDiscountNode($id:ID!) {
            discountNode(id:$id) {
                id
                discount {
                    ... on DiscountAutomaticApp {
                        title
                        startsAt
                        endsAt
                        appDiscountType {
                            title
                            functionId  
                        }
                        combinesWith {
                           orderDiscounts
                            productDiscounts
                            shippingDiscounts
                        }                                
                    }
                }
                metafield(namespace:"srd",key:"config") {
                    value
                }  
            }
        }
        """,
        {"id":f"gid://shopify/DiscountAutomaticNode/{id}"}
    )
    def deleteAppDiscount(self,id):
        return self.run("""
        mutation discountAutomaticDelete($id: ID!) {
            discountAutomaticDelete(id: $id) {
                deletedAutomaticDiscountId
                userErrors {
                    field
                    code
                    message
                }
            }
        }                
        """,
        {
            "id":f"gid://shopify/DiscountAutomaticNode/{id}"
        })