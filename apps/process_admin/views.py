# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from apps.process_admin.forms import *
from apps.process_admin.models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


def get_users_by_workers(request):
	"""Return all User objects depending of GET var 'workers'"""
	is_active_worker = True
	w = None
	if request.method == "GET" and 'workers' in request.GET:
		try:
			w = int(request.GET.get("workers"))
		except Exception, e:
			print "Exception: ",e
			w = 1
		is_active_worker = bool(w)
	users = User.objects.filter(userprofile__is_active_worker=is_active_worker, userprofile__is_active=True)
	return users, is_active_worker


@login_required()
def read_users(request):
	from apps.account.forms import UserForm
	from apps.process_admin.forms import UserProfileForm
	if request.method == 'POST':
		user_form  = UserForm(request.POST)
		userprofile_form  = UserProfileForm(request.POST)
		u = user_form.is_valid()
		up = userprofile_form.is_valid()
		if u and up:
			_user = user_form.save()
			_up = userprofile_form.save(commit=False)
			_up.id_user = _user
			_up.save()
			user_form = UserForm()
			userprofile_form  = UserProfileForm()
		else:
			show_form = True
		if '_createanother' in request.POST:
			show_form = True
	else:
		user_form  = UserForm()
		userprofile_form  = UserProfileForm()
	form_mode  = "_create"
	users, is_active_worker = get_users_by_workers(request)
	return render_to_response("users/read_users.html", locals(), context_instance=RequestContext(request))


@login_required()
def read_user(request, id_user):
	users = User.objects.all()
	return render_to_response("read_user.html", locals(), context_instance=RequestContext(request))


@login_required()
def update_user(request, id_user):
	_user = get_object_or_404(User, pk=id_user)
	users, is_active_worker = get_users_by_workers(request)
	from apps.account.forms import UserForm
	from apps.process_admin.forms import UserProfileForm
	if request.method == "POST":
		user_form  = UserForm(request.POST, instance=_user)
		userprofile_form  = UserProfileForm(request.POST, instance=_user.userprofile)
		u = user_form.is_valid()
		up = userprofile_form.is_valid()
		if u and up:
			_user = user_form.save()
			_up = userprofile_form.save()
			user_form = UserForm()
			userprofile_form  = UserProfileForm()
			w=1
			try:
				w = int(request.GET.get("workers"))
			except Exception:
				w = 1
			return HttpResponseRedirect(reverse(read_users) + "?workers=" + str(w))
		else:
			show_form = True
	else:
		show_form = True
		user_form  = UserForm(instance=_user)
		userprofile_form  = UserProfileForm(instance=_user.userprofile)
	form_mode = "_update"
	return render_to_response("users/read_users.html", locals(), context_instance=RequestContext(request))


@login_required()
def delete_user(request, id_user):
	_user = get_object_or_404(User, pk=id_user)
	_user.userprofile.is_active = False
	_user.userprofile.is_active_worker = False
	_user.userprofile.save()
	return HttpResponseRedirect(reverse("read_users") + "#usuario-eliminado"+ str(_user.id))


@login_required()
def create_activity(request):
	"""Form to create an activity"""
	if request.method == 'POST':
		form  = ActivityForm(request.POST)
		if form.is_valid():
			activity = form.save(commit=False)
			activity.id_user = request.user
			activity.save()
			form = ActivityForm()
		else:
				show_form = True
		if '_createanother' in request.POST:
			show_form = True
	else:
		form  = ActivityForm() 
	form_mode  = "_create"
	activities = Activities.objects.get_active()
	return render_to_response('create_activity.html', locals(), context_instance=RequestContext(request))


@login_required()
def update_activity(request, id_activity):
	"""Manage activities"""
	act = get_object_or_404(Activities, pk = id_activity)
	if request.method == "POST":
		form = ActivityForm(request.POST, instance=act)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse(create_activity))
		else:
			show_form = True
	else:
		show_form = True
		form = ActivityForm(instance=act)
	form_mode = "_update"
	activities = Activities.objects.get_active()
	return render_to_response("create_activity.html", locals(), context_instance=RequestContext(request))


@login_required()
def delete_activity(request, id_activity):
	"""Logical deletion of activities"""
	act = get_object_or_404(Activities, pk = id_activity)
	act.is_active=False
	act.save()
	return HttpResponseRedirect(reverse(create_activity))
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
