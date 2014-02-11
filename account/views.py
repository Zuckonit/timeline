from django.contrib.auth.models import User
from django.shortcuts import render_to_response as render
from django.contrib import auth
from django.http import Http404
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from models import UserProfile
from datetime import date

from forms import LoginForm, RegisterForm, ProfileForm

REGISTER_TURN_OFF = False

def _register(request):
    if REGISTER_TURN_OFF:
        return render('register_turn_off.html', RequestContext(request))
    if request.user.is_authenticated():
        auth.logout(request)
    if request.method == 'GET':
        form = RegisterForm()
        return render('register.html', RequestContext(request, {'form': form}))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            data = form.clean()
            if data['password'] != data['re_password']:
                return render('register.html', RequestContext(request, {'form': form}))
            obj_user = User.objects
            if obj_user.filter(username=data['username']).exists() or obj_user.filter(email=data['email']).exists():
                messages.error(request, 'user or email already existed')
                return render('register.html', RequestContext(request, {'form': form}))
            new_user = obj_user.create_user(username=data['username'], password=data['password'], email=data['email'])
            new_user.is_active = True
            new_user.is_staff = True
            new_user.save()
            new_profile = UserProfile(user=new_user)
            try:
                new_profile.save()
                return HttpResponseRedirect('/')
            except:
                messages.error(request, 'register new user failed!')
                return render('register.html', RequestContext(request, {'form': form}))
            return HttpResponseRedirect('/')
        return render('register.html', RequestContext(request, {'form': form}))


@csrf_protect
def _login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
    if request.method == 'GET':
        referer  = request.META.get('HTTP_REFERER','/')
        if not 'accounts' in str(referer) :
            request.session['referer'] = referer
        else :
            request.session['referer'] = '/'
        form = LoginForm()
        return render('login.html', RequestContext(request, {'form': form}))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.clean()
            user = auth.authenticate(username=data['username'], password=data['password'])
            if user is not None and user.is_active:
                auth.login(request, user)
                next = request.GET.get('next') or request.session['referer'] or '/'
                return HttpResponseRedirect(next)
        return render('login.html', RequestContext(request, {'form':form, }))


def _logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect('/')


@login_required
def _update_profile(request):
    if request.method == 'GET':
        form = ProfileForm()
        return render('update_profile.html', RequestContext(request, {'form': form}))
    if request.method == 'POST':
        form  = ProfileForm(request.POST)
        sex = request.POST.get('sex', '')
        birthday = request.POST.get('birthday', '')
        profile_obj = UserProfile.objects
        cur_user = profile_obj.get(user=request.user)
        cur_user.sex = sex
        b = birthday.split('/')
        cur_user.birthday = date(int(b[2]), int(b[0]), int(b[1]))
        cur_user.save()
        return HttpResponseRedirect('/')


@login_required
def show_user_profile(request):
    #username = request.user.username
    profile = UserProfile.objects.get(user=request.user)
    return render('profile.html', RequestContext(request, {'profile':profile,}))
