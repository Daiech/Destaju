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
import json


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

    try:
        smtp = settings.GMAIL_USER and settings.GMAIL_USER_PASS
    except NameError:
        smtp = None
    if smtp:
        try:
            sendGmailEmail(to, subject, html_content)
        except Exception, e:
            print "Exception sendGmailEmail", e
            saveErrorLog('Ha ocurrido un error al intentar enviar un correo de tipo %s a %s' % (email_type, to))
    else:
        msg = EmailMultiAlternatives(subject, text_content, from_email, to)
        msg.attach_alternative(html_content, "text/html")
        try:
            msg.send()
        except Exception, e:
            print e
            print "Error al enviar correo electronico tipo: ", email_type, " con plantilla HTML."
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


import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText


def sendGmailEmail(to, subject, text, attach=False):
    gmail_user = settings.GMAIL_USER
    gmail_pwd = settings.GMAIL_USER_PASS
    msg = MIMEMultipart()

    msg['From'] = gmail_user
    msg['To'] = ",".join(to)
    msg['Subject'] = subject

    msg.attach(MIMEText(text, "html"))

    if attach:
        from email import Encoders
        from email.MIMEBase import MIMEBase
        import os
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(open(attach, 'rb').read())
        Encoders.encode_base64(part)
        part.add_header('Content-Disposition',
               'attachment; filename="%s"' % os.path.basename(attach))
        msg.attach(part)

    mailServer = smtplib.SMTP("smtp.gmail.com", 587)
    mailServer.ehlo()
    mailServer.starttls()
    mailServer.ehlo()
    mailServer.login(gmail_user, gmail_pwd)
    mailServer.sendmail(gmail_user, to, msg.as_string())
    # Should be mailServer.quit(), but that crashes...
    mailServer.close()