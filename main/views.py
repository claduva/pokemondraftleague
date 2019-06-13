from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers
from django.db.models import Q

import json
from datetime import datetime
import time

from accounts.forms import UserRegisterForm
from .models import *
from leagues.models import *

# Create your views here.
def home(request):
    try:
        yourleagues=coachdata.objects.all().filter(Q(coach=request.user)|Q(teammate=request.user))
        if yourleagues.count()>0:
            context = {
                "title": "Pokemon Draft League",
                "yourleagues": yourleagues,
            }
            return  render(request,"coachlandingpage.html", context)
    except:
        print("error")
    form=form = UserRegisterForm()
    context = {
        "title": "Pokemon Draft League",
        "form": form,
    }
    return  render(request,"index.html", context)

def about(request):
    return  render(request,"about.html")