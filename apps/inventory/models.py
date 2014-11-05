# encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from apps.process_admin.models import Tools
from apps.production_orders.models import ProductionOrder

class GenericManager(models.Manager):

    def get_all_active(self):
        return self.filter(is_active=True).order_by('-date_modified')

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None



class Inventory(models.Model):

    tool = models.ForeignKey(Tools,  null=True, blank=True, related_name='%(class)s_tool') 
    quantity = models.FloatField(max_length=20, verbose_name="Quantity", null=False)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()
    
    def __unicode__(self):
        return "%s: %s"%(self.tool, self.quantity)

    
class ProviderOrder(models.Model):

    user_generator = models.ForeignKey(User,  null=True, blank=True, related_name='%(class)s_user_generator') 
    user_provider = models.ForeignKey(User,  null=True, blank=True, related_name='%(class)s_user_provider') 
    user_approver = models.ForeignKey(User,  null=True, blank=True, related_name='%(class)s_user_approved') 
    invoice_number = models.CharField(max_length=50, verbose_name="Invoice number", blank=True, null=True)
    details = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)
    date_approved = models.DateTimeField()

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()
    
    def __unicode__(self):
        return "[%s] - %s"%(self.invoice_number, self.user_generator)


class EmployedOrder(models.Model):

    TYPE_CHOICES =( ('Recovery','Entrada'),    ('Output','Ingreso'))

    user_approver = models.ForeignKey(User,  null=True, blank=True, related_name='%(class)s_user_approver') 
    user_generator = models.ForeignKey(User,  null=True, blank=True, related_name='%(class)s_user_generator') 
    production_order = models.ForeignKey(ProductionOrder,  null=True, blank=True, related_name='%(class)s_production_order') 
    type_order = models.CharField(max_length=15, choices=TYPE_CHOICES)
    details = models.TextField(blank=True, null=True)
    is_approved = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()
    
    def __unicode__(self):
        return "%s %s"%(self.user_generator, self.type_order)
    

class QuantityProviderTool(models.Model):

    tool = models.ForeignKey(Tools,  null=True, blank=True, related_name='%(class)s_tool') 
    quantity = models.FloatField(max_length=20, verbose_name="Quantity", null=False)
    unit_value = models.FloatField(max_length=30, verbose_name="Unit value", null=False)
    provider_order = models.ForeignKey(ProviderOrder,  null=True, blank=True, related_name='%(class)s_provider_order') 

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()
    
    def __unicode__(self):
        return "%s: %s"%(self.tool, self.quantity)
    
    
class QuantityEmployedTool(models.Model):

    tool = models.ForeignKey(Tools,  null=True, blank=True, related_name='%(class)s_tool') 
    quantity = models.FloatField(max_length=20, verbose_name="Quantity", null=False)
    employed_order = models.ForeignKey(EmployedOrder,  null=True, blank=True, related_name='%(class)s_employed_order') 

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()
    
    def __unicode__(self):
        return "%s: %s"%(self.tool, self.quantity)
    
