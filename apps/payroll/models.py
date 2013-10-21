# encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from apps.process_admin.models import GeneralDiscounts, Increases
from django.db.models import Max, Sum, Q

class MyUser(User):

    def get_total_discounts(self):
        return  DiscountsApplied.objects.get_total_discounts_by_user(self.pk)        

    def get_date_last_discount(self):
        return  DiscountsApplied.objects.get_date_last_discount_by_user(self.pk)

    def get_total_increases(self):
        return  IncreasesApplied.objects.get_total_increases_by_user(self.pk)        

    def get_date_last_increase(self):
        return  IncreasesApplied.objects.get_date_last_increase_by_user(self.pk)

    class Meta:
        proxy=True



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
        return super(DiscountsAppliedManager, self).get_query_set().filter(is_active=True)
    
    def get_total_discounts_by_user(self, id_user):
        a = DiscountsApplied.objects.filter(employee__pk=id_user, is_active=True)\
                .aggregate(total_discounts=Sum('value'))
        return a['total_discounts']

    def get_date_last_discount_by_user(self, id_user):
        a = DiscountsApplied.objects.filter(employee__pk=id_user, is_active=True)\
                .aggregate(date_last_discount=Max('date_modified'))
        return a['date_last_discount']


class IncreasesAppliedManager(GenericManager):
    
    def get_query_set(self):
        return super(IncreasesAppliedManager, self).get_query_set().filter(is_active=True)
    
    def get_total_increases_by_user(self, id_user):
        a = IncreasesApplied.objects.filter(employee__pk=id_user, is_active=True)\
                .aggregate(total_increases=Sum('value'))
        return a['total_increases']

    def get_date_last_increase_by_user(self, id_user):
        a = IncreasesApplied.objects.filter(employee__pk=id_user, is_active=True)\
                .aggregate(date_last_increase=Max('date_modified'))
        return a['date_last_increase']


class DiscountsApplied(models.Model):
    """Table to apply employee's discounts"""    
    admin = models.ForeignKey(User,  null=False, related_name='%(class)s_admin') 
    employee = models.ForeignKey(User,  null=False, related_name='%(class)s_employee') 
    general_discount = models.ForeignKey(GeneralDiscounts,  null=False, related_name='%(class)s_general_discounts')
    value = models.IntegerField(max_length=100, verbose_name="value", null=False)
    is_active = models.BooleanField(default=True)
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = DiscountsAppliedManager()
    
    
    def __unicode__(self):
        return "%s - %s - %s - %s"%(self.admin, self.employee, self.general_discount, self.value)
    
    def get_table_name(self):
        return u"Descuentos aplicados"


class IncreasesApplied(models.Model):
    """Table to apply employee's increases"""    
    admin = models.ForeignKey(User,  null=False, related_name='%(class)s_admin') 
    employee = models.ForeignKey(User,  null=False, related_name='%(class)s_employee') 
    increase = models.ForeignKey(Increases,  null=False, related_name='%(class)s_increase')
    value = models.IntegerField(max_length=100, verbose_name="value", null=False)
    is_active = models.BooleanField(default=True)
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = IncreasesAppliedManager()
    
    
    def __unicode__(self):
        return "%s - %s - %s - %s"%(self.admin, self.employee, self.increase, self.value)
    
    def get_table_name(self):
        return u"Aumentos"