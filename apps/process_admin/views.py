# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from apps.process_admin.forms import *
from apps.process_admin.models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

def home(request):
	return HttpResponse("Welcome")

@login_required(login_url='/account/login')
def create_activity(request):
	"""Form to create an activity"""
	if request.method == 'POST':
		form  = ActivityForm(request.POST, request.FILES)
		if form.is_valid():
			Activities(id_user=request.user, **form.cleaned_data).save()
	else:
		form  = ActivityForm() 
	return render_to_response('create_activity.html', locals(), context_instance=RequestContext(request))