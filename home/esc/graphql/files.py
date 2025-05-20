from .base import GraphQL

class Files(GraphQL):
    def create(self,url,fileName,altText):
        return self.run(
            """
            mutation fileCreate($files: [FileCreateInput!]!) {
                fileCreate(files: $files) {
                    files {
                        id
                        fileStatus
                        alt
                        createdAt
                    }
                    userErrors {
                        code
                        field
                        message
                    }
                }
            }
            """,
            {
                "files":[
                    {
                        "originalSource":url,
                        "filename":fileName,
                        "alt":altText
                    }
                ]
            }
        )