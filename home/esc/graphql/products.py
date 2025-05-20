from .base import *
       
class Products(GraphQL):
    def getByHandle(self,handle):
        data = self.run("""
            query getProductIdFromHandle($handle: String!) {
                productByHandle(handle: $handle) {
                id
            }
        }
        """,
        {"handle":handle}
        )
        return self.get(data.get("productByHandle",{}).get("id"))
    def get(self,id):
        return self.run(
        """
            query getProduct ($id:ID!) {
             product(id: "gid://shopify/Product/108828309") {
                title
                description
                onlineStoreUrl
            }
        }""",
        {
            "id":id
        }
        )
    def metafield(self,id,namespace,key):
        data =self.run("""
            query getProduct($id: ID!,$namespace:String,$key:String) {
                product(id:$id) {
                    id
                    title
                    handle
                    productType
                    metafield(namespace:$namespace,key:$key) {
                        value
                    }
                }
            }
        """,
        {
            "id":f"gid://shopify/Product/{id}",
            "namespace":namespace,
            "key":key
        })
        return data
class Metafields(GraphQL):
    def set(self,metafield):
        return self.run("""
        mutation MetafieldsSet($metafields: [MetafieldsSetInput!]!) {
            metafieldsSet(metafields: $metafields) {
                metafields {
                    key
                    namespace
                    value
                    createdAt
                    updatedAt
                }
                userErrors {
                    field
                    message
                    code
                }
            }
        }""",
        {
            "metafields":[
               metafield
            ]
        })