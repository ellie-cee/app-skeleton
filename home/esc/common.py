import json
import os
from jmespath import search as jpath
from dict_recursive_update import recursive_update
import shopify
from ..models import ShopifySite

class SearchableDict:
    def __init__(self,data):
        if data is None:
            return None
        for k in data.keys():
            if not hasattr(self,k):
                setattr(self,k,data[k])
        self.data = data
    def search(self,path,default=None):
        ret =  jpath(path,self.data)
        if ret is None:
            return default
        return ret
    def has(self,key):
        return hasattr(self,key)
    def get(self,key,default=None):
        if self.data.get(key):
            return self.data.get(key)
        else:
            return default
    def valueOf(self,key):
        ret = self.get(key)
        if ret is dict and self.search(f"{key}.refName"):
            return self.search(f"{key}.refName")
        else:
            return ret
    def dump(self,printIt=True):
        if printIt:
            print(json.dumps(self.data,indent=1))
        else:
            return self.data
    def set(self,key,value):
        paths = list(reversed(key.split(".")))
        if len(paths)>1:
            object = value
            for k in paths:
                object = {k:object}
            self.data = recursive_update(self.data,object)
        else:
            self.data[key] = value
    def getAsSearchable(self,key,default={}):
        val = self.search(key)
        if isinstance(val,list):
            return [SearchableDict(x) for x in val]
        if isinstance(val,dict):
            return SearchableDict(val)
        if val is None:
            return SearchableDict({})
        return val
    
    def append(self,key,value):
        myValue = self.search(key,[])
        myValue.append(value)
        self.set(key,myValue)
        return
        if key not in self.data:
            self.data[key] = value
        elif type(self.data[key]) is not list:
            self.data[key] = [self.data[key],value]
        else:
            self.data[key].append(value) 
    
class GqlReturn(SearchableDict):
    def errors(self,dump=False):
        if not hasattr(self,"errorDetails"):
            errorDetails = self.findErrors(self.data)
            setattr(self,"errorDetails",errorDetails)
            if dump:
                print(json.dumps(errorDetails,indent=1))
               
        return self.errorDetails
        
    def findErrors(self,object):
        if isinstance(object, dict):
            if "userErrors" in object:
                return object["userErrors"]
            elif "errors" in object:
                return [{"message":x.get("message"),"code":"NA","field":SearchableDict(x).search("problems[0].path[-1]")} for x in object.get("errors")]
            for key in object:
                item = self.findErrors(object[key])
                if item is not None:
                    return item
            
        elif isinstance(object, list):  
            for element in object:
                item = self.findErrors(element)
                if item is not None:
                    return item
        return None
    def errorMessages(self):
        if self.errors() is None:
            return []
        return [x.get("message") for x in self.errors()]
    def errorCodes(self):
        if self.errors() is None:
            return []
        return [x.get("code") for x in self.errors()]
    def hasErrorCode(self,code):
        return code in self.errorCodes()
    def hasErrors(self):
        return self.errors() is not None and  len(self.errors())>0
    def nodes(self,path):
        return [GqlReturn(x) for x in self.search(f"{path}.nodes",[])]
    
def mapLineItemProperties(properties):
    return {x.get("name"):x.get("value") for x in properties}

def shopifyInit():
    shopify_store = os.environ.get("SHOPIFY_DOMAIN")
    shopfiy_details = ShopifySite.objects.get(shopify_site=shopify_store)
        
    session = shopify.Session(
        f"{shopify_store}/admin",
        os.environ.get("SHOPIFY_API_VERSION"),
        shopfiy_details.access_token
    )
    shopify.ShopifyResource.activate_session(session)