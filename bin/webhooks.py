#!/usr/bin/env python3

from pathlib import Path
import sys
import os
import uuid


if __package__ is None:                  
    DIR = Path(__file__).resolve().parent
    sys.path.insert(0, str(DIR.parent))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopify_django_app.settings')
    
    try:
        from django.core.management import execute_from_command_line
        import django
        django.setup()
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    __package__ = DIR.name




import shopify
import json
import csv
import os
from jmespath import search as jpath
from argparse import ArgumentParser
from home.esc.graphql_common import Webhooks
import requests

def hookByTopic(topic):
    for hook in jpath("data.webhookSubscriptions.nodes",Webhooks().list()):
        if hook.get("topic")==topic:
            return hook
    return None

session = shopify.Session(f"{os.environ.get('SHOPIFY_DOMAIN')}","2024-07",os.environ.get("SHOPIFY_TOKEN"))
shopify.ShopifyResource.activate_session(session)

parser = ArgumentParser()
parser.add_argument("--list",action='store_true')
parser.add_argument("--trigger",action='store_true')
parser.add_argument("--local",action='store_true')
parser.add_argument("--path",required=False)
args = parser.parse_args()



    
if args.list:
    print(json.dumps(Webhooks().list(),indent=1))
elif args.trigger:
    if not hasattr(args,"path"):
        print("topic required to trigger webhook!")
        sys.exit()        
    url = f"{os.environ.get('APP_URL') if not args.local else 'http://127.0.0.1:8000/'}{args.path}"
    print(url)
    ret = requests.post(
        url,
        data=sys.stdin.read(),
        headers={
            "Content-Type":"application/json",
            "X-Shopify-Shop-Domain":os.environ.get("SHOPIFY_DOMAIN"),
            "X-Shopify-Event-Id":uuid.uuid1().hex
        }
    )
    print(ret.content)
    print(json.dumps(ret.json(),indent=1))


