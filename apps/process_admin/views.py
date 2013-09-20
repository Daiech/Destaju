# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from apps.process_admin.forms import *
from apps.process_admin.models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

def home(request):
	return HttpResponse("Welcome")

@login_required(login_url='/account/login')
def create_activity(request):
	"""Form to create an activity"""
	if request.method == 'POST':
		form  = ActivityForm(request.POST)
		if form.is_valid():
			activity = form.save(commit=False)
			activity.id_user = request.user
			activity.save()
			form = ActivityForm()
		show_form = True
	else:
		form  = ActivityForm() 
	activities = Activities.objects.get_active()
	return render_to_response('create_activity.html', locals(), context_instance=RequestContext(request))

def update_activity(request, id_activity):
	"""Form to edit an activity"""
	act = Activities.objects.get(pk = id_activity)
	if request.method == "POST":
		form = ActivityForm(request.POST, instance=act)
		if form.is_valid():
			form.save()
		else:
			show_form = True
	else:
		show_form = True
		if act:
			form = ActivityForm(instance=act)
		else:
			return HttpResponseRedirect("/administracion/listar_actividades/#error")
	activities = Activities.objects.get_active()
	return render_to_response("create_activity.html", locals(), context_instance=RequestContext(request))
