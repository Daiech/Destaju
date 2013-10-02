#encoding:utf-8
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context,  RequestContext
from django.contrib.auth.models import User
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from apps.emailmodule.models import *
try:
    from apps.actions_log.views import saveActionLog, saveViewsLog, saveErrorLog
except Exception, e:
    print "-------------------apps.actions_log Exception:", e
from django.utils import simplejson as json


def sendEmailHtml(email_type, ctx, to, _group=None):
    """
        Este modulo esta en proceso de construccion, por el momento se utilizara este metodo que recibe
        el tipo de correo que se envia y el contexto con las variables que se trasmitiran a cada template.
        La siguiente lista define los valores perimitidos para la variable type y su respectivo significado.
        1- Correo de validacion.                                   (Siempre es necesario)
        2- Correo de nueva reunion                                 (Depende del grupo)
        3- Correo de nueva Acta                                    (Depende del grupo)
        4- Correo de asignacion de rol                             (Depende del grupo)
        5- Correo de confirmacion de asistencia a reunion          (Depende del grupo)
        6- Correo de invitacion a un grupo                         (Por definir)
        7- Correo de invitacion a actarium                         (Siempre es necesario)
        8- Correo de notificacion de aceptacion de grupo           (Depende del grupo)
        9- Correo notificacion de feedback al staff de Actarium    (Siempre es necesario)
        10- email_resend_activate_account  (Por definir)
        11- email_group_reinvitation   (Depende del grupo)
        12- email_new_annotation   (Depende del grupo)
        13- email_new_minutes_for_approvers   (Depende del grupo)
        14- Correo de solicitud de acceso a DNI para un grupo      (Depende del grupo)
    """

    if email_type == 1:
        subject = ctx['username'] + " Bienvenido!"
        plaintext = get_template('emailtest.txt')
        htmly = get_template('email_activate_account.html')
    elif email_type == 2:
        subject = ctx['username'] + u" te invitó a " + settings.PROJECT_NAME
        plaintext = get_template('emailtest.txt')
        htmly = get_template('email_project_invitation.html')
    elif email_type == 3:
        subject = ctx['email'] + " Dejo un comentario tipo: " + ctx['type_feed'] + " en Actarium"
        plaintext = get_template('emailtest.txt')
        htmly = get_template('email_feedback_notification.html')
    elif email_type == 4:
        subject = ctx['firstname'] + " (" + ctx['username'] + ") " + u"está solicitando tu precencia en " + settings.PROJECT_NAME
        plaintext = get_template('emailtest.txt')
        htmly = get_template('email_resend_activate_account.html')
    else:
        plaintext = get_template('emailtest.txt')
        htmly = get_template('emailtest.html')
        subject, to = 'Mensaje de prueba', ['daiech@daiech.com']
    from_email = settings.FROM_EMAIL
    d = Context(ctx)
    text_content = plaintext.render(d)
    html_content = htmly.render(d)

    actives_required_list = [3, 4, 6, 14]  # This list contains the number of email_type that requires the user is active in the project
    if email_type in actives_required_list:
        to = activeFilter(to)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    try:
        msg.send()
    except:
        #        print "Error al enviar correo electronico tipo: ", email_type, " con plantilla HTML."
        saveErrorLog('Ha ocurrido un error al intentar enviar un correo de tipo %s a %s' % (email_type, to))


def activeFilter(email_list):
    new_email_list = []
    #    print '----------Active filter----------------------------------------'
    for email in email_list:
        _user = User.objects.get(email=email)
        if _user.is_active == True:
            new_email_list.append(email)
            # print 'Se ha evitado enviar correo a: ', email
    return new_email_list


@login_required(login_url='/account/login')
def emailAjax(request, slug_group):
    saveViewsLog(request, "groups.views.emailAjax")
    # if request.is_ajax():
    _email_admin_type = email_admin_type.objects.get(name='grupo')
    from groups.views import getGroupBySlug
    _group = getGroupBySlug(slug=slug_group)

    if request.method == "GET":
        try:
            id_email_type = str(request.GET['id_email_type'])
            input_status = str(request.GET['input_status'])
            if input_status == "false":
                input_status = False
            elif input_status == "true":
                input_status = True
            try:
                _email = email.objects.get(admin_type=_email_admin_type, email_type=id_email_type)
                try:
                    _email_group_permission = email_group_permissions.objects.get(id_user=request.user, id_group=_group, id_email_type=_email)
                    _email_group_permission.is_active = input_status
                    _email_group_permission.save()
                    message = {"saved": True}
                    return HttpResponse(json.dumps(message), mimetype="application/json")
                except email_group_permissions.DoesNotExist:
                    email_group_permissions(id_user=request.user, id_group=_group, id_email_type=_email, is_active=input_status).save()
                    message = {"saved": True}
                    return HttpResponse(json.dumps(message), mimetype="application/json")
                except:
                    message = False
                    return HttpResponse(message)
            except:
                message = False
                return HttpResponse(message)
        except:
            message = False
            return HttpResponse(message)
    else:
        message = False
        return HttpResponse(message)
