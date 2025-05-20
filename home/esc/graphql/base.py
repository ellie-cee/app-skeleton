import requests
import shopify
import json
import os
import logging
from jmespath import search as jsearch
from ..common import *

logger = logging.getLogger(__name__)
class GraphQL:
    def __init__(self):
        pass
        
    def run(self,query,variables={}):
        return GqlReturn(json.loads(shopify.GraphQL().execute(query,variables)))
    
class GraphQlIterable(GraphQL):
    def __init__(self, query,params,dataroot="data.products"):
        super().__init__(searchable=True,debug=False)
        self.cursor = None
        self.hasNext = True
        self.query = query
        self.params = params
        self.dataroot = dataroot
    def __iter__(self):
        return self
    def __next__(self):
        if not self.hasNext:
            raise StopIteration
        self.params["after"] = self.cursor
        print(self.params)
        ret = self.run(self.query,self.params)
        if ret.get("data") is not None: 
            self.dataroot = next(ret.get("data").keys(),None)
            
        values = [SearchableDict(x) for x in ret.search(f"{self.dataroot}.nodes",[])]
        if ret.search(f"{self.dataroot}.pageInfo.hasNextPage"):
            self.hasNext = True
            self.cursor = ret.search(f"{self.dataroot}.pageInfo.endCursor")
        else:
            self.hasNext = False
        return values