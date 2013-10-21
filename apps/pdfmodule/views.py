# encoding:utf-8
from django.http import HttpResponseRedirect, HttpResponse
import random
from django.conf import settings
from xhtml2pdf.pisa import CreatePDF, startViewer
from apps.actions_log.views import saveActionLog, saveViewsLog
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# from reportlab.platypus import Table
# from reportlab.platypus import Paragraph
# from reportlab.platypus import Image
# from reportlab.platypus import Spacer
# from reportlab.lib.styles import getSampleStyleSheet
# from reportlab.platypus import Frame


def htmlToPdf(html_string, pdf_name):
    from django.template.defaultfilters import slugify
    pdf_address = "pdf/%s_%s_%s.pdf" % (
                    slugify(pdf_name),
                    slugify(settings.PROJECT_NAME),
                    int(random.random() * 100000)
                    )
    file_dir = "%s/%s" % (settings.MEDIA_ROOT, pdf_address)
    file_dir = file(file_dir, "wb")
    pdf = CreatePDF(html_string, file_dir)
                    #, default_css="#minute{margin:200px}")
    if not pdf.err:
        startViewer(pdf_name)
    file_dir.close()
    return '%s%s' % (settings.MEDIA_URL, pdf_address)


@login_required()
@require_POST
def html_to_pdf(request):
    try:
        html_data = request.POST.get('html-data')
        pdf_name = request.POST.get('pdf_name')
        pdf_address = htmlToPdf(html_data, pdf_name)
        return HttpResponseRedirect(pdf_address)
    except Exception, e:
        print e
        # raise Exception
        return HttpResponse(e)