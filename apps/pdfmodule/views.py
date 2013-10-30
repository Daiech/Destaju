# encoding:utf-8
from django.http import HttpResponseRedirect, HttpResponse
import random
from django.conf import settings
from xhtml2pdf.pisa import CreatePDF, startViewer
from apps.actions_log.views import saveActionLog, saveViewsLog
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from apps.production_orders.models import ProductionOrder
from apps.payroll.models import DiscountsApplied, IncreasesApplied


def htmlToPdf(html_string, pdf_name):
    from django.template.defaultfilters import slugify
    import datetime
    pdf_address = "pdf/%s_%s_%s.pdf" % (
                    slugify(pdf_name),
                    slugify(settings.PROJECT_NAME),
                    datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
                    )
    file_dir = "%s/%s" % (settings.MEDIA_ROOT, pdf_address)
    file_dir = file(file_dir, "wb")
    pdf = CreatePDF(html_string, file_dir)
                    #, default_css="#minute{margin:200px}")
    if not pdf.err:
        startViewer(pdf_name)
    file_dir.close()
    return '%s%s' % (settings.MEDIA_URL, pdf_address)


def generate_xls(filename, fields, values_list):
    from export_xls.views import export_xlwt
    return export_xlwt(filename, fields, values_list, save=True, folder="xls/")


@login_required()
@require_POST
def html_to_pdf(request):
    try:
        html_data = request.POST.get('html-data')
        pdf_name = request.POST.get('pdf_name')
        pdf_address = htmlToPdf(html_data, pdf_name)
        
        #vars for django-export-xls
        filename = ""
        fields = ["user", "activity", "place", "status", "modifications", "comments"]
        values_list = ProductionOrder.objects.filter(status=3).values_list(*fields)

        xls_address = generate_xls(filename, fields, values_list)
        #relate xls_address, with pdf_address and payroll
        empty payroll
        ProductionOrder.objects.filter(status=3).update(status=4)
        DiscountsApplied.objects.filter(is_active=True).update(is_active=False)
        IncreasesApplied.objects.filter(is_active=True).update(is_active=False)

        return HttpResponseRedirect(pdf_address)
    except Exception, e:
        print e
        # raise Exception
        return HttpResponse(e)
