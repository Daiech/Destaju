# encoding:utf-8
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from apps.production_orders.forms import *
from apps.production_orders.models import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from apps.process_admin.models import Tools, Places, Activities
from apps.actions_log.views import save_with_modifications
from django.forms.models import modelformset_factory
from apps.account.decorators import access_required
from django.db.models import Max
from django.http import Http404
from django.db.models import Sum
import datetime
import json
from apps.production_orders.functions import *

from apps.inventory.models import Inventory, ProviderOrder, EmployedOrder, QuantityProviderTool, QuantityEmployedTool
from apps.inventory.forms import ProviderOrderForm, QuantityProviderToolForm, QuantityEmployedToolForm

@login_required()
@access_required("superadmin", "admin", "s1", "s2")
def create_production_order(request):
    """Form to generate a production order"""
    
    if request.method == 'POST':
        QuantityEmployedToolFormSet = modelformset_factory(QuantityEmployedTool, form=QuantityEmployedToolForm)
        formset =  QuantityEmployedToolFormSet(request.POST)
        form  = ProductionOrderForm(request.POST)
        if formset.is_valid():
            if form.is_valid():
                productionorder_obj = form.save(commit=False)
                productionorder_obj.user = request.user
                productionorder_obj.save()
                
                # for tool in request.POST.getlist('tools'):
                #     productionorder_obj.tools.add(tool)
                    
                for user in request.POST.getlist('responsible'):
                    productionorder_obj.responsible.add(user)

                form.save_m2m()

                # Quantity employed order
                quantityemployedtool_list = formset.save(commit=False)

                if len(quantityemployedtool_list) > 0:
                    # Employed Order
                    employedorder_obj = EmployedOrder(user_generator = request.user,  production_order=productionorder_obj, type_order='Output', status_order="Waiting", details=productionorder_obj.comments )
                    employedorder_obj.save()
                
                    for quantityemployedtool_obj in quantityemployedtool_list:
                        quantityemployedtool_obj.employed_order = employedorder_obj
                
                
                    formset.save()

                form = ProductionOrderForm()

                if '_createanother' in request.POST:
                    show_form = True
                else:
                    return HttpResponseRedirect(reverse(create_production_order))
            else:
                show_form = True
        else:
            show_form = True
    else:
        form  = ProductionOrderForm() 
        QuantityEmployedToolFormSet = modelformset_factory(QuantityEmployedTool, form=QuantityEmployedToolForm, extra=10)
        qs = QuantityEmployedTool.objects.none()
        formset =  QuantityEmployedToolFormSet(queryset = qs) # initial=responsible,
    form_mode  = "_create"
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [1,2])
    return render_to_response('production_order.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "s1", "s2")
def update_production_order(request, id_production_order):
    """Manage tools"""
    productionorder_obj = get_object_or_404(ProductionOrder, pk=id_production_order)

    if productionorder_obj.status == 1:
        if request.method == "POST":
            QuantityEmployedToolFormSet = modelformset_factory(QuantityEmployedTool, form=QuantityEmployedToolForm)
            formset =  QuantityEmployedToolFormSet(request.POST)
            form = ProductionOrderForm(request.POST, instance=productionorder_obj)
            if form.is_valid() and formset.is_valid():

                 # Quantity employed order
                quantityemployedtool_list = formset.save(commit=False)

                if len(quantityemployedtool_list) > 0:
                    # Employed Order
                    employedorder_obj = EmployedOrder(user_generator = request.user,  production_order=productionorder_obj, type_order='Output', status_order="Waiting", details=productionorder_obj.comments )
                    employedorder_obj.save()
                
                    for quantityemployedtool_obj in quantityemployedtool_list:
                        quantityemployedtool_obj.employed_order = employedorder_obj
                
                    reject_employedorder_list = EmployedOrder.objects.filter(production_order=productionorder_obj, status_order="Waiting").exclude(id=employedorder_obj.id)
                    for reject_employedorder_obj in reject_employedorder_list:
                        reject_employedorder_obj.status_order='Not_Approved_OP'
                        reject_employedorder_obj.user_approver = request.user
                        reject_employedorder_obj.date_approved = datetime.datetime.now()
                        reject_employedorder_obj.save()

                    formset.save()

                save_with_modifications(request.user, form, productionorder_obj, ProductionOrder)
                return HttpResponseRedirect(reverse(create_production_order))
            else:
                show_form = True
        else:
            QuantityEmployedToolFormSet = modelformset_factory(QuantityEmployedTool, form=QuantityEmployedToolForm, extra=10)
            employedorder_obj = EmployedOrder.objects.filter(production_order=productionorder_obj).last()



            qs = QuantityEmployedTool.objects.filter(employed_order=employedorder_obj)
            
            quantityemployedtool_list = []
            for quantityemployedtool_obj in qs:
                quantityemployedtool_list.append({'tool':quantityemployedtool_obj.tool.id,'quantity':quantityemployedtool_obj.quantity})
            
            formset =  QuantityEmployedToolFormSet(queryset = QuantityEmployedTool.objects.none(), initial=quantityemployedtool_list) # initial=responsible, queryset = qs
            show_form = True
            form = ProductionOrderForm(instance=productionorder_obj)
        form_mode = "_update"
    else:
        return HttpResponseRedirect(reverse(create_production_order))
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [1,2])
    return render_to_response("production_order.html", locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "s1", "s2")
