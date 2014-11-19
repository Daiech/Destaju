# encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from apps.process_admin.models import Tools, Activities, Places
from apps.payroll.models import Payroll

class GenericManager(models.Manager):

    def get_all_active(self):
        return self.filter(is_active=True).order_by('-date_modified')

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None


class ProductionOrder(models.Model):
    """Table for generate the production order"""
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user') 
    activity = models.ForeignKey(Activities,  null=False, related_name='%(class)s_activity')
    place = models.ForeignKey(Places,  null=False, related_name='%(class)s_place')
    status = models.IntegerField(default=1, choices=((1,"Generada"),(2,"Llena"),(3,"Calificada"),(4,"En nomina")))
    is_active = models.BooleanField(default=True)
    responsible = models.ManyToManyField(User)
    tools = models.ManyToManyField(Tools, null=True, blank=True)
    modifications = models.IntegerField(default=0)
    comments = models.TextField(blank=True)
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()
    
    payroll = models.ForeignKey(Payroll,  null=True, related_name='%(class)s_payroll')
    
    def __unicode__(self):
        return "%s - %s "%(self.id, self.activity.name)
    
    def get_table_name(self):
        return u"Orden de producción"

    def get_employed_orders_output_approved(self):
        return self.employedorder_production_order.get_all_active().order_by('-date_added')

    def get_employed_orders_for_op(self):
        return self.employedorder_production_order.get_all_active().filter(status_order="Waiting",type_order="Output").order_by('-date_added')


class FillingProOrd(models.Model):
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user')
    production_order = models.OneToOneField(ProductionOrder)
    comments = models.TextField(blank=True)
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s : %s"%(self.user, self.production_order)

    
class QualificationProOrd(models.Model):
    user = models.ForeignKey(User,  null=True, blank=True, related_name='%(class)s_user') 
    user_value = models.ForeignKey(User,  null=True, blank=True, related_name='%(class)s_user_value') 
    production_order = models.OneToOneField(ProductionOrder)
    comments = models.TextField(blank=True)
    comments_value = models.TextField(blank=True)
    status = models.IntegerField(default=2,  choices=((1,"Aprobada"),(2,"No aprobada")))
    value = models.IntegerField(default=4,  choices=((1,"Malo"),(2,"Regular"),(3,"Bueno"), (4,"Muy bueno"), (5,"Excelente")))
    is_qualified = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    date_qualified = models.DateTimeField(blank=True, null=True)
    date_verified = models.DateTimeField(blank=True, null=True)

    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s : %s"%(self.user, self.production_order)


class Filling(models.Model):
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user') 
    value = models.FloatField(max_length=100, verbose_name="value", null=False)
    filling_pro_ord = models.ForeignKey(FillingProOrd,  null=False, related_name='%(class)s_filling_pro_ord')
    comments = models.TextField(blank=True)
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s - %s : %s"%(self.user, self.filling_pro_ord, self.value)
    
    def activity_value(self):
#        print "obj",self.value
#        print "Activity", self.filling_pro_ord.production_order.activity.value
#        print "Total", int(self.value) * int(self.filling_pro_ord.production_order.activity.value)
        return int(round(self.value * self.filling_pro_ord.production_order.activity.value,0))