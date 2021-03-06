#encoding:utf-8
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse

from django.template import RequestContext  # para hacer funcionar {% csrf_token %}

#Django Auth
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_complete, password_reset_confirm

import json
from django.contrib.auth.models import User
from hashlib import sha256 as sha_constructor
import random
from django.core.urlresolvers import reverse

from apps.account.forms import RegisterForm
from apps.account.decorators import access_required
from apps.account.templatetags.gravatartag import showgravatar
try:
    from apps.actions_log.views import *
except Exception, e:
    print "-------------------apps.actions_log Exception:", e
try:
    from apps.emailmodule.views import sendEmailHtml
except Exception, e:
    print "-------------------apps.emailmodule Exception:", e


#------------------------------- <Normal User>---------------------------
def getActivationKey(email_user):
    return sha_constructor(sha_constructor(str(random.random())).hexdigest()[:5] + email_user).hexdigest()


def getNextUsername(username):
    """
    the entry username is already exists.
    then, search a new username.
    """
    num = username.split("_")[-1]
    if num.isdigit():
        num = int(num) + 1
        username = "_".join(username.split("_")[:-1]) + "_" + str(num)
    else:
        username = username + "_1"
    try:
        User.objects.get(username=username)
        return getNextUsername(username)
    except User.DoesNotExist:
        return username


def validateUsername(username):
    try:
        User.objects.get(username=username)
        return getNextUsername(username)
    except User.DoesNotExist:
        from django.template.defaultfilters import slugify
        return slugify(username)


def log_in(request):
    '''
        Inicia session de un usuario que usa el formulario propio del sistema.
        Retorna y crea una sesion de usuario
    '''
    saveViewsLog(request, "apps.account.views.log_in")
    if not request.user.is_anonymous():
        return HttpResponseRedirect(reverse('personal_data'))
    if request.method == 'POST':
        formulario = AuthenticationForm(data=request.POST)
        if formulario.is_valid():
            return userLogin(request, request.POST['username'], request.POST['password'])
    else:
        formulario = AuthenticationForm()
    return render_to_response('login.html', {'formulario': formulario}, context_instance=RequestContext(request))


@login_required()
def log_out(request):
    '''
        Finaliza una sesion activa
    '''
    saveViewsLog(request, "apps.account.views.log_out")
    try:
        _user = request.user
        saveActionLog(_user,  "LOG_OUT", "username: %s" % (_user.username), request.META['REMOTE_ADDR'])  # Guarda la accion de cerrar sesion
        logout(request)
    except Exception, e:
        print e
    return HttpResponseRedirect('/')