def delete_production_order(request, id_production_order):
    """Logical deletion of tools"""
    obj = get_object_or_404(ProductionOrder, pk=id_production_order)
    obj.is_active=False
    obj.save()
    return HttpResponseRedirect(reverse(create_production_order))


def generate_pdf(request,id_production_order):
    from django.template.loader import render_to_string
    html_string = render_to_string("generate_pdf.html",{"obj":ProductionOrder.objects.get(pk=id_production_order)})
    from apps.pdfmodule.views import htmlToPdf
    return HttpResponseRedirect(htmlToPdf(html_string, "pdf"))


@login_required()
@access_required("superadmin", "admin", "s1", "s2")
def filling_pro_ord(request):
    """Show the production orders with status 1:generate and 2:fulled """
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [1,2]) \
    .annotate(last_filling=Max('fillingproord__filling_filling_pro_ord__date_modified'))
    return render_to_response('filling_pro_ord.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "s1", "s2")
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

#qualification - this acction was sepparated in 2 actions - cualifications and approval. 
@login_required()
@access_required("superadmin", "admin", "s1")
def qualification_pro_ord(request):
    """Show the production orders with status 1:generate and 2:fulled """
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [2,3]) \
    .annotate(last_filling=Max('fillingproord__filling_filling_pro_ord__date_modified'))
    return render_to_response('qualification_pro_ord.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "s1")
def qualification(request, id_production_order):
    """Form to qualify a production order"""
    po = get_object_or_404(ProductionOrder, pk=id_production_order)
    if request.method == 'POST':
        if po.status == 2:
            form =  QualificationsForm(request.POST)
            if form.is_valid():
                obj = form.save(commit = False)
                obj.user_value=request.user 
                obj.production_order=po
                obj.is_qualified = True
                obj.date_qualified = datetime.datetime.now()
                obj.save()
                po.status = 3
                po.save()
                return HttpResponseRedirect(reverse(qualification_pro_ord))
        elif po.status == 3:
            form =  QualificationsForm(request.POST, instance= po.qualificationproord)
            if form.is_valid():
                obj = form.save(commit = False)
                obj.user_value=request.user 
                obj.is_qualified = True
                obj.date_qualified = datetime.datetime.now()
                obj.save()
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
    production_order_json = get_production_order_json(po)
    return render_to_response('qualification_form.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "s1")
def approval_pro_ord(request):
    """Show the production orders with status 1:generate and 2:fulled """
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [2,3]) \
    .annotate(last_filling=Max('fillingproord__filling_filling_pro_ord__date_modified'))
    return render_to_response('approval_pro_ord.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "s1")
def approval(request, id_production_order):
    """Form to qualify a production order"""
    po = get_object_or_404(ProductionOrder, pk=id_production_order)
    if request.method == 'POST':
        if po.status == 2:
            form =  ApprovalForm(request.POST)
            if form.is_valid():
                obj = form.save(commit = False)
                obj.user=request.user 
                obj.production_order=po
                obj.is_verified = True
                obj.date_verified = datetime.datetime.now()
                obj.save()
                po.status = 3
                po.save()
                return HttpResponseRedirect(reverse(approval_pro_ord))
        elif po.status == 3:
            form =  ApprovalForm(request.POST, instance= po.qualificationproord)
            if form.is_valid():
                obj = form.save(commit = False)
                obj.is_verified = True
                obj.user=request.user 
                obj.date_verified = datetime.datetime.now()
                obj.save()
                return HttpResponseRedirect(reverse(approval_pro_ord))
        else:
            return HttpResponseRedirect(reverse(approval_pro_ord))
    else:
        if po.status == 2:
            form =  ApprovalForm()
        elif po.status == 3:
            form =  ApprovalForm(instance = po.qualificationproord)
        else:
            return HttpResponseRedirect(reverse(approval_pro_ord))
    object_list = ProductionOrder.objects.get_all_active().filter(status__in = [2,3]) \
    .annotate(last_filling=Max('fillingproord__filling_filling_pro_ord__date_modified'))
    #    form_mode = "_create"
    show_form =True
    production_order_json = get_production_order_json(po)
    return render_to_response('approval_form.html', locals(), context_instance=RequestContext(request))


@login_required()
@access_required("superadmin", "admin", "s1")
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
                fields=["#","Actividad", "Lugar", "Estado", "Fecha de creacion","Cantidad", "Calificacion"]
                for obj in object_list:
                    total_filling = obj.total_filling if obj.total_filling else 0
                    values_list.append(
                        (
                            obj.pk, 
                            obj.activity.name, 
                            obj.place.name, 
                            get_str_status(obj), 
                            str(obj.date_added.strftime('%Y-%m-%d_%H-%M')), 
                            total_filling,
                            get_str_qualification_pro_ord(obj)
                        )   
                    )
                name_file = str(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M'))
                return export_xlwt("op_"+(name_file), fields, values_list)
        else:
            disable_excel_button = True
    else:
        form = ListProductionOrderForm()
        disable_excel_button = True
    return render_to_response('list_production_orders.html', locals(), context_instance=RequestContext(request))


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
        

     






















