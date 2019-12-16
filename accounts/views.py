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
from django.db.models import Q

from collections import Counter

from .forms import *

from pokemonadmin.models import *

import math

class SignUp(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

def user_profile(request,username):
    try:
        userofinterest=User.objects.get(username=username)
        userprofile=userofinterest.profile
    except:
        messages.error(request,'User does not exist!',extra_tags='danger')
        return redirect('home')
    try:
        winpercent=f'{round(userprofile.wins/(userprofile.wins+userprofile.losses)*100)}%'
    except:
        winpercent='N/A'
    #favorite pokemon
    alldraft=list(draft.objects.all().exclude(pokemon__isnull=True).filter(Q(team__coach=userofinterest)|Q(team__teammate=userofinterest)).values_list('pokemon',flat=True))
    allhistoricdraft=list(historical_draft.objects.all().filter(Q(team__coach1=userofinterest)|Q(team__coach2=userofinterest)).values_list('pokemon',flat=True))
    allfreeagency=list(free_agency.objects.all().filter(Q(coach__coach=userofinterest)|Q(coach__teammate=userofinterest)).values_list('addedpokemon',flat=True))
    allhistoricfreeagency=list(historical_freeagency.objects.all().filter(Q(team__coach1=userofinterest)|Q(team__coach2=userofinterest)).values_list('addedpokemon',flat=True))
    alltrading=list(trading.objects.all().filter(Q(coach__coach=userofinterest)|Q(coach__teammate=userofinterest)).values_list('addedpokemon',flat=True))
    allhistorictrading=list(historical_trading.objects.all().filter(Q(team__coach1=userofinterest)|Q(team__coach2=userofinterest)).values_list('addedpokemon',flat=True))
    monlist_=alldraft+allhistoricdraft+allfreeagency+allhistoricfreeagency+alltrading+allhistorictrading
    monlist=[]
    allmons=all_pokemon.objects.all()
    for item in monlist_:
        monlist.append(allmons.get(id=item).pokemon)
    mostacquired=dict(Counter(monlist))
    mostacquired={k:v for (k,v) in mostacquired.items() if v>1}
    mostacquired = dict(sorted(mostacquired.items() ,reverse=True,  key=lambda x: x[1]))
    print(mostacquired)
    context = {
        "title": f"{username}'s Profile",
        'userofinterest':userofinterest,
        'winpercent':winpercent,
        'mostacquired':mostacquired,
    }
    return render(request, 'userprofile.html',context)

@login_required
def settings(request):
    if request.method == 'POST':
        if request.POST['purpose']=='Delete':
            showdownalts.objects.get(id=request.POST['altid']).delete()
            messages.success(request,'Alt has been deleted!')
        else:
            u_form = UserUpdateForm(request.POST,instance=request.user)
            p_form = ProfileUpdateForm(
                request.POST,
                request.FILES,
                instance=request.user.profile
                )
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.success(request,f'Your account has been updated!')
            else: 
                print(p_form.errors)
    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile) 
    showdown_alts = showdownalts.objects.all().filter(user=request.user)
    context = {
        'forms': [u_form,p_form],
        'settingheading': "Update User Info",
        'usersettings': True,
        'showdownalts': showdown_alts,
    }
    return render(request, 'usersettings.html',context)

@login_required
def site_settings(request):
    if request.method == 'POST':
        form = SiteSettingUpdateForm(request.POST,instance=request.user.sitesettings)
        if form.is_valid():
            form.save()
            messages.success(request,f'Your settings have been updated!')
            return redirect('site_settings')
    else:
        form = SiteSettingUpdateForm(instance=request.user.sitesettings)

    context = {
        'forms': [form],
        'settingheading': "Update Site Settings",
        'sitesettings': True,
    }
    return render(request, 'settings.html',context)

@login_required
def add_showdown_alt(request):
    if request.method == 'POST':
        alt=request.POST['showdownalt']
        showdownalts.objects.create(user=request.user,showdownalt=alt)
        messages.success(request,f'Your account has been updated!')
        return redirect('settings')

@login_required
def inbox_view(request):
    context = {
        'startinbox': True
    }
    return render(request, 'inbox.html',context)

