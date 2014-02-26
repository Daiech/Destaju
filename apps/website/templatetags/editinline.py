from django.template import Library
from django.template import Variable, VariableDoesNotExist
from django.utils.log import getLogger
from django.utils.safestring import mark_safe
import hashlib

register = Library()
logger = getLogger('django')


@register.assignment_tag(takes_context=True)
def editinline(context, context_variable):
    try:
        field_value = Variable(context_variable).resolve(context)
    except VariableDoesNotExist:
        field_value = ''
    except Exception, e:
        field_value = ''
        print "ERROR:", e
    field_name = context_variable.split('.')[-1]
    last_obj = ".".join(context_variable.split('.')[:-1])
    try:
        # context_obj = Variable(context_variable.split('.')[0]).resolve(context)
        # request = Variable('request').resolve(context)
        context_last_obj = Variable(last_obj).resolve(context)
        field = context_last_obj._meta.get_field_by_name(field_name)[0]
        
        # print "************************************************"
        # print "field_value: %s, tipo %s" % (field_value, type(field_value))
        # # print "context_obj: %s, tipo %s" % (context_obj, type(context_obj))
        # print "field_name: %s " % (field_name)
        # print "last_obj: %s " % (last_obj)
        # print "context_last_obj: %s " % (type(context_last_obj))
        if field_value==None:
            field_value=""
        reference = hashlib.sha1(field.model.__name__).hexdigest()
        return mark_safe(u"<span class='hidden'>{field_value}</span><input class='editable' value='{field_value}' data-value-saved='{field_value}' name='{field_name}' data-obj-id='{id}' data-reference='{reference}' />".format(field_value=field_value, field_name=field_name, id=context_last_obj.id, reference=reference[:10]))
    except VariableDoesNotExist:
        logger.warning("editlive: the template variable \"%s\" doesn't exists." % context_variable)
        return u''
    return field_value

# register.filter('editinline', editinline)
editinline.needs_autoescape = True