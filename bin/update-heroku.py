#!/usr/bin/env python3

import os
import sys
import json
from urllib.parse import urlparse
from password_generator import PasswordGenerator
import subprocess
import heroku3
import toml
import json
from slugify import slugify
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--heroku_key",required=True)
parser.add_argument("--app",required=True)

args = parser.parse_args()

config = {}
for line in open(".env").readlines():
    if "=" not in line:
        continue
    line = line.replace("\n","").strip()
    key = line[0:line.index("=")]
    value = line[line.index("=")+1:len(line)].strip()
    config[key] = value
    


print("Configuring Heroku...")
heroku = heroku3.from_key(args.heroku_key)

ret = heroku.update_appconfig(
    args.app,
    {key:config[key] for key in filter(lambda x: x not in ["SHOPIFY_TOKEN"],config.keys()) }
)