from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers

import json
from datetime import datetime
import time

from .models import *
# Create your views here.
def home(request):
    context = {
        "title": "Pokemon Draft League",
    }
    return  render(request,"index.html", context)

def about(request):
    return  render(request,"about.html")