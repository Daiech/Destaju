# Create your views here.
# encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from apps.process_admin.forms import *
from apps.process_admin.models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.core import serializers
from apps.actions_log.views import save_with_modifications


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
def admin_users(request):
	from apps.account.forms import UserForm
	from apps.process_admin.forms import UserProfileForm
	if request.method == 'POST':
		user_form  = UserForm(request.POST)
		userprofile_form  = UserProfileForm(request.POST)
		u = user_form.is_valid()
		up = userprofile_form.is_valid()
		if u and up:
			_user = user_form.save()
			## add a username
			if user_form.cleaned_data['email'] != '':
				_user.username = _user.email
			else:
				from apps.account.views import validateUsername
				_user.username = validateUsername(_user.first_name)
			## add a username

			_user.save()
			_up = userprofile_form.save(commit=False)
			_up.user = _user
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
	user_obj = False
	return render_to_response("users/admin_users.html", locals(), context_instance=RequestContext(request))


@login_required()
def read_user(request, id_user):
	u = get_object_or_404(User, pk=id_user)
	return render_to_response("users/read_user.html", locals(), context_instance=RequestContext(request))


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
        # up2 = userprofile_form.is_dni_unique(_user)
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
            return HttpResponseRedirect(reverse(admin_users) + "?workers=" + str(w))
        else:
            show_form = True
    else:
        show_form = True
        user_form  = UserForm(instance=_user)
        userprofile_form  = UserProfileForm(instance=_user.userprofile)
    form_mode = "_update"
    user_obj = _user
    return render_to_response("users/admin_users.html", locals(), context_instance=RequestContext(request))


@login_required()
def delete_user(request, id_user):
	_user = get_object_or_404(User, pk=id_user)
	_user.userprofile.is_active = False
	_user.userprofile.is_active_worker = False
	_user.userprofile.save()
	return HttpResponseRedirect(reverse("admin_users") + "#usuario-eliminado"+ str(_user.id))
	

@login_required()
def admin_employments(request):
	"""admin employments"""
	if request.method == 'POST':
		form  = EmploymentsForm(request.POST)
		if form.is_valid():
			obj = form.save(commit=False)
			obj.user = request.user
			try:
				obj.save()
			except:
				form = EmploymentsForm()
		else:
			show_form = True
		if '_createanother' in request.POST:
			show_form = True
	else:
		form  = EmploymentsForm() 
	form_mode  = "_create"
	object_list = Employments.objects.filter(is_active=True)
	return render_to_response('employments/admin_employments.html', locals(), context_instance=RequestContext(request))


@login_required()
def update_employment(request, id_employment):
	"""Manage employments"""
	obj = get_object_or_404(Employments, pk=id_employment)
	if request.method == "POST":
		form = EmploymentsForm(request.POST, instance=obj)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse(admin_employments))
		else:
			show_form = True
	else:
		show_form = True
		form = EmploymentsForm(instance=obj)
	form_mode = "_update"
	object_list = Employments.objects.filter(is_active=True)
	return render_to_response("employments/admin_employments.html", locals(), context_instance=RequestContext(request))


@login_required()
def delete_employment(request, id_employment):
	"""Logical deletion of employments"""
	obj = get_object_or_404(Employments, pk=id_employment)
	obj.is_active=False
	obj.save()
	return HttpResponseRedirect(reverse(admin_employments))


@login_required()
def create_activity(request):
	"""Form to create an activity"""
	if request.method == 'POST':
		form  = ActivityForm(request.POST)
		if form.is_valid():
			activity = form.save(commit=False)
			activity.user = request.user
			activity.save()
			form = ActivityForm()
		else:
				show_form = True
		if '_createanother' in request.POST:
			show_form = True
	else:
		form  = ActivityForm() 
	form_mode  = "_create"
	activities_list = Activities.objects.get_all_active()
	return render_to_response('activities/create_activity.html', locals(), context_instance=RequestContext(request))




@login_required()
def update_activity(request, id_activity):
	"""Manage activities"""
	obj = get_object_or_404(Activities, pk=id_activity)
	if request.method == "POST":		
		form = ActivityForm(request.POST, instance=obj)
		if form.is_valid():
			save_with_modifications(request.user, form, obj, Activities)
			return HttpResponseRedirect(reverse(create_activity))
		else:
			show_form = True
	else:
		show_form = True
		form = ActivityForm(instance=obj)
	form_mode = "_update"
	activities_list = Activities.objects.get_all_active()
	return render_to_response("activities/create_activity.html", locals(), context_instance=RequestContext(request))


@login_required()
def delete_activity(request, id_activity):
	"""Logical deletion of activities"""
	_activity = get_object_or_404(Activities, pk=id_activity)
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
			legal_discount.user = request.user
			legal_discount.save()
			form = LegalDiscountForm()
		else:
				show_form = True
		if '_createanother' in request.POST:
			show_form = True
	else:
		form  = LegalDiscountForm() 
	form_mode  = "_create"
	legal_discounts_list = LegalDiscounts.objects.get_all_active()
	return render_to_response('discounts/legal_discounts.html', locals(), context_instance=RequestContext(request))


