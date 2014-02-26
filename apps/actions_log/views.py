#encoding:utf-8
from django.contrib.auth.decorators import login_required
from apps.actions_log.models import actions, rel_user_action, UpdateTables
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from pymongo import MongoClient, DESCENDING as pymongo_DESCENDING
from django.forms.models import model_to_dict
from django.db.models.query import QuerySet
from apps.account.decorators import access_required
#from django.core.mail import EmailMessage

import datetime
import sys
#@login_required(login_url='/account/login')

def saveActionLog(id_user, code, extra, ip_address):
    try:
        action = actions.objects.get(code=code)
        log = rel_user_action(id_user=id_user, id_action=action, extra=extra, ip_address=ip_address)
        log.save()
        return True
    except rel_user_action.DoesNotExist, e:
        print "Error al registrar accion: %s" % e
        return False
    except actions.DoesNotExist, e:
        print "Error al registrar accion: %s" % e
        return False
    except Exception, e:
        print "Error al registrar accion: %s" % e
        return False


@login_required()
def showActions(request):
    saveViewsLog(request,'actions_log.views.showActions')
    if request.user.is_staff:
        saveErrorLog('(%s) ingreso al actionlog' % request.user.username)
        ctx = {"actions": rel_user_action.objects.all().order_by("-date_done")}
        return render_to_response('actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required()
def showAction(request, id_action):
    saveViewsLog(request,'actions_log.views.showAction')
    if request.user.is_staff:
        ctx = {"actions": rel_user_action.objects.filter(id_action=id_action).order_by("-date_done")}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required()
def showUserActions(request, username):
    saveViewsLog(request,'actions_log.views.showUserActions')
    if request.user.is_staff:
        user = User.objects.get(username=username)
        ctx = {"actions": rel_user_action.objects.filter(id_user=user).order_by("-date_done")}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required()
def showOrderActions(request, field):
    saveViewsLog(request,'actions_log.views.showOrderActions')
    if request.user.is_staff:
        ctx = {"actions": rel_user_action.objects.filter().order_by("-%s" % (field))}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


@login_required()
def showUserActionsOrder(request, username, field):
    saveViewsLog(request,'actions_log.views.showUserActionsOrder')
    if request.user.is_staff:
        if username == "ALL":
            action = rel_user_action.objects.filter().order_by("-%s" % (field))
        else:
            user = User.objects.get(username=username)
            action = rel_user_action.objects.filter(id_user=user).order_by("-%s" % (field))
        ctx = {"actions": action}
        return render_to_response('actions/actions.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def saveErrorLog(errordata):
    try:
        logfile = open("error.log", "a")
        try:
            logfile.write('%s %s \n'%(datetime.datetime.now(),errordata))
        finally:
            logfile.close()
    except IOError:
        pass
    

def saveViewsLog(request,page):
    try:
        connection = MongoClient('localhost',27017)
        db = connection.actarium
        views = db.views
        try:
            if request.user.is_authenticated():
                id_user = request.user.pk
                username = request.user.username
            else:
                id_user = 0
                username = "Anonymous User"
            data = {
                    'id_user':id_user,
                    'username':username,
                    'page': page,
                    'date': datetime.datetime.now(),
                    'ip': request.META['REMOTE_ADDR']
                    }
            views.insert(data)
        except:
            print "Error: %s"%(sys.exc_info()[0])
        
        return True
    except:
        saveErrorLog("Error: conexion a MongoDB")
        print "Error saveViewsLog"
        return False


@login_required()
def showViewsLog(request):
    saveViewsLog(request,'actions_log.views.showViewsLog')
    if request.user.is_staff:
        try:
            connection = MongoClient('localhost',27017)
            db = connection.actarium
            views = db.views
            try: 
                if request.method == "GET":
                    u = str(request.GET['u'])
                    count = views_data = views.find({'username':u}).count()
                    views_data = views.find({'username':u}).sort([("date", pymongo_DESCENDING)])
            except:
                count = views.find().count()
                views_data = views.find().sort([("date", pymongo_DESCENDING)])
            ctx = {"views": views_data, "count": count}
        except:
            ctx = {"views": [], 'count': 0}
        return render_to_response('actions/views.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')


def showViewsStats(request):
    saveViewsLog(request,'actions_log.views.showViewsStats')
    if request.user.is_staff:
        try:
            connection = MongoClient('localhost',27017)
            db = connection.actarium
            from bson.code import Code
            _map = Code("function () {"
                    "var key = this.page;"
                    "var values = {'id':key, count: 1 };"
                    "    emit(key,values);"
                   "}")
            _reduce = Code("function (key, values) {"
                       "  var reducedValue = {'id':key,'count':0};"
                       "  for (var i = 0; i < values.length; i++) {"
                       "    reducedValue['count'] += parseInt(values[i].count);"
                       "  }"
                       "  return reducedValue;"
                      "}")
            result_views = db.views.map_reduce(_map, _reduce, "result_views")
            mr = result_views.find()
            data = []
            for i in mr:
                data.append(i)
            ctx = {"views": data}
        except:
            ctx = {"views": []}
        return render_to_response('actions/views_stats.html', ctx, context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/')    


@login_required()
@access_required("superadmin", "admin", "consultor")
def read_modifications(request):
    """read the modifications"""
    object_list = UpdateTables.objects.all()
    return render_to_response('modifications.html', locals(), context_instance=RequestContext(request))
    

def save_editinline_modifications(model, field_name, obj, last_data, user):
    update_table_obj = UpdateTables(user=user, 
                        table_name = obj.get_table_name(), 
                        record_pk = obj.pk, 
                        field = field_name,
                        modification_number = obj.modifications + 1, 
                        last_data = last_data,
                        new_data = obj.__getattribute__(field_name)
                            )
    update_table_obj.save()
    obj.modifications = obj.modifications + 1
    obj.save()


def save_with_modifications(user,form,form_obj,model):
    "This method save_simple and 2m2 the data from form and save a record with the data modified"
    obj = model.objects.get(pk=form_obj.pk)
    form_cleaned = form.cleaned_data 
    table_name = obj.get_table_name()
    pk_obj = obj.pk
    object_list = []

    for f in form_cleaned.keys():
        if type(form_cleaned[f]) == QuerySet:
            if list(form_cleaned[f]) != list(getattr(obj,f).all()):
                
                ld = "<ul>"
                for i in getattr(obj,f).all():
                    ld = ld + "<li>" +str(i) +"</li>"
                ld = ld + "</ul>"

                nd = "<ul>"
                for j in form_cleaned[f]:
                    nd = nd + "<li>" +str(j) +"</li>"
                nd = nd + "</ul>"
                update_table_obj = UpdateTables(user = user, 
                        table_name = table_name, 
                        record_pk = pk_obj, 
                        field = form[f].label,
                        modification_number = obj.modifications + 1, 
                        last_data = ld, 
                        new_data = nd
                            )
                object_list.append(update_table_obj)
        else:
            if form_cleaned[f] !=  getattr(obj,f):
                update_table_obj = UpdateTables(user = user, 
                            table_name = table_name, 
                            record_pk = pk_obj, 
                            field = form[f].label,
                            modification_number = obj.modifications + 1, 
                            last_data = getattr(obj,f), 
                            new_data = form_cleaned[f],
                            )
                object_list.append(update_table_obj)
    if object_list != []:
        UpdateTables.objects.bulk_create(object_list)
        form_obj.modifications = form_obj.modifications + 1 
        form.save()
        return True
    else:
        return False
