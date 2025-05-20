from .base import *

class Webhooks(GraphQL):
    def list(self):
        return self.run(
            """
            query {
              webhookSubscriptions(first: 250) {
                nodes {
                    id
                    topic
                    endpoint {
                        __typename
                        ... on WebhookHttpEndpoint {
                            callbackUrl
                        }
                    }
                }
            }
        }
            """
        )
    def get(self,id):
        return self.run(
            """
            query getWebhook($id:ID!) {
                webhookSubscription(id: $id) {
                    id
                    topic
                    endpoint {
                        __typename
                        ... on WebhookHttpEndpoint {
                            callbackUrl
                        }
                    }
                }
            }
            """,
            {"id":f"gid://shopify/WebhookSubscription/{id}"}
        )
    def create(self,topic,url):
        return self.run(
            """
                mutation webhookSubscriptionCreate($topic: WebhookSubscriptionTopic!, $webhookSubscription: WebhookSubscriptionInput!) {
                    webhookSubscriptionCreate(topic: $topic, webhookSubscription: $webhookSubscription) {
                        webhookSubscription {
                            id
                            topic
                            format
                            endpoint {
                                __typename
                                ... on WebhookHttpEndpoint {
                                    callbackUrl
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
                "topic":topic,
                "webhookSubscription": {
                    "callbackUrl": url,
                    "format": "JSON"
                }
            }
        )
    def update(self,id,url):
        return self.run(
            """
                mutation webhookSubscriptionUpdate($id: ID!, $webhookSubscription: WebhookSubscriptionInput!) {
                    webhookSubscriptionUpdate(id: $id, webhookSubscription: $webhookSubscription) {
                        userErrors {
                            field
                            message
                        }
                        webhookSubscription {
                            id
                            topic
                            endpoint {
                                ... on WebhookHttpEndpoint {
                                    callbackUrl
                                }
                            }
                        }
                    }
                }
            """,
            {
                "id": f"gid://shopify/WebhookSubscription/{id}",
                "webhookSubscription": {
                    "callbackUrl": url
                }
            }   
        )
    def delete(self,id):
        return self.run(
            """
            mutation webhookSubscriptionDelete($id: ID!) {
                webhookSubscriptionDelete(id: $id) {
                    userErrors {
                      field
                      message
                    }
                    deletedWebhookSubscriptionId
                }
            }
            """,
            {"id":f"gid://shopify/WebhookSubscription/{id}"}
        )