@login_required
def inbox_item_view(request,messageid):
    try:
        messageofinterest=inbox.objects.get(pk=messageid)
    except:
        messages.error(request,"Message doesnt exist",extra_tags="danger")
        return redirect('inbox')
    if request.user != messageofinterest.recipient:
        messages.error(request,"You do not have permission to view this message!",extra_tags="danger")
        return redirect('inbox')
    messageofinterest.read=True
    messageofinterest.save()
    context = {
        'messageofinterest': messageofinterest,
    }
    return render(request, 'inbox.html',context)

@login_required
def inbox_item_delete(request,messageid):
    try:
        messageofinterest=inbox.objects.get(pk=messageid)
    except:
        messages.error(request,"Message doesnt exist",extra_tags="danger")
        return redirect('inbox')
    if request.user != messageofinterest.recipient:
        messages.error(request,"You do not have permission to delete this message!",extra_tags="danger")
        return redirect('inbox')
    if messageofinterest.traderequest:
        sender=messageofinterest.traderequest.requestedpokemon.team.coach
        recipient=messageofinterest.traderequest.offeredpokemon.team.coach
        messagebody=f"Hello,\nI regret to inform you that I am rejecting your trade offer of your {messageofinterest.traderequest.offeredpokemon.pokemon.pokemon} for my {messageofinterest.traderequest.requestedpokemon.pokemon.pokemon}. Thank you anyway."
        inbox.objects.create(sender=sender,recipient=recipient,messagesubject="Trade Request Rejected",messagebody=messagebody)
        messageofinterest.traderequest.delete()   
        messages.success(request,'Trade request denied!')
        messageofinterest.delete()
        return redirect('inbox')      
    messageofinterest.delete()
    messages.success(request,'Message deleted!')
    return redirect('inbox')

@login_required
def accept_trade(request,messageid):
    try:
        messageofinterest=inbox.objects.get(pk=messageid)
    except:
        messages.error(request,"Message doesnt exist",extra_tags="danger")
        return redirect('inbox')
    if request.user != messageofinterest.recipient:
        messages.error(request,"You do not have permission to delete this message!",extra_tags="danger")
        return redirect('inbox')
    if messageofinterest.traderequest:
        offered=messageofinterest.traderequest.offeredpokemon
        requested=messageofinterest.traderequest.requestedpokemon
        offeredteam=offered.team
        requestedteam=requested.team
        sender=messageofinterest.traderequest.requestedpokemon.team.coach
        recipient=messageofinterest.traderequest.offeredpokemon.team.coach
        offered.team=requestedteam
        requested.team=offeredteam
        offered.zuser="N"
        requested.zuser="N"
        offered_=trading.objects.create(coach=offeredteam,season=offered.season,droppedpokemon=offered.pokemon,addedpokemon=requested.pokemon)
        trading.objects.create(coach=requestedteam,season=requested.season,droppedpokemon=requested.pokemon,addedpokemon=offered.pokemon)
        offered.save()
        requested.save()
        messagebody=f"Hello,\nI am happy to inform you that I am accepting your trade offer of your {messageofinterest.traderequest.offeredpokemon.pokemon.pokemon} for my {messageofinterest.traderequest.requestedpokemon.pokemon.pokemon}. Thank you!"
        inbox.objects.create(sender=sender,recipient=recipient,messagesubject="Trade Request Accepted",messagebody=messagebody)
        messageofinterest.traderequest.delete()   
        messages.success(request,'Trade request accepted!')
        league_=offeredteam.league_name
        discordserver=league_.subleague.first().discord_settings.discordserver
        discordchannel=league_.subleague.first().discord_settings.tradechannel
        request_league=seasonsetting.objects.get(league=league_)
        league_start=request_league.seasonstart
        elapsed=offered_.timeadded-league_start
        weekrequested=math.ceil(elapsed.total_seconds()/60/60/24/7)
        if weekrequested>0:
            weekeffective=weekrequested+1
        else:
            weekeffective=1
        title=f"The {offeredteam.teamname} have agreed to trade their {offered.pokemon.pokemon} to the {requestedteam.teamname} for their {requested.pokemon.pokemon}. Effective Week {weekeffective}."
        trading_announcements.objects.create(
            league = discordserver,
            league_name = league_.name,
            text = title,
            tradingchannel = discordchannel
        )
        messageofinterest.delete()
        return redirect('inbox')   
    else:
        messages.error(request,"There is no trade request associated with this message!",extra_tags="danger")
        return redirect('inbox')   