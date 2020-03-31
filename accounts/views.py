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
    try:  
        site_settings = request.user.sitesettings
    except:
        user=User.objects.get(username="defaultuser")
        site_settings = user.sitesettings
    #favorite pokemon
    alldraft=list(draft.objects.all().exclude(pokemon__isnull=True).filter(Q(team__coach=userofinterest)|Q(team__teammate=userofinterest)).values_list('pokemon',flat=True))
    allhistoricdraft=list(historical_draft.objects.all().exclude(pokemon__isnull=True).filter(Q(team__coach1=userofinterest)|Q(team__coach2=userofinterest)).values_list('pokemon',flat=True))
    allfreeagency=list(free_agency.objects.all().exclude(addedpokemon__isnull=True).filter(Q(coach__coach=userofinterest)|Q(coach__teammate=userofinterest)).values_list('addedpokemon',flat=True))
    allhistoricfreeagency=list(historical_freeagency.objects.all().exclude(addedpokemon__isnull=True).filter(Q(team__coach1=userofinterest)|Q(team__coach2=userofinterest)).values_list('addedpokemon',flat=True))
    alltrading=list(trading.objects.all().exclude(addedpokemon__isnull=True).filter(Q(coach__coach=userofinterest)|Q(coach__teammate=userofinterest)).values_list('addedpokemon',flat=True))
    allhistorictrading=list(historical_trading.objects.all().exclude(addedpokemon__isnull=True).filter(Q(team__coach1=userofinterest)|Q(team__coach2=userofinterest)).values_list('addedpokemon',flat=True))
    monlist=alldraft+allhistoricdraft+allfreeagency+allhistoricfreeagency+alltrading+allhistorictrading
    allmons=all_pokemon.objects.all()
    mostacquired_=list(dict(Counter(monlist)).items())
    mostacquired_=list(filter(lambda x: x[1]>1,mostacquired_))
    mostacquired=[]
    for item in mostacquired_:
        moi=allmons.get(id=item[0])
        mostacquired.append([moi.pokemon,item[1],get_sprite_url(moi,site_settings.sprite)])
    mostacquired=sorted(mostacquired,key=lambda x: x[0])
    mostacquired=sorted(mostacquired,key=lambda x: x[1], reverse=True)
    #all matches
    usermatches=replaydatabase.objects.all().filter(Q(team1coach1=request.user)|Q(team1coach2=request.user)|Q(team2coach1=request.user)|Q(team2coach2=request.user))
    userhistoricmatches=usermatches.filter(associatedhistoricmatch__isnull=False)
    usermatches=usermatches.filter(associatedhistoricmatch__isnull=True)
    usermatches_t1=list(usermatches.filter(Q(team1coach1=request.user)|Q(team1coach2=request.user)).values_list('associatedmatch__season__league__name','associatedmatch__season__seasonname','associatedmatch__week','associatedmatch__team2__teamname','associatedmatch__replay','associatedmatch__team1score'))
    usermatches_t2=list(usermatches.filter(Q(team2coach1=request.user)|Q(team2coach2=request.user)).values_list('associatedmatch__season__league__name','associatedmatch__season__seasonname','associatedmatch__week','associatedmatch__team1__teamname','associatedmatch__replay','associatedmatch__team2score'))
    userhistoricmatches_t1=list(userhistoricmatches.filter(Q(team1coach1=request.user)|Q(team1coach2=request.user)).values_list('associatedhistoricmatch__team1__league__name','associatedhistoricmatch__team1__seasonname','associatedhistoricmatch__week','associatedhistoricmatch__team2__teamname','associatedhistoricmatch__replay','associatedhistoricmatch__team1score'))
    userhistoricmatches_t2=list(userhistoricmatches.filter(Q(team2coach1=request.user)|Q(team2coach2=request.user)).values_list('associatedhistoricmatch__team1__league__name','associatedhistoricmatch__team1__seasonname','associatedhistoricmatch__week','associatedhistoricmatch__team1__teamname','associatedhistoricmatch__replay','associatedhistoricmatch__team2score'))
    matchlist_=usermatches_t1+usermatches_t2+userhistoricmatches_t1+userhistoricmatches_t2
    matchlist=[]
    for item in matchlist_:
        matchlist.append([item[0],item[1],item[2],item[3],item[4],item[5]])
    context = {
        "title": f"{username}'s Profile",
        'userofinterest':userofinterest,
        'winpercent':winpercent,
        'mostacquired':mostacquired,
        'matchlist':matchlist,
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
def reply_message(request,messageid):
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
    form=ReplyMessageForm(initial={
        'sender':request.user,
        'recipient': messageofinterest.sender,
        'messagesubject': messageofinterest.messagesubject,
        })
    if request.method == 'POST':
        form = ReplyMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your reply has been sent!')
            return redirect('inbox_item',messageid=messageid)
    context = {
        'messageofinterest': messageofinterest,
        'form':form,
        'reply':True,
    }
    return render(request, 'inbox.html',context)

@login_required
def compose_message(request):
    form=ComposeMessageForm(initial={'sender':request.user})
    if request.method == 'POST':
        form = ComposeMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your message has been sent!')
            return redirect('inbox')
    context = {
        'form': form,
        'compose':True,
    }
    return render(request,"inbox.html",context)

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
    messageofinterest.delete()
    messages.success(request,'Message deleted!')
    return redirect('inbox') 

@login_required
def delete_inbox(request):   
    inbox.objects.all().filter(recipient=request.user).delete()
    messages.success(request,'Your inbox has been emptied!')
    return redirect('inbox') 

@login_required
def read_inbox(request):   
    inbox.objects.all().filter(recipient=request.user).update(read=True)
    messages.success(request,'Success!')
    return redirect('inbox') 

def get_sprite_url(poi,arg):
    if arg=="swsh/ani/standard/PKMN.gif":
        string=poi.sprite.dexani.url
    elif arg=="swsh/ani/shiny/PKMN.gif":
        string=poi.sprite.dexanishiny.url
    elif arg=="swsh/png/standard/PKMN.png":
        string=poi.sprite.dex.url
    elif arg=="swsh/png/shiny/PKMN.png":
        string=poi.sprite.dexshiny.url
    elif arg=="bw/png/standard/PKMN.png":
        string=poi.sprite.bw.url
    elif arg=="bw/png/shiny/PKMN.png":
        string=poi.sprite.bwshiny.url
    elif arg=="afd/png/standard/PKMN.png":
        string=poi.sprite.afd.url
    elif arg=="afd/png/shiny/PKMN.png":
        string=poi.sprite.afdshiny.url
    return string