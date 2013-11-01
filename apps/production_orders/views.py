# encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from apps.production_orders.forms import *
from apps.production_orders.models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
#from django.core import serializers
#from apps.actions_log.views import save_with_modifications
from apps.process_admin.models import Tools, Places, Activities
from apps.actions_log.views import save_with_modifications
# from django.forms.formsets import modelformset_factory
from django.forms.models import modelformset_factory
from apps.account.decorators import access_required
from django.db.models import Max
from django.utils import simplejson as json
from django.forms.models import model_to_dict
from django.core import serializers
from django.template.loader import render_to_string
from django.http import Http404
from django.utils import formats
from django.db.models import Max, Sum
import datetime

@login_required()
@access_required("superadmin", "admin", "s1")
def create_production_order(request):
    """Form to generate a production order"""
    if request.method == 'POST':
        form  = ProductionOrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = request.user
            obj.save()
            
            for tool in request.POST.getlist('tools'):
                obj.tools.add(tool)
                
            for user in request.POST.getlist('responsible'):
                obj.responsible.add(user)

            form.save_m2m()

            form = ProductionOrderForm()
            if '_createanother' in request.POST:
                show_form = True
            else:
                return HttpResponseRedirect(reverse(create_production_order))
        else:
            show_form = True
#        if '_createanother' in request.POST:
#            show_form = True
    else:
        form  = ProductionOrderForm() 
    form_mode  = "_create"
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [1,2])
    return render_to_response('production_order.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "s1")
def update_production_order(request, id_production_order):
    """Manage tools"""
    obj = get_object_or_404(ProductionOrder, pk=id_production_order)
    if obj.status == 1:
        if request.method == "POST":
            form = ProductionOrderForm(request.POST, instance=obj)
            if form.is_valid():
                save_with_modifications(request.user, form, obj, ProductionOrder)
                return HttpResponseRedirect(reverse(create_production_order))
            else:
                show_form = True
        else:
            show_form = True
            form = ProductionOrderForm(instance=obj)
        form_mode = "_update"
    else:
        return HttpResponseRedirect(reverse(create_production_order))
    object_list = ProductionOrder.objects.get_all_active()
    return render_to_response("production_order.html", locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "s1")
def delete_production_order(request, id_production_order):
    """Logical deletion of tools"""
    obj = get_object_or_404(ProductionOrder, pk=id_production_order)
    obj.is_active=False
    obj.save()
    return HttpResponseRedirect(reverse(create_production_order))


@login_required()
@access_required("superadmin", "admin", "s2")
def filling_pro_ord(request):
    """Show the production orders with status 1:generate and 2:fulled """
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [1,2]) \
    .annotate(last_filling=Max('fillingproord__filling_filling_pro_ord__date_modified'))
    return render_to_response('filling_pro_ord.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "s2")
def filling(request, id_production_order):
    """Form to filling a production order"""
    po = get_object_or_404(ProductionOrder, pk=id_production_order)
    if request.method == 'POST':
        if po.status == 1:
            FillingFormSet = modelformset_factory(Filling, form=FillingForm)
            formset =  FillingFormSet(request.POST)
            if formset.is_valid():
                filling_pro_ord_obj = FillingProOrd(user=request.user, production_order=po)
                filling_pro_ord_obj.save()
                form = FillingProOrdForm(request.POST, instance=filling_pro_ord_obj)
                if form.is_valid():
                    form.save()
                po.status = 2
                po.save()
                object_list = formset.save(commit=False)
                for obj in object_list:
                    obj.filling_pro_ord = filling_pro_ord_obj
                formset.save()
                return HttpResponseRedirect(reverse(filling_pro_ord))
            else:
                form = FillingProOrdForm(request.POST)
        else:
            form = FillingProOrdForm(request.POST, instance = po.fillingproord)
            if form.is_valid():
                    form.save()
            qs = Filling.objects.filter(filling_pro_ord=FillingProOrd.objects.get(production_order=po))
            FillingFormSet = modelformset_factory(Filling, form=FillingForm,  extra=0)
            formset =  FillingFormSet(request.POST, queryset=qs)
            if formset.is_valid():
                formset.save()
                return HttpResponseRedirect(reverse(filling_pro_ord))
    else:
        responsible_list = ProductionOrder.objects.get(pk=id_production_order).responsible.all()
        responsible = []
        for user in responsible_list:
            responsible.append({"user":user})
        if po.status == 1:
            form = FillingProOrdForm()
            FillingFormSet = modelformset_factory(Filling, form=FillingForm, extra=len(responsible))
            qs = Filling.objects.none()
            formset =  FillingFormSet(initial=responsible,queryset = qs)
        elif po.status == 2:
            form = FillingProOrdForm(instance = po.fillingproord)
            FillingFormSet = modelformset_factory(Filling, form=FillingForm, extra=0)
            qs = Filling.objects.filter(filling_pro_ord=FillingProOrd.objects.get(production_order=po))
            formset =  FillingFormSet(queryset = qs)
        else:
            return HttpResponseRedirect(reverse(filling_pro_ord))
        
        
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [1,2]) \
    .annotate(last_filling=Max('fillingproord__filling_filling_pro_ord__date_modified'))
    form_mode = "_update"
    show_form =True
    return render_to_response('filling_pro_ord.html', locals(), context_instance=RequestContext(request))

