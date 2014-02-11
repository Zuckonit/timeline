from django.contrib.auth.models import User
from django.shortcuts import render_to_response as render
from django.contrib import auth
from django.http import Http404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from models import UserProfile

from forms import LoginForm, RegisterForm, ProfileForm

def _register(request):
    if request.user.is_authenticated():
        auth.logout(request)
    if request.method == 'GET':
        form = RegisterForm()
        return render('register.html', RequestContext(request, {'form': form}))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            re_password = request.POST.get('re_password', '')
            email = request.POST.get('email', '')
            if password != re_password:
                return render('register.html', RequestContext(request, {'form': form}))
            obj_user = User.objects
            if obj_user.filter(username=username).exists() or obj_user.filter(email=email).exists():
                message(request, 'user or email already existed')
                return render('register.html', RequestContext(request, {'form': form}))
            new_user = obj_user.create_user(username=username, password=password, email=email)
            new_user.is_active = True
            new_user.is_staff = True
            try:
                new_user.save()
                return HttpResponseRedirect('/account/login')
            except:
                message(request, 'register new user failed!')
                return render('register.html', RequestContext(request, {'form': form}))
            return HttpResponseRedirect('/account/login')
        return render('register.html', RequestContext(request, {'form': form}))


def _login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/admin')
    if request.method == 'GET':
        form = LoginForm()
        return render('login.html', RequestContext(request, {'form': form}))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('/admin')
            return render('login.html', RequestContext(request, {'form':form, 'password_is_wrong':True}))
        return render('login.html', RequestContext(request, {'form':form, }))


def _logout(request):
    if request.user.is_authenticated():
        auth.logout(request)
    return HttpResponseRedirect('/account/login')

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
        #if cur_user.filter(birthday=birthday).exists() and cur_user.filter(sex=sex).exists():
            #return HttpResponseRedirect('/admin')
        cur_user.sex = sex
        cur_user.birthday = birthday
        cur_user.save()
        return HttpResponseRedirect('/admin')



