import requests
from .common import *

class RestBase:
    def __init__(self,**kwArgs):
        pass
     
    def headers(self):
        return {}
		
    def url(self,url): 
        return "https://api.rechargeapps.com/%s" % (url)
    def process(self,response):
        if isinstance(response,dict):
            return SearchableDict(response)
        elif isinstance(response,list):
            return [SearchableDict(x) for x in response]
        else:
            return response
    def get(self,url):
        print(self.url(url))
        return self.process(
            requests.get(self.url(url),headers=self.headers()).json()
        )
    def post(self,url,body={}):
        return self.process(
            requests.post(self.url(url),data=json.dumps(body),headers=self.headers()).json()
        )
    def put(self,url,body={}):
        return self.process(
            requests.put(self.url(url),data=json.dumps(body),headers=self.headers()).json()
        )
    def delete(self,url):
        return requests.delete(self.url(url),headers=self.headers()).status_code