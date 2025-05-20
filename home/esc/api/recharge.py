import requests

class RechargeREST:
	def __init__(self,key):
		self.api_key = key
	def headers(self):
		return {
			"X-Recharge-Version": "2021-11",
			"Content-Type": "application/json",
			"X-Recharge-Access-Token": self.api_key
		}
	def url(self,url): 
		return "https://api.rechargeapps.com/%s" % (url)
	def get(self,url):
		print(self.url(url))
		return requests.get(self.url(url),headers=self.headers()).json()
	def post(self,url,body={}):
		return requests.post(self.url(url),data=json.dumps(body),headers=self.headers()).json()
	def put(self,url,body={}):
		return requests.put(self.url(url),data=json.dumps(body),headers=self.headers()).json()
	def delete(self,url):
		return requests.delete(self.url(url),headers=self.headers()).status_code

class Webhooks(RechargeREST):
	def __init__(self, key):
		super().__init__(key)
	def list(self):
		pass
	def create(self,topic,url):
		pass
	def delete(self,id):
		pass

class Orders(RechargeREST):
    def get(self,id):
        pass