def userLogin(request, user_name, password):
    '''
        Autentica a un usuario con los parametros recibidos
        actualmente solo se loguea con username, se espera autenticar con mail
    '''
    saveViewsLog(request, "apps.account.views.userLogin")
    try:
        next = request.GET['next']
    except Exception:
        next = '/'

    acceso = authenticate(username=user_name, password=password)
    if acceso is not None:
        if acceso.is_active:
            login(request, acceso)
            try:
                user_id = User.objects.get(username=user_name)
            except:
                user_id = User.objects.get(email=user_name)
            saveActionLog(user_id, "LOG_IN", "username: %s" % (user_name), request.META['REMOTE_ADDR'])  # Guarda la accion de inicar sesion
            return HttpResponseRedirect(next)
        else:
            return render_to_response('noactivo.html', context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect(reverse('log_in') + '?next=' + next)


def set_activation_key(user):
    try:
        from .models import activation_keys
        ak_obj = activation_keys(id_user=user, email=user.email, activation_key=getActivationKey(user.email))
        ak_obj.save()
        return ak_obj
    except Exception, e:
        print "Error in activation_keys:", e
        return False

#------------------------------- </Normal User>---------------------------


#--------------------------------<Cuenta de Usuario>----------------------
def get_userprofile_form(request, is_POST=False):
    try:
        up = request.user.userprofile
    except Exception, e:
        up = None
    from apps.process_admin.forms import UserProfileForm
    if up:
        if is_POST:
            return UserProfileForm(request.POST, instance=request.user.userprofile)
        else:
            return UserProfileForm(instance=request.user.userprofile)
    else:
        if is_POST:
            return UserProfileForm(request.POST)
        else:
            return UserProfileForm()


@login_required()
def personal_data(request):
    return render_to_response('personal_data.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin")
def update_personal_data(request):
    '''Control para usuarios logueados.
        se consultan los datos y se los envia al template para imprimirlos'''
    saveViewsLog(request, "apps.account.views.personalData")
    last_data = "last=> username: %s, name: %s, last_name: %s, email %s" % (request.user.username, request.user.first_name, request.user.last_name, request.user.email)
    from apps.account.forms import UserForm
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        userprofile_form  = get_userprofile_form(request, is_POST=True)
        u = user_form.is_valid()
        up = userprofile_form.is_valid()
        if u and up:
            _user = user_form.save()
            _up = userprofile_form.save(commit=False)
            _up.user = _user
            _up.save()
            saveActionLog(request.user, "CHG_USDATA", last_data, request.META['REMOTE_ADDR'])  # Guarda datos de usuarios antes de modificarse
            update = True
            user_form = False  # don't show the form
        else:
            update = False
    else:
        user_form = UserForm(instance=request.user)
        userprofile_form = get_userprofile_form(request)
        update = False
    return render_to_response('personal_data.html', locals(), context_instance=RequestContext(request))


@login_required()
def changePassword(request):
    '''
        Opcion para cambiar password
    '''
    saveViewsLog(request, "account.views.savePassword")
    passUpdate = False
    if request.method == "POST":
        passUpdate = False
        passForm = PasswordChangeForm(data=request.POST, user=request.user)
        if passForm.is_valid():
            passForm.save()
            saveActionLog(request.user, "CHG_PASS", "Password changed", request.META['REMOTE_ADDR'])  # Guarda datos de usuarios antes de modificarse
            passUpdate = True
    else:
        passForm = PasswordChangeForm(user=request.user)
        passUpdate = False
    ctx = {"passForm": passForm, "dataUpdate": False, "passwordUpdate": passUpdate, "error_email": False}
    return render_to_response('password.html', ctx, context_instance=RequestContext(request))

# --------------------------------</Cuenta de Usuario>----------------------

# --------------------------------<Recuperacion de contrasena>----------------------


def password_reset2(request):
        """
        django.contrib.auth.views.password_reset view (forgotten password)
        """
        saveViewsLog(request, "account.views.password_reset2")
        if not request.user.is_authenticated():
            # print "entro a password_reset2"
            try:
                return password_reset(request, template_name='password_reset_form.html', email_template_name='password_reset_email.html', subject_template_name='password_reset_subject.txt', post_reset_redirect=reverse("password_reset_done2"))
            except Exception:
                return HttpResponseRedirect(reverse("password_reset_done2"))
        else:
            # print "no entro a password_reset2"
            return HttpResponseRedirect(reverse("personal_data"))


def password_reset_done2(request):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        saveViewsLog(request, "account.views.password_reset_done2")
        if not request.user.is_authenticated():
            return password_reset_done(request, template_name='password_reset_done.html')
        else:
            return HttpResponseRedirect(reverse("personal_data"))


def password_reset_confirm2(request, uidb36, token):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        saveViewsLog(request, "account.views.password_reset_confirm2")
        if not request.user.is_authenticated():
                # print "entro a password_reset_confirm2"
                return password_reset_confirm(request, uidb36, token, template_name='password_reset_confirm.html', post_reset_redirect=reverse("password_reset_done2"))
        else:
                # print "no entro a password_reset_confirm2"
                return HttpResponseRedirect(reverse("personal_data"))


def password_reset_complete2(request):
        """
        django.contrib.auth.views.password_reset_done - after password reset view
        """
        saveViewsLog(request, "account.views.password_reset_complete2")
        if not request.user.is_authenticated():
                # print "entro a password_reset_complete2"
                return password_reset_complete(request, template_name='password_reset_complete.html')
        else:
                # print "no entro a password_reset_complete2"
                return HttpResponseRedirect(reverse("personal_data"))

# --------------------------------</Recuperacion de contrasena>----------------------

# ---------------------------------<activacion de cuenta>----------------------------


def activationKeyIsValid(activation_key):
    from apps.account.models import activation_keys
    try:
        return activation_keys.objects.get(activation_key=activation_key, is_expired=False)
    except activation_keys.DoesNotExist:
        return False
    except Exception:
        return False


def confirm_account(request, activation_key, is_invited=False):
    saveViewsLog(request, "account.views.confirm_account")
    ak = activationKeyIsValid(activation_key)
    if ak:
        return HttpResponseRedirect(reverse("activate_account", args=(activation_key,)) + "?is_invited=1")
    else:
        return render_to_response('invalid_link.html', {}, context_instance=RequestContext(request))


def activate_account(request, activation_key):
    saveViewsLog(request, "account.views.activate_account")
    if activate_account_now(request, activation_key):
        is_invited = request.GET.get('is_invited') if "is_invited" in request.GET and request.GET.get("is_invited") != "" else False
        return render_to_response('account_actived.html', {"invited": is_invited}, context_instance=RequestContext(request))
    else:
        return render_to_response('invalid_link.html', {}, context_instance=RequestContext(request))


def activate_account_now(request, activation_key):
    saveViewsLog(request, "account.views.activate_account_now")
    from .models import activation_keys
    try:
        activation_obj = activation_keys.objects.get(activation_key=activation_key)
        if not activation_obj.is_expired:
            user = User.objects.get(id=activation_obj.id_user.pk)
            user.is_active = True
            user.save()
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            activation_obj.is_expired = True
            activation_obj.save()
            return True
        else:
            return False
    except activation_keys.DoesNotExist:
        return False
    except Exception:
        return False
