from .base import *
class Functions(GraphQL):
    def list(self):
        return self.run(
        """
        query {
            shopifyFunctions(first: 25) {
                nodes {
                    app {
                        title
                    }
                    apiType
                    title
                    id
                }
            }
        }
        """)
    def find(self,type):
        types = type.split(",")
        return {
            "data":{
                "shopifyFunctions":{
                    "nodes":list(
                        filter(lambda x: x.get("apiType") in types,self.list().search("data.shopifyFunctions.nodes",[])
                        )
                    )
                }
            }
        }