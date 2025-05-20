from .base import *

class Metafields(GraphQL):
    def set(self,metafields):
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
            "metafields":metafields
        })