@login_required()
def update_legal_discount(request, id_legal_discount):
	"""Manage legal discounts"""
	obj = get_object_or_404(LegalDiscounts, pk=id_legal_discount)
	if request.method == "POST":
		form = LegalDiscountForm(request.POST, instance=obj)
		if form.is_valid():
			save_with_modifications(request.user, form, obj, LegalDiscounts)
			return HttpResponseRedirect(reverse(create_legal_discounts))
		else:
			show_form = True
	else:
		show_form = True
		form = LegalDiscountForm(instance=obj)
	form_mode = "_update"
	legal_discounts_list = LegalDiscounts.objects.get_all_active()
	return render_to_response("discounts/legal_discounts.html", locals(), context_instance=RequestContext(request))


@login_required()
def delete_legal_discount(request, id_legal_discount):
	"""Logical deletion of legal discounts"""
	_legal_discount = get_object_or_404(LegalDiscounts, pk=id_legal_discount)
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
			general_discount.user = request.user
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
	general_discounts_list = GeneralDiscounts.objects.get_all_active()
	return render_to_response('discounts/general_discounts.html', locals(), context_instance=RequestContext(request))


@login_required()
def update_general_discount(request, id_general_discount):
	"""Manage general discounts"""
	obj = get_object_or_404(GeneralDiscounts, pk=id_general_discount)
	if request.method == "POST":
		form = GeneralDiscountForm(request.POST, instance=obj)
		if form.is_valid():
			save_with_modifications(request.user, form, obj, GeneralDiscounts)
			return HttpResponseRedirect(reverse(create_general_discounts))
		else:
			show_form = True
	else:
		show_form = True
		form = GeneralDiscountForm(instance=obj)
	form_mode = "_update"
	general_discounts_list = GeneralDiscounts.objects.get_all_active()
	return render_to_response("discounts/general_discounts.html", locals(), context_instance=RequestContext(request))


@login_required()
def delete_general_discount(request, id_general_discount):
	"""Logical deletion of general discounts"""
	_general_discount = get_object_or_404(GeneralDiscounts, pk=id_general_discount)
	_general_discount.is_active=False
	_general_discount.save()
	return HttpResponseRedirect(reverse(create_general_discounts))


@login_required()
def create_places(request):
	"""Form to create places"""
	if request.method == 'POST':
		form  = PlacesForm(request.POST)
		if form.is_valid():
			place = form.save(commit=False)
			place.user = request.user
			try:
				place.save()
				print "es valido"
			except:
				print "error guardando"
			form = PlacesForm()
		else:
				show_form = True
		if '_createanother' in request.POST:
			show_form = True
	else:
		form  = PlacesForm() 
	form_mode  = "_create"
	places_list = Places.objects.get_all_active()
	return render_to_response('places/places.html', locals(), context_instance=RequestContext(request))


@login_required()
def update_place(request, id_place):
	"""Manage places"""
	obj = get_object_or_404(Places, pk=id_place)
	if request.method == "POST":
		form = PlacesForm(request.POST, instance=obj)
		if form.is_valid():
			save_with_modifications(request.user, form, obj, Places)
			return HttpResponseRedirect(reverse(create_places))
		else:
			show_form = True
	else:
		show_form = True
		form = PlacesForm(instance=obj)
	form_mode = "_update"
	places_list = Places.objects.get_all_active()
	return render_to_response("places/places.html", locals(), context_instance=RequestContext(request))


@login_required()
def delete_place(request, id_place):
	"""Logical deletion of places"""
	_place = get_object_or_404(Places, pk=id_place)
	_place.is_active=False
	_place.save()
	return HttpResponseRedirect(reverse(create_places))


@login_required()
def create_tools(request):
	"""Form to create tools"""
	if request.method == 'POST':
		form  = ToolsForm(request.POST)
		if form.is_valid():
			tool = form.save(commit=False)
			tool.user = request.user
			try:
				tool.save()
				print "es valido"
			except:
				print "error guardando"
			form = ToolsForm()
		else:
				show_form = True
		if '_createanother' in request.POST:
			show_form = True
	else:
		form  = ToolsForm() 
	form_mode  = "_create"
	tools_list = Tools.objects.get_all_active()
	return render_to_response('tools/tools.html', locals(), context_instance=RequestContext(request))


@login_required()
def update_tool(request, id_tool):
	"""Manage tools"""
	obj = get_object_or_404(Tools, pk=id_tool)
	if request.method == "POST":
		form = ToolsForm(request.POST, instance=obj)
		if form.is_valid():
			save_with_modifications(request.user, form, obj, Tools)
			return HttpResponseRedirect(reverse(create_tools))
		else:
			show_form = True
	else:
		show_form = True
		form = ToolsForm(instance=obj)
	form_mode = "_update"
	tools_list = Tools.objects.get_all_active()
	return render_to_response("tools/tools.html", locals(), context_instance=RequestContext(request))


@login_required()
def delete_tool(request, id_tool):
	"""Logical deletion of tools"""
	_tool = get_object_or_404(Tools, pk=id_tool)
	_tool.is_active=False
	_tool.save()
	return HttpResponseRedirect(reverse(create_tools))
