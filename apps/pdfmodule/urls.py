from django.conf.urls import url, patterns
pdfmodule_urls = patterns('apps.pdfmodule.views',
    url(r'^htmltopdf$', 'html_to_pdf', name='html_to_pdf'),
)
