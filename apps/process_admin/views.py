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
def create_user(request):
	users = User.objects.all()
	return render_to_response("create_user.html", locals(), context_instance=RequestContext(request))


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
		userprofile_form  = UserProfileForm(request.POST, instance=_user)
		print request.POST
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
		userprofile_form  = UserProfileForm(instance=_user)
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
	activities_list = Activities.objects.get_active()
	return render_to_response('activities/create_activity.html', locals(), context_instance=RequestContext(request))


@login_required()
def update_activity(request, id_activity):
	"""Manage activities"""
	_activity = get_object_or_404(Activities, pk = id_activity)
	if request.method == "POST":
		form = ActivityForm(request.POST, instance=_activity)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse(create_activity))
		else:
			show_form = True
	else:
		show_form = True
		form = ActivityForm(instance=_activity)
	form_mode = "_update"
	activities_list = Activities.objects.get_active()
	return render_to_response("activities/create_activity.html", locals(), context_instance=RequestContext(request))


@login_required()
def delete_activity(request, id_activity):
	"""Logical deletion of activities"""
	_activity = get_object_or_404(Activities, pk = id_activity)
	_activity.is_active=False
	_activity.save()
	return HttpResponseRedirect(reverse(create_activity))
	
@login_required()
def create_legal_discounts(request):
	"""Form to create legal discounts"""
	if request.method == 'POST':
		form  = LegalDiscountForm(request.POST)
		if form.is_valid():
			legal_discount = form.save(commit=False)
			legal_discount.id_user = request.user
			legal_discount.save()
			form = LegalDiscountForm()
		else:
				show_form = True
		if '_createanother' in request.POST:
			show_form = True
	else:
		form  = LegalDiscountForm() 
	form_mode  = "_create"
	legal_discounts_list = LegalDiscounts.objects.get_active()
	return render_to_response('discounts/legal_discounts.html', locals(), context_instance=RequestContext(request))


@login_required()
def update_legal_discount(request, id_legal_discount):
	"""Manage legal discounts"""
	_legal_discount = get_object_or_404(LegalDiscounts, pk = id_legal_discount)
	if request.method == "POST":
		form = LegalDiscountForm(request.POST, instance=_legal_discount)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse(create_legal_discounts))
		else:
			show_form = True
	else:
		show_form = True
		form = LegalDiscountForm(instance=_legal_discount)
	form_mode = "_update"
	legal_discounts_list = LegalDiscounts.objects.get_active()
	return render_to_response("discounts/legal_discounts.html", locals(), context_instance=RequestContext(request))


@login_required()
def delete_legal_discount(request, id_legal_discount):
	"""Logical deletion of legal discounts"""
	_legal_discount = get_object_or_404(LegalDiscounts, pk = id_legal_discount)
	_legal_discount.is_active=False
	_legal_discount.save()
	return HttpResponseRedirect(reverse(create_legal_discounts))


@login_required()
def create_general_discounts(request):
	"""Form to create general discounts"""
	if request.method == 'POST':
		form  = GeneralDiscountForm(request.POST)
		if form.is_valid():
			general_discount = form.save(commit=False)
			general_discount.id_user = request.user
			try:
				general_discount.save()
				print "es valido"
			except:
				print "error guardando"
			form = GeneralDiscountForm()
		else:
				show_form = True
		if '_createanother' in request.POST:
			show_form = True
	else:
		form  = GeneralDiscountForm() 
	form_mode  = "_create"
	general_discounts_list = GeneralDiscounts.objects.get_active()
	return render_to_response('discounts/general_discounts.html', locals(), context_instance=RequestContext(request))


@login_required()
def update_general_discount(request, id_general_discount):
	"""Manage general discounts"""
	_general_discount = get_object_or_404(GeneralDiscounts, pk = id_general_discount)
	if request.method == "POST":
		form = GeneralDiscountForm(request.POST, instance=_general_discount)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse(create_general_discounts))
		else:
			show_form = True
	else:
		show_form = True
		form = GeneralDiscountForm(instance=_general_discount)
	form_mode = "_update"
	general_discounts_list = GeneralDiscounts.objects.get_active()
	return render_to_response("discounts/general_discounts.html", locals(), context_instance=RequestContext(request))


@login_required()
def delete_general_discount(request, id_general_discount):
	"""Logical deletion of general discounts"""
	_general_discount = get_object_or_404(GeneralDiscounts, pk = id_general_discount)
	_general_discount.is_active=False
	_general_discount.save()
	return HttpResponseRedirect(reverse(create_general_discounts))
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
