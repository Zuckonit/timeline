from django.shortcuts import render_to_response as  render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from models import TimeLine
from forms import TimeLineForm


@login_required
def post_new_timeline(request):
    if request.method == 'GET':
        form = TimeLineForm()
        return render('post_timeline.html', RequestContext(request, {'form':form}))
    if request.method == 'POST':
        form  = TimeLineForm(request.POST)
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        obj_timeline = TimeLine.objects
        obj_timeline.create(user=request.user, title=title, content=content)
        return HttpResponseRedirect('/blog/')


@login_required
def show_user_timeline(request):
    user = request.user.username
    pieces = TimeLine.objects.filter(user=request.user)
    return render('timeline.html', RequestContext(request, {'username':user, 'pieces':pieces,}))


def index_page(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/blog')
    return HttpResponseRedirect('/account/login')
