#!/usr/bin/env python3

import os
import sys
import heroku3
import toml
import json
from slugify import slugify
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--heroku_key",required=True)
parser.add_argument("--app",required=True)

args = parser.parse_args()
heroku = heroku3.from_key(args.heroku_key)
app = heroku.apps()[args.app]
config = app.config()


envfile = open(".env","w")
for key,value in config.to_dict().items():
    print(f"{key}={value}")
    envfile.write(f"{key}={value}\n")
envfile.close()

    
