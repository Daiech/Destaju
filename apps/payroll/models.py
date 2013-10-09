# encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from apps.process_admin.models import GeneralDiscounts
from django.db.models import Max, Sum, Q

class GenericManager(models.Manager):

    def get_all_active(self):
        return self.filter(is_active=True).order_by('-date_modified')

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class DiscountsAppliedManager(GenericManager):

    def get_query_set(self):
        print "Se esta ejecut Quwery"
        return super(DiscountsAppliedManager, self).get_query_set().filter(is_active=True)
    
    def filter(self):
        print "Se esta ejecut"
        return super(DiscountsAppliedManager, self).filter().filter(is_active=True)
    
    def all(self):
        print "Se esta ejecut all"
        return super(DiscountsAppliedManager, self).all().filter(is_active=True)
    
    def get(self):
        print "Se ejeccuta get"
        if self.is_active == False :
            return None
        else:
            return self
    
    def get_user_with_discounts_applied(self):
        return User.objects.filter(is_active=True) \
                .annotate(total_discounts = Sum('discountsapplied_employee__value')) \
                .annotate(date_last_discount = Max('discountsapplied_employee__date_modified')) \
                .order_by('-total_discounts')


class DiscountsApplied(models.Model):
    """Table to apply employee's discounts"""    
    admin = models.ForeignKey(User,  null=False, related_name='%(class)s_admin') 
    employee = models.ForeignKey(User,  null=False, related_name='%(class)s_employee') 
    general_discount = models.ForeignKey(GeneralDiscounts,  null=False, related_name='%(class)s_general_discounts')
    value = models.CharField(max_length=100, verbose_name="value", null=False)
    is_active = models.BooleanField(default=True)
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = DiscountsAppliedManager()
    
    
    def __unicode__(self):
        return "%s - %s - %s - %s"%(self.admin, self.employee, self.general_discount, self.value)
    
    def get_table_name(self):
        return u"Descuentos aplicados"