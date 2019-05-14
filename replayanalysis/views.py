from django.http import HttpResponse, Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core import serializers

import json
from datetime import datetime
import time

from .models import *
from .forms import *
from .ShowdownReplayParser.replayparser import *

# Create your views here.
def replay_analysis(request):
    if request.method=="POST":
        form = MatchReplayForm(request.POST)
        if form.is_valid():
            url=form.cleaned_data['url']
            outputstring, team1, team2 = replayparse(url)
            context={
                'output': outputstring,
                'team1':team1,
                'team2':team2,
                'replay': url,
            }
            return render(request,"replayanalysisform.html",context)
    form=MatchReplayForm()
    context={
        'form': form,
        'submission': True,
    }
    return  render(request,"replayanalysisform.html",context)

