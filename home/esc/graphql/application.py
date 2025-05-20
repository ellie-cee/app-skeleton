from .base import * 

class Application(GraphQL):
    def scopes(self):
        return self.run(
            """
            query {
                currentAppInstallation {
                    accessScopes {
                        description
                        handle
                    }
                    app {
                        availableAccessScopes {
                            handle
                        }
                    }
                }
            }
            """
        )