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

    tool = models.ForeignKey(Tools, related_name='%(class)s_tool') 
    quantity = models.FloatField(max_length=20, verbose_name="Quantity", null=False)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()
    
    def __unicode__(self):
        return "%s: %s"%(self.tool, self.quantity)

    def get_unit_value(self):
        quantitiprovidertool_list = QuantityProviderTool.objects.filter(tool=self.tool, is_active=True, provider_order__status_order="Approved")
        c1 = 0
        c2 = 0
        for quantitiprovidertool_obj in quantitiprovidertool_list:
            c1 = c1+quantitiprovidertool_obj.quantity
            c2 = c2 + quantitiprovidertool_obj.quantity*quantitiprovidertool_obj.unit_value
        if c1 == 0:
            return 0
        else:
            return c2/c1

    def get_total_value(self):
        return self.get_unit_value()*self.quantity 

    
class ProviderOrder(models.Model):

    STATUS_CHOICES =( ('Waiting','En espera'), ('Approved','Aprobada'), ('Not_Approved','No aprobada'))

    user_generator = models.ForeignKey(User, related_name='%(class)s_user_generator') 
    user_provider = models.ForeignKey(User, related_name='%(class)s_user_provider') 
    user_approver = models.ForeignKey(User,  null=True, blank=True, related_name='%(class)s_user_approved') 
    invoice_number = models.CharField(max_length=50, verbose_name="Invoice number", blank=True, null=True, default='---')
    details = models.TextField(blank=True, null=True)
    status_order = models.CharField(max_length=20, choices=STATUS_CHOICES,  default='Waiting')
    date_approved = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()
    
    def __unicode__(self):
        return "%s - [%s] - %s"%(self.id, self.invoice_number, self.user_generator.get_full_name())


class EmployedOrder(models.Model):

    TYPE_CHOICES =( 
        ('Recovery','Retorno al almacen'),    
        ('Output','Salida por OP'), 
        ('Output_Stock','Salida por almacen')
    )

    STATUS_CHOICES =( 
        ('Waiting','En espera'), 
        ('Approved','Aprobada'), 
        ('Not_Approved','Rechazada'),
        ('Not_Approved_OP',u'Rechazada automaticamente por Modificación de OP'),
        ('Not_Approved_OP_Canceled',u'Rechazada automaticamente por Cancelación de OP')
    )

    user_approver = models.ForeignKey(User,  null=True, blank=True, related_name='%(class)s_user_approver') 
    user_generator = models.ForeignKey(User, related_name='%(class)s_user_generator') 
    production_order = models.ForeignKey(ProductionOrder, related_name='%(class)s_production_order') 
    type_order = models.CharField(max_length=50, choices=TYPE_CHOICES)
    details = models.TextField(blank=True, null=True)
    status_order = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Waiting')
    date_approved = models.DateTimeField(null=True, blank=True)

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()
    
    def __unicode__(self):
        return "%s - %s"%(self.id, self.user_generator.get_full_name())
    

class QuantityProviderTool(models.Model):

    tool = models.ForeignKey(Tools, related_name='%(class)s_tool') 
    quantity = models.FloatField(max_length=20, verbose_name="Quantity", null=False)
    unit_value = models.FloatField(max_length=30, verbose_name="Unit value", null=False)
    provider_order = models.ForeignKey(ProviderOrder, null=True, blank=True, related_name='%(class)s_provider_order') 

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()
    
    def __unicode__(self):
        return "%s - %s: %s"%(self.id, self.tool, self.quantity)

    

class QuantityEmployedTool(models.Model):

    tool = models.ForeignKey(Tools, related_name='%(class)s_tool') 
    quantity = models.FloatField(max_length=20, verbose_name="Quantity", null=False)
    employed_order = models.ForeignKey(EmployedOrder, related_name='%(class)s_employed_order') 

    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()
    
    def __unicode__(self):
        return "%s: %s"%(self.tool, self.quantity)
    