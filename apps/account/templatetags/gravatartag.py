from django import template
import urllib
import hashlib
from django.conf import settings
# from django.template import Context, loader

register = template.Library()

#@register.inclusion_tag('templatetags/gravatar.html')
#@register.filter(name='showgravatar')


def showgravatar(email, size):
    #default = "http://cms.myspacecdn.com/cms/Music%20Vertical/Common/Images/default_small.jpg"
    default = settings.URL_BASE + "/static/img/user_default.png"

    url = "http://www.gravatar.com/avatar.php?"
    url += urllib.urlencode({
        'gravatar_id': hashlib.md5(email).hexdigest(),
        # 'default': default,
        'size': str(size)
    })
    return url
register.filter('showgravatar', showgravatar)
    #return {'gravatar': {'url': url, 'size': size}}


#import urllib, hashlib
#from django import template
#
#
#
#register = template.Library()
#
#@register.inclusion_tag('templatetags/gravatar.html')
#def showgravatar(email, size=48):
#    default = "http://cms.myspacecdn.com/cms/Music%20Vertical/Common/Images/default_small.jpg"
#
#    url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
#    url += urllib.urlencode({'d':default, 's':str(size)})

#    return {'gravatar': {'url': url, 'size': size}}
