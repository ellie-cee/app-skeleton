from .base import *

class Customers(GraphQL):
    def setTaxFree(self,id):
        return self.run(
            """
        mutation customerUpdate($input: CustomerInput!) {
            customerUpdate(input: $input) {
                userErrors {
                    field
                    message
                }
                customer {
                    id
                    email
                    firstName
                    lastName
                    taxExempt
                }
            }
        }
        """,
        {
            "input":{
                "id":id,
                "taxExempt":True
            }
        })
    def companyFromCustomer(self,id):
        return json.loads(shopify.GraphQL().execute(
        """
        query customer($id:ID!) {
            customer(id:$id) {
                companyContactProfiles {
                        company {
                            id
                            externalId
                            contactCount {
                                count
                            }
                            locationCount {
                                count
                            }
                            locations(first:20) {
                                nodes {
                                    id
                                    shippingAddress {
                                        province
                                        zoneCode
                                    }
                                    taxExemptions    
                                }  
                            }
                        }    
                    
                }       
            }
        }
        """,
        {"id":id}
    ))
    
    def getCustomerSubscriptionsCount(self,customerId):
        ret =  self.run(
            """
            query getCustomer($id:ID!) {
                customer(id:$id) {
                    id
                    subscriptions: storeSubscriptionContracts(first:5) {
                        nodes {
                            id
                        }
                    }
                }
            }
            """,
            {"id":customerId}
        )
        return len(ret.nodes("data.customer.subscriptions"))
    
    def getCustomerIdFromEmail(self,email):
        customers = self.run(
            """
            query getCustomers($query:String) {
                customers(first:1,query:$query) {
                    nodes {
                        id
                        email    
                    }
                }
            }
            """,
            {"query":f'email:{email}'}
        )
        for customer in customers.nodes("data.customers.nodes"):
            if customer.get("email")==email:
                return customer.get("id")
        return None
    