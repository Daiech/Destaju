# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse


def home(request):
	template = "index.html"
	if not request.user.is_anonymous():
		template = "home.html"
	return render_to_response(template, context_instance=RequestContext(request))