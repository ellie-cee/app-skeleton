from .base import *

class DraftOrder(GraphQL):
    def create(self,input):
        return self.run(
            """
            mutation draftOrderCreate($input: DraftOrderInput!) {
                draftOrderCreate(input: $input) {
                    draftOrder {
                        id
                    }
                    userErrors {
                        field
                        message
                    }
                }
            }
            """,
            input
        )
    def closeDraft(self,id):
        return self.run(
            """
            mutation draftOrderComplete($id: ID!) {
                draftOrderComplete(id: $id) {
                    draftOrder {
                        id
                        order {
                            id
                            lineItems(first:100) {
                                nodes {
                                    id
                                    sku
                                }
                            }
                            fulfillmentOrders(first:50) {
                                nodes {
                                    id
                                    lineItems(first:100) {
                                        nodes {
                                            id
                                            title: variantTitle
                                            sku
                                            quantity: totalQuantity
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
            """,
            {
                "id":id
                    
            }
        )