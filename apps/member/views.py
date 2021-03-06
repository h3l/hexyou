# Create your views here.
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response,redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from activity.models import Activity
from group.models import MemberShip, Group
from member.forms import EditProfileForm
from django import forms
from messages.forms import ComposeForm
from django.template import RequestContext
from django.contrib.auth.forms import PasswordChangeForm

def frontpage(request):
    """docstring for person"""
    return render_to_response('members/frontpage.html')

@login_required(login_url='/login/')
def single(request,username):
    """docstring for person"""
    view_user = User.objects.get(username=username)
    is_me = request.user.username==username
    groups = Group.objects.filter(members=view_user,membership__is_approved=True)[:8].values()
    group_counter = Group.objects.filter(members=view_user,membership__is_approved=True).count()
    participated_activities = Activity.objects.filter(members=view_user,memberhostship__is_host=False)
    participated_activities_slice = participated_activities[:4].annotate(Count('members'))
    participated_activities_count = participated_activities.count()
    hosted_activities = Activity.objects.filter(members=view_user,memberhostship__is_host=True)
    hosted_activities_slice = hosted_activities[:4].annotate(Count('members'))
    hosted_activities_count = hosted_activities.count()
    form = ComposeForm()
    return render_to_response('members/single.html',locals(), context_instance=RequestContext(request))

@login_required(login_url='/login/')
def profile(request):
    return single(request,request.user.username)
    # return render_to_response('members/single.html',{'user':request.user,'is_me':True})

@login_required(login_url='/login/')
def edit_profile(request):
    if request.POST:
        form = EditProfileForm(request.POST,instance=request.user)
        if form.is_valid(): form.save()
        if request.POST.has_key('old_password'):
            passform=PasswordChangeForm(request.user,request.POST)
            if passform.is_valid() : passform.save()
        else:
            passform=PasswordChangeForm(request.user)
    else:
        form = EditProfileForm(instance=request.user)
        passform=PasswordChangeForm(request.user)
    return render_to_response('members/edit.html',{'user':request.user,'form':form,'is_me':True,'passform':passform},context_instance=RequestContext(request))

@login_required()
def my(request):
    pass