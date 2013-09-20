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

@login_required()
def read_users(request):
	is_active_worker = True
	if request.method == "GET" and 'workers' in request.GET:
		try:
			w = int(request.GET.get("workers"))
		except Exception:
			w = 1
		is_active_worker = bool(w)
	users = User.objects.filter(userprofile__is_active_worker=is_active_worker, userprofile__is_active=True)
	return render_to_response("users/read_users.html", locals(), context_instance=RequestContext(request))


@login_required()
def create_user(request):
	users = User.objects.all()
	return render_to_response("create_user.html", locals(), context_instance=RequestContext(request))


@login_required()
def read_user(request, id_user):
	users = User.objects.all()
	return render_to_response("read_user.html", locals(), context_instance=RequestContext(request))


@login_required()
def update_user(request, id_user):
	users = User.objects.all()
	return render_to_response("update_user.html", locals(), context_instance=RequestContext(request))


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
		if '_addanother' in request.POST:
			show_form = True
	else:
		form  = ActivityForm() 
	form_mode  = "_save"
	activities = Activities.objects.get_active()
	return render_to_response('create_activity.html', locals(), context_instance=RequestContext(request))

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
	form_mode = "_edit"
	activities = Activities.objects.get_active()
	return render_to_response("create_activity.html", locals(), context_instance=RequestContext(request))
