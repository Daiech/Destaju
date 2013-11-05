from apps.production_orders.models import *
from django.utils import formats
from django.db.models import Sum

def get_str_status(obj):
    if obj.status == 1:
        status="Generada"
    elif obj.status == 2:
        status="llena"
    elif obj.status == 3:
        if obj.qualificationproord.status == 1:
            status="Calificada y Aprobada"
        else:
            status="Calificada y No Aprobada"
    elif obj.status == 4:
        status="En nomina"
    else:
        status = "ERROR"
    return status


def get_str_qualification_pro_ord(obj):

    try:
        value = obj.qualificationproord.value
    except:
        value = 0

    if value == 1:
        str_value = "Malo"
    elif value == 2:
        str_value = "Regular"
    elif value == 3:
        str_value = "Bueno"
    elif value == 4:
        str_value = "Muy bueno"
    elif value == 5:
        str_value = "Excelente"
    else:
        str_value = "Sin Calificar"

    return str_value


def get_production_order_json(pro_ord_obj):

    filling_list = Filling.objects.filter(filling_pro_ord__production_order=pro_ord_obj)

    status = get_str_status(pro_ord_obj)

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
        total_activities = total_activities_obj['total_activities'] if total_activities_obj['total_activities'] else 0
    except:
        total_activities = 0
        

    qualification  = get_str_qualification_pro_ord(pro_ord_obj)
    

    json_dict = {
        "pk": pro_ord_obj.pk,
        "status":  status,
        "activity": pro_ord_obj.activity.name,
        "place": pro_ord_obj.place.name,
        "date_added":formats.date_format(pro_ord_obj.date_added, "DATETIME_FORMAT"),
        "date_modified":formats.date_format(pro_ord_obj.date_modified, "DATETIME_FORMAT"),
        "qualification":qualification,
        "comments":{
            "generated": comments_generated,
            "filling": comments_filling,
            "qualified": comments_qualified
        },
        "responsible": responsible_list,
        "total": total_activities
    }
    return json_dict  