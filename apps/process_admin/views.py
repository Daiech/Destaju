# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse


def home(request):
	return HttpResponse("Welcome")