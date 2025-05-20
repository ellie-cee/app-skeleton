from django.shortcuts import render,redirect
import shopify
from shopify_app.decorators import shop_login_required
from ..esc.common import *

import logging
import json
from django.http import HttpResponse
from ..models import ShopifySite,functionConfigGroup,FunctionConfig
from . import webhooks
from ..esc.graphql import Discounts
from .webhooks import FirstSubscriptionGift
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from jmespath import search as jsearch
import os

@csrf_exempt
def subscriptionsHandler(request):
    return FirstSubscriptionGift(request).run()