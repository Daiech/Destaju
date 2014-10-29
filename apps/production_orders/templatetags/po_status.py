#encoding:utf-8
from django.template import Library


register = Library()


@register.filter
def po_status_text(obj):
    ops = "---"
    if obj.status == 1:
        ops = "Generada"
    elif obj.status == 2:
        ops = "llena"
    elif obj.status == 3:
        if obj.qualificationproord.is_qualified :
            ops = "Calificada"
        else: 
            ops = "No calificada"

        ops = ops+" - "

        if obj.qualificationproord.is_verified:
            if obj.qualificationproord.status == 1:
                ops = ops+"Aprobada"
            elif obj.qualificationproord.status == 2:
                ops = ops+"No Aprobada"
        else: 
            ops = ops+"No verificada"

    elif obj.status == 4 and obj.qualificationproord.is_verified and obj.qualificationproord.status == 1:
        ops = u"En nómina"
    elif obj.status == 4 and obj.qualificationproord.is_verified and obj.qualificationproord.status == 2:
        ops = "Rechazada"
    else: 
        ops = "ERROR"

    return ops

@register.filter
def po_status_icon(obj):
    ops = "-"
    if obj.status == 1:
        ops = '<span title="Orden generada aun no se ha llenado" class="glyphicon glyphicon-unchecked" ></span>'
    elif obj.status == 2:
        ops = '<span title="Orden llena,aun no se ha calificado" class="glyphicon glyphicon-stop" ></span>'
    elif obj.status == 3:
        if obj.qualificationproord.is_qualified :
            ops = '<span title="Orden calificada y aprobada" class="glyphicon glyphicon-ok-circle" ></span>'
        else: 
            ops = '<span title="Calificada pero no aprobada" class="glyphicon glyphicon-remove-sign" ></span>'

        if obj.qualificationproord.is_verified:
            if obj.qualificationproord.status == 1:
                ops = ops+' <span title="Orden calificada y aprobada" class="glyphicon glyphicon-ok-circle" ></span>'
            elif obj.qualificationproord.status == 2:
                ops = ops+' <span title="Calificada pero no aprobada" class="glyphicon glyphicon-remove-sign" ></span>'
        else: 
            ops = ops+' <span title="No se ha verificado" class="glyphicon glyphicon-time" ></span>'

    elif obj.status == 4 and obj.qualificationproord.is_verified and obj.qualificationproord.status == 1:
        ops = '<span title="En n&oacute;mina" class="glyphicon glyphicon-star" ></span>'
    elif obj.status == 4 and obj.qualificationproord.is_verified and obj.qualificationproord.status == 2:
        ops = '<span title="Calificada pero no aprobada" class="glyphicon glyphicon-remove-sign" ></span>'
    else: 
        ops = '<span title="Calificada pero no aprobada" class="glyphicon glyphicon-ban-circle" ></span>'

    return ops

