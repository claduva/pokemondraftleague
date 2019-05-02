# accounts/views.py
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages

from .forms import *
from .models import *

def league_detail(request,league_name):
    league_=league.objects.get(name=league_name)
    try:
        applications=league_application.objects.get(applicant=request.user)
        apply=False
    except:
        apply=True
    context = {
        'league': league_,
        'apply': apply,
    }
    return render(request, 'league_detail.html',context)

@login_required
def create_league(request):
    if request.method == 'POST':
        form = CreateLeagueForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,f'Your league has been successfully created!')
            return redirect('league_detail',league_name=form.cleaned_data['name'])
    else:
        form = CreateLeagueForm(initial={'host': request.user})

    context = {
        'form': form,
    }
    return render(request, 'createleague.html',context)

def league_list(request):
    return render(request, 'leagues.html')

@login_required
def leagues_hosted_settings(request):
    context = {
        'settingheading': "Select League",
    }
    return render(request, 'leaguelist.html',context)

@login_required
def individual_league_settings(request,league_name):
    try:
        league_instance=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user != league_instance.host:
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    league_settings_instance=league_settings.objects.get(league_name=league_instance)
    if request.method == 'POST':
        l_form = UpdateLeagueForm(
            request.POST,
            request.FILES,
            instance=league_instance
            )
        ls_form = UpdateLeagueSettingsForm(request.POST,instance=league_settings_instance)
        if l_form.is_valid() and ls_form.is_valid():
            l_form.save()
            ls_form.save()
            messages.success(request,league_name+' has been updated!')
            return redirect('individual_league_settings',league_name=league_name)
    else:
        l_form = UpdateLeagueForm(instance=league_instance)
        ls_form = UpdateLeagueSettingsForm(instance=league_settings_instance)

    context = {
        'settingheading': league_name,
        'forms': [l_form,ls_form],
        'deletebutton': 'Delete League',
    }
    return render(request, 'settings.html',context)

@login_required
def delete_league(request,league_name):
    try:
        leaguetodelete=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user != leaguetodelete.host:
        messages.error(request,'Only a league host may delete a league!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    leaguetodelete.delete()
    messages.success(request,league_name+' has been deleted!')
    return redirect('leagues_hosted_settings')

@login_required
def league_apply(request,league_name):
    try:
        applications=league_application.objects.get(applicant=request.user)
        messages.error(request,'You have already applied to '+league_name+"!",extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    except:
        try:
            league_=league.objects.get(name=league_name)
        except:
            messages.error(request,'League does not exist!',extra_tags='danger')
            return redirect('leagues_list')
        if league_.league_settings.is_recruiting == False:
            messages.error(request,league_name+' is not currently accepting applications!',extra_tags='danger')
            return redirect('leagues_list')
        if request.method == 'POST':
            form = LeagueApplicationForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,'You have successfully applied to '+league_name+"!")
                return redirect('league_detail',league_name=league_name)
        else:
            form = LeagueApplicationForm(initial={
                'applicant': request.user,
                'league_name': league_
                })
            
        context = {
            'league': league_,
            'forms': [form],
        }
        return render(request, 'leagueapplication.html',context)

@login_required
def manage_coachs(request,league_name):
    context = {
        'settingheading': "Select League",
    }
    return render(request, 'managecoachs.html',context)