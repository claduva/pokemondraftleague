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

class SignUp(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

@login_required
def profile(request):
    leagueshosted = request.user.league_set.all()
    print(leagueshosted)
    context = {
        "title": "Profile",
    }
    return render(request, 'profile.html',context)

@login_required
def settings(request):
    if request.method == 'POST':
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
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile) 

    context = {
        'forms': [u_form,p_form],
        'settingheading': "Update User Info",
        'usersettings': True,
    }
    return render(request, 'settings.html',context)

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