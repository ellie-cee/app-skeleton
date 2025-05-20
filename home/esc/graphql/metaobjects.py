from .base import *

class Metaobject(GraphQL):
    def get(self,type,handle):
        return self.run(
            """
            query getMetaObject($input:MetaobjectHandleInput!) {
                metaobjectByHandle(handle:$input) {
                    displayName
                    id
                    fields {
                        key
                        type
                        value
                        reference {
                            ... on ProductVariant {
                                id
                                title
                            }
                        }
                        references(first:20) {
                            nodes {
                                ... on ProductVariant {
                                    id
                                    title
                                }
                            }
                        }
                    }
                }
            }
            """,
            {"input":{"type":type,"handle":handle}}
            
        )