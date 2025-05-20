from .base import *

class CartTransforms(GraphQL):
    def list(self):
        return self.run(
            """
            query {
                cartTransforms(first:250) {
                    nodes {
                        functionId
                        id
                        blockOnFailure
                        metafield(key:"config",namespace:"srd") {
                            value
                        }    
                    }
                }
            }
            """
        )
    def get(self,id):
        try:
            return list(
                filter(
                    lambda x:x["id"]==f"gid://shopify/CartTransform/{id}",
                    self.list()["data"]["cartTransforms"]["nodes"]
                )
            )[-1]
        except:
            return {}
    def create(self,function,block=False):
        return self.run(
            """
                mutation cartTransformCreate($functionId: String!,$block:Boolean) {
                    cartTransformCreate(functionId: $functionId,blockOnFailure:$block) {
                        cartTransform {
                            functionId
                            id
                        }
                        userErrors {
                            field
                            message
                        }
                    }
                }
            """,
            {"functionId":function,"block":block}
        )
    def delete(self,id):
        return self.run(
            """
            mutation cartTransformDelete($id: ID!) {
                cartTransformDelete(id: $id) {
                    deletedId
                    userErrors {
                        field
                        message
                    }
                }
            }
            """,
            {"id":f"gid://shopify/CartTransform/{id}"}
        )