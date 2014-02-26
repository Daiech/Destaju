#encoding:utf-8
# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.db.models.loading import get_model
from django.conf import settings
import json
import hashlib
from apps.actions_log.views import save_editinline_modifications


def home(request):
	template = "index.html"
	if not request.user.is_anonymous():
		template = "home.html"
	return render_to_response(template, context_instance=RequestContext(request))


def server_error(request, template_name='500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context: None
    """
    return render_to_response(template_name,
        context_instance = RequestContext(request)
    )


def get_model_from_string(hash_model):
    app_name = ""
    for app in settings.EDITABLES_MODEL:
        for m in settings.EDITABLES_MODEL[app]:
            msha = hashlib.sha1(m).hexdigest()
            if msha[:10] == hash_model:
                # print "Te tengo eres el modelo %s de la app %s" % (m, app)
                hash_model = m
                app_name = app
                break
    return get_model(app_name, hash_model)


@login_required()
def ajax_edit_in_line(request):
    if request.is_ajax():
        obj = ""
        if request.method == "POST":
            try:
                obj = request.POST.dict()
                ref = obj['reference']
                obj_id = obj['obj_id']
                model = get_model_from_string(ref)
                a = model.objects.get_or_none(**{"id": obj_id})
                if a:
                    last_data = a.__getattribute__(obj['name'])
                    a.__setattr__(obj['name'], obj['data'])
                    a.save()
                    save_editinline_modifications(model, obj['name'], a, last_data, request.user)
                    obj = {"value": obj['name'] + " " + "ha sido agregado"}
                else:
                    print "Error"
            except Exception, e:
                print e
                obj = {'value': "Error", "message": u"Ocurrió un error al intentar actualizar, por favor recarga la página e intenta de nuevo"}
        return HttpResponse(json.dumps(obj), mimetype="application/json")
    else:
        raise Http404

