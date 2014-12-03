from apps.production_orders.models import *
from django.utils import formats
from django.db.models import Sum
from templatetags.po_status import *

def get_str_status(obj):
    return obj.get_status_display()


def get_str_qualification_pro_ord(obj):
    return obj.qualificationproord.get_value_display()


def get_production_order_json(pro_ord_obj):

    filling_list = Filling.objects.filter(filling_pro_ord__production_order=pro_ord_obj)

    # status = get_str_status(pro_ord_obj)
    # status = po_status_text(pro_ord_obj)


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
        comments_verified = pro_ord_obj.approvalproord.comments
    except:
        comments_verified = ""
        
    try:
        total_activities_obj = Filling.objects.filter(filling_pro_ord__production_order=pro_ord_obj).aggregate(total_activities=Sum('value'))
        total_activities = total_activities_obj['total_activities'] if total_activities_obj['total_activities'] else 0
    except:
        total_activities = 0

    # users
    try:
        user_generator = pro_ord_obj.user.get_full_name()
    except:
        user_generator = ""

    try:
        user_filling = pro_ord_obj.fillingproord.user.get_full_name()
    except:
        user_filling = ""    

    try:
        user_qualification = pro_ord_obj.qualificationproord.user.get_full_name()
    except:
        user_qualification = ""

    try:
        user_approval = pro_ord_obj.approvalproord.user.get_full_name()
    except:
        user_approval = ""

    
        

    # qualification  = get_str_qualification_pro_ord(pro_ord_obj)
    qualification  = pro_ord_obj.qualificationproord.get_value_display()
    verification  = pro_ord_obj.approvalproord.get_status_display()
    

    employed_orders_output_approved = []

    for employed_order in pro_ord_obj.get_employed_orders_output_approved() :
        employed_orders_output_approved.append({
            "id":employed_order.id, 
            "status_order":employed_order.get_status_order_display(),
            "type_order":employed_order.get_type_order_display(), 
            "items": [{"name": item.tool.name, "quantity": item.quantity } for item in employed_order.quantityemployedtool_employed_order.all()] 
            })


    json_dict = {
        "pk": pro_ord_obj.pk,
        "status":  pro_ord_obj.get_status_display(),
        "activity": pro_ord_obj.activity.name,
        "measuring_unit":pro_ord_obj.activity.measuring_unit,
        "place": pro_ord_obj.place.name,
        "date_added":formats.date_format(pro_ord_obj.date_added, "DATETIME_FORMAT"),
        "date_modified":formats.date_format(pro_ord_obj.date_modified, "DATETIME_FORMAT"),
        "qualification":qualification,
        "verification":verification,
        "comments":{
            "generated": comments_generated,
            "filling": comments_filling,
            "qualified": comments_qualified,
            "verified": comments_verified
        },
        "user":{
            "generator": user_generator,
            "filling": user_filling,
            "qualification":user_qualification,
            "approval": user_approval
        },
        "responsible": responsible_list,
        "total": total_activities,
        "employed_orders_output_approved": employed_orders_output_approved
    }
    return json_dict  