@login_required()
def qualification_pro_ord(request):
    """Show the production orders with status 1:generate and 2:fulled """
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [2,3]) \
    .annotate(last_filling=Max('fillingproord__filling_filling_pro_ord__date_modified'))
    return render_to_response('qualification_pro_ord.html', locals(), context_instance=RequestContext(request))

@login_required()
def qualification(request, id_production_order):
    """Form to qualify a production order"""
    po = get_object_or_404(ProductionOrder, pk=id_production_order)
    if request.method == 'POST':
        if po.status == 2:
            form =  QualificationsForm(request.POST)
            if form.is_valid():
                obj = form.save(commit = False)
                obj.user=request.user 
                obj.production_order=po
                obj.save()
                po.status = 3
                po.save()
                return HttpResponseRedirect(reverse(qualification_pro_ord))
        elif po.status == 3:
            form =  QualificationsForm(request.POST, instance= po.qualificationproord)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse(qualification_pro_ord))
        else:
            return HttpResponseRedirect(reverse(qualification_pro_ord))
    else:
        if po.status == 2:
            form =  QualificationsForm()
        elif po.status == 3:
            form =  QualificationsForm(instance = po.qualificationproord)
        else:
            return HttpResponseRedirect(reverse(qualification_pro_ord))
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [2,3]) \
    .annotate(last_filling=Max('fillingproord__filling_filling_pro_ord__date_modified'))
    #    form_mode = "_create"
    show_form =True
    return render_to_response('qualification_form.html', locals(), context_instance=RequestContext(request))

@login_required()
def list_production_orders(request):
    if request.method == 'POST':
        form = ListProductionOrderForm(request.POST)
        if form.is_valid():
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']
            type_date = form.cleaned_data['type_date']
            if type_date == 'added':
                object_list = ProductionOrder.objects.filter(date_added__gt = date_from).filter(date_added__lt = date_to).annotate(total_filling=Sum("fillingproord__filling_filling_pro_ord__value"))
            elif type_date == 'modified':
                object_list = ProductionOrder.objects.filter(date_modified__gt = date_from).filter(date_modified__lt = date_to).annotate(total_filling=Sum("fillingproord__filling_filling_pro_ord__value"))
            elif type_date == 'filling':
                object_list = ProductionOrder.objects.filter(fillingproord__date_modified__gt = date_from).filter(fillingproord__date_modified__lt = date_to).annotate(total_filling=Sum("fillingproord__filling_filling_pro_ord__value"))
            else:
                print "Error"
            if '_excel' in request.POST:
                from export_xls.views import export_xlwt
                values_list =[]
                fields=["#","cantidad"]
                for obj in object_list:
                    values_list.append((obj.pk,obj.total_filling))
                name_file = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
                print name_file
                return export_xlwt("op_"+(name_file), fields, values_list)
        else:
            disable_excel_button = True
    else:
        form = ListProductionOrderForm()
        disable_excel_button = True
    return render_to_response('list_production_orders.html', locals(), context_instance=RequestContext(request))

def get_production_order_json(pro_ord_obj):
    filling_list = Filling.objects.filter(filling_pro_ord__production_order=pro_ord_obj)
    if pro_ord_obj.status == 1:
        status="Generada"
    elif pro_ord_obj.status == 2:
        status="llena"
    elif pro_ord_obj.status == 3:
        if pro_ord_obj.qualificationproord.status == 1:
            status="Calificada y Aprobada"
        else:
            status="Calificada y No Aprobada"
    elif pro_ord_obj.status == 4:
        status="En nomina"
    else:
        "ERROR"
    responsible_list=[]
    
    for r in filling_list:
        responsible_list.append({"name": r.user.get_full_name(),"filling":r.value,"comments":r.comments})

    try:
        comments_generated = pro_ord_obj.comments
    except:
        comments_generated = ""
        
    try:
        comments_filling = pro_ord_obj.fillingproord.comments
    except:
        comments_filling = ""
        
    try:
        comments_qualified = pro_ord_obj.qualificationproord.comments
    except:
        comments_qualified = ""
        
    try:
        total_activities_obj = Filling.objects.filter(filling_pro_ord__production_order=pro_ord_obj).aggregate(total_activities=Sum('value'))
        total_activities = total_activities_obj['total_activities']
    except:
        total_activities = 0
        
    json_dict = {
        "pk": pro_ord_obj.pk,
        "status":  status,
        "activity": pro_ord_obj.activity.name,
        "place": pro_ord_obj.place.name,
        "date_added":formats.date_format(pro_ord_obj.date_added, "DATETIME_FORMAT"),
        "date_modified":formats.date_format(pro_ord_obj.date_modified, "DATETIME_FORMAT"),
        "comments":{
            "generated": comments_generated,
            "filling": comments_filling,
            "qualified": comments_qualified
        },
        "responsible": responsible_list,
        "total": total_activities
    }
    return json_dict  

@login_required()
def show_production_order_ajax(request, id_production_order):
    if request.is_ajax():
        if request.method == "GET":
            try: 
                pro_ord_obj = ProductionOrder.objects.get(pk=id_production_order)
            except:
                json_str = '{"error":"No se encuentra informacion acerca de la orden de produccion solicitada"}'
            production_order_json = get_production_order_json(pro_ord_obj)
            json_str = json.dumps(production_order_json)
        else:
            json_str = u"Peticion denegada"
        return HttpResponse(str(json_str), mimetype="application/json")
    else:
        raise Http404
        

     






















