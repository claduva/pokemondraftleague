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
from pokemondatabase.models import *

def league_detail(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('league_list')
    try:
        applications=league_application.objects.get(applicant=request.user)
        apply=False   
    except:
        try:
            coachdata.objects.filter(coach=request.user,league_name=league_)
            apply=False
        except:
            try:
                coachdata.objects.filter(teammate=request.user,league_name=league_)
                apply=False
            except:
                apply=True
    leaguesettings=league_settings.objects.get(league_name=league_)
    numberofconferences=leaguesettings.number_of_conferences
    numberofdivisions=leaguesettings.number_of_divisions
    numberofteams=leaguesettings.number_of_divisions
    divisionspefconference=int(numberofdivisions/numberofconferences)
    league_teams=coachdata.objects.all().filter(league_name=league_)
    context = {
        'league': league_,
        'apply': apply,
        'numberofconferences': range(numberofconferences),
        'divisionspefconference': range(divisionspefconference),
        'leaguepage': True,
        'league_name': league_name,
        'league_teams': league_teams,
    }
    return render(request, 'league_detail.html',context)

@login_required
def create_league(request):
    if request.method == 'POST':
        form = CreateLeagueForm(request.POST)
        if form.is_valid():
            newleague=form.save()
            messages.success(request,f'Your league has been successfully created!')
            allpokes=all_pokemon.objects.all()
            for item in allpokes:
                pokemon_tier.objects.create(pokemon=item,league=newleague)
            return redirect('league_detail',league_name=form.cleaned_data['name'])
    else:
        form = CreateLeagueForm(initial={'host': request.user})

    context = {
        'form': form,
    }
    return render(request, 'createleague.html',context)

def league_list(request):
    context={
        'leagueheading': 'All Leagues',
    }
    return render(request, 'leagues.html',context)

def recruiting_league_list(request):
    recruitinglist=league_settings.objects.filter(is_recruiting=True)
    context={
        'recruitinglist': recruitinglist,
        'leagueheading': 'Recruiting Leagues',
    }
    return render(request, 'leagues.html',context)

@login_required
def leagues_hosted_settings(request):
    context = {
        'settingheading': "Select League",
        'leagueshostedsettings': True,
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
        'leagueshostedsettings': True,
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
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_list')
    try:
        applications=league_application.objects.get(applicant=request.user)
        messages.error(request,'You have already applied to '+league_name+"!",extra_tags='danger')
        return redirect('league_detail',league_name=league_name)
    except:
        try:
            coachdata.objects.filter(teammate=request.user,league_name=league_)
            messages.error(request,'You are already a coach in '+league_name+"!",extra_tags='danger')
            return redirect('league_detail',league_name=league_name)
        except:
            try:
                coachdata.objects.filter(coach=request.user,league_name=league_)
                messages.error(request,'You are already a coach in '+league_name+"!",extra_tags='danger')
                return redirect('league_detail',league_name=league_name)
            except:
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
    league_=league.objects.get(name=league_name)
    if request.user != league_.host:
        messages.error(request,'Only a league host may manage coachs!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    applicants=league_application.objects.filter(league_name=league_)
    totalapplicants=len(applicants)
    coachs=coachdata.objects.filter(league_name=league_)
    leaguecapacity=league_.league_settings.number_of_teams
    numberofcoachs=leaguecapacity-len(coachs)
    spotsremaining=(numberofcoachs>0)
    context = {
        'applicants': applicants,
        'coachs': coachs,
        'league_name': league_name,
        'leagueshostedsettings': True,
        'numberofcoachs': numberofcoachs,
        'totalapplicants': totalapplicants,
        'spotsremaining': spotsremaining,
    }
    return render(request, 'managecoachs.html',context)

@login_required
def add_coach(request,league_name):
    if request.POST:
        application=league_application.objects.get(pk=request.POST['coach'])
        coachdata.objects.create(coach=application.applicant,league_name=application.league_name)
        application.delete()
    return redirect('manage_coachs',league_name=league_name)

@login_required
def remove_coach(request,league_name):
    if request.POST:
        league_=league.objects.get(name=league_name)
        coachtoremove=coachdata.objects.get(pk=request.POST['coach'])
        league_application.objects.create(applicant=coachtoremove.coach,league_name=coachtoremove.league_name)
        coachtoremove.delete()
    return redirect('manage_coachs',league_name=league_name)

@login_required
def leagues_coaching_settings(request):
    context = {
        'settingheading': "Select League",
        'leaguescoachingpage': True,
        'leaguescoachingsettings': True,
    }
    return render(request, 'leaguelist.html',context)

@login_required
def individual_league_coaching_settings(request,league_name):
    try:
        league_instance=league.objects.get(name=league_name)
        coachinstance=coachdata.objects.filter(league_name=league_instance,coach=request.user).first()
        settings=league_settings.objects.get(league_name=league_instance)
        allowsteams=settings.allows_teams
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.method == 'POST':
        if allowsteams:
            form = UpdateCoachInfoForm(
                request.POST,
                request.FILES,
                instance=coachinstance
                )
            tm_form=UpdateCoachTeammateForm(request.POST,instance=coachinstance)
            if form.is_valid() and tm_form.is_valid():
                form.save()
                tm_form.save()
                messages.success(request,'Your coach info has been updated!')
                return redirect('individual_league_coaching_settings',league_name=league_name)
        else:
            form = UpdateCoachInfoForm(
                request.POST,
                request.FILES,
                instance=coachinstance
                )
            if form.is_valid():
                form.save()
                messages.success(request,'Your coach info has been updated!')
                return redirect('individual_league_coaching_settings',league_name=league_name)
    else:
        form = UpdateCoachInfoForm(instance=coachinstance)
        forms=[]
        forms.append(form)
        if allowsteams:
            tm_form=UpdateCoachTeammateForm(instance=coachinstance)
            forms.append(tm_form)

    context = {
        'settingheading': league_name,
        'forms': forms,
        'leaguescoachingsettings': True,
    }
    return render(request, 'settings.html',context)

@login_required
def manage_tiers(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user != league_.host:
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.method == 'POST':
        form = CreateTierForm(request.POST)
        if form.is_valid() :
            form.save()
            messages.success(request,'Tier has been added!')
            return redirect('manage_tiers',league_name=league_name)
    else:
        form = CreateTierForm(initial={'league': league_})

    pokemontiers=pokemon_tier.objects.filter(league=league_).all().order_by('pokemon__pokemon','tier')
    leaguestiers=leaguetiers.objects.filter(league=league_).all().order_by('tiername')
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'pokemontiers': pokemontiers,
        'leaguetiers':leaguestiers,
        'forms': [form],
        'managetiers': True,
    }
    return render(request, 'managetiers.html',context)

@login_required
def delete_tier(request,league_name):
    if request.POST:
        tiertodelete=leaguetiers.objects.get(pk=request.POST['tiertodelete'])
        tiertodelete.delete()
    return redirect('manage_tiers',league_name=league_name)

@login_required
def edit_tier(request,league_name,tierid):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user != league_.host:
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.method == 'POST':
        tierinstance=leaguetiers.objects.get(pk=tierid)
        form = UpdateTierForm(request.POST,instance=tierinstance)
        if form.is_valid() :
            form.save()
            messages.success(request,'Tier has been edited!')
            return redirect('manage_tiers',league_name=league_name)
    else:
        tierinstance=leaguetiers.objects.get(pk=tierid)
        form=UpdateTierForm(instance=tierinstance)
    pokemontiers=None#pokemon_tier.objects.filter(league=league_).all().order_by('pokemon__pokemon','points')
    leaguestiers=leaguetiers.objects.filter(league=league_).all().order_by('tiername')
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'pokemontiers': pokemontiers,
        'leaguetiers':leaguestiers,
        'forms': [form],
        'editingtier': True,
    }
    return render(request, 'managetiers.html',context)

@login_required
def update_tier(request,league_name):
    if request.POST:
        pokemonofinterest=all_pokemon.objects.get(pokemon=request.POST['pokemon-select'])
        pokemontoupdate=pokemon_tier.objects.get(pokemon=pokemonofinterest)
        tiertoadd=leaguetiers.objects.get(pk=request.POST['tier-select'])
        pokemontoupdate.tier=tiertoadd
        pokemontoupdate.save()
        messages.success(request,'Tier has been edited!')
    return redirect('manage_tiers',league_name=league_name)

@login_required
def view_tier(request,league_name,tier):
    try:
        league_=league.objects.get(name=league_name)
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user != league_.host:
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.method == 'POST':
        form = CreateTierForm(request.POST)
        if form.is_valid() :
            form.save()
            messages.success(request,'Tier has been added!')
            return redirect('manage_tiers',league_name=league_name)
    else:
        form = CreateTierForm(initial={'league': league_})
        pokemontiers=pokemon_tier.objects.filter(league=league_).all().order_by('pokemon__pokemon','tier')
        leaguestiers=leaguetiers.objects.filter(league=league_).all().order_by('tiername')
        if tier=="Untiered":
            pokemonlist=pokemon_tier.objects.filter(league=league_,tier=None).all().order_by('pokemon__pokemon')
        else:
            tier=tier.replace("_"," ")
            tierofinterest=leaguetiers.objects.filter(league=league_,tiername=tier).first()
            pokemonlist=pokemon_tier.objects.filter(league=league_,tier=tierofinterest).all().order_by('pokemon__pokemon')
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'pokemontiers': pokemontiers,
        'leaguetiers':leaguestiers,
        'forms': [form],
        'pokemonlist': pokemonlist
    }
    return render(request, 'managetiers.html',context)

@login_required
def default_tiers(request,league_name):
    try:
        league_=league.objects.get(name=league_name)
        tier="Untiered"
    except:
        messages.error(request,'League does not exist!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.user != league_.host:
        messages.error(request,'Only a league host may access a leagues settings!',extra_tags='danger')
        return redirect('leagues_hosted_settings')
    if request.method == 'POST':
            templatetierset=leaguetiertemplate.objects.all().filter(template=request.POST['template-select'])
            templatepokemonset=pokemon_tier_template.objects.all().filter(template=request.POST['template-select'])
            existingtiers=leaguetiers.objects.all().filter(league=league_)
            existingpokemontiers=pokemon_tier.objects.all().filter(league=league_)
            for item in existingtiers:
                item.delete()
            for item in templatetierset:
                leaguetiers.objects.create(league=league_,tiername=item.tiername,tierpoints=item.tierpoints)
            for item in existingpokemontiers:
                item.delete()
            for item in templatepokemonset:
                tiertouse=leaguetiers.objects.get(tiername=item.tier.tiername)
                pokemon_tier.objects.create(pokemon=item.pokemon,league=league_,tier=tiertouse)
            messages.success(request,'The template has been applied!')
            return redirect('manage_tiers',league_name=league_name)
    else:
        pokemonlist=pokemon_tier.objects.filter(league=league_,tier=None).all().order_by('pokemon__pokemon')
        pokemontiers=pokemon_tier.objects.filter(league=league_).all().order_by('pokemon__pokemon','tier')
        leaguestiers=leaguetiers.objects.filter(league=league_).all().order_by('tiername')
        availabletemplates=leaguetiertemplate.objects.all().distinct('template')
        form = CreateTierForm(initial={'league': league_})
    context = {
        'league_name': league_name,
        'leagueshostedsettings': True,
        'pokemontiers': pokemontiers,
        'leaguetiers':leaguestiers,
        'forms': [form],
        'pokemonlist': pokemonlist,
        'defaulttemplate': True,
        'availabletemplates': availabletemplates,
    }
    return render(request, 'managetiers.html',context)