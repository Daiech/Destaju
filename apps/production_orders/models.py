# encoding:utf-8
from django.db import models
from django.contrib.auth.models import User
from apps.process_admin.models import Tools, Activities, Places


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
    status = models.IntegerField(default=1, choices=((1,"Generada"),(2,"Llena"),(3,"Aprobada")))
    is_active = models.BooleanField(default=True)
    responsible = models.ManyToManyField(User)
    tools = models.ManyToManyField(Tools, null=True, blank=True)
    modifications = models.IntegerField(default=0)
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    objects = GenericManager()
    
    
    def __unicode__(self):
        return "%s - %s - %s - %s"%(self.user, self.activity, self.place, self.status)
    
    def get_table_name(self):
        return u"Orden de producción"


class FillingProOrd(models.Model):
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user')
    production_order = models.ForeignKey(ProductionOrder,  null=False, related_name='%(class)s_production_order')
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s : %s"%(self.user, self.production_order)

    
class QualificationProOrd(models.Model):
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user') 
    production_order = models.ForeignKey(ProductionOrder,  null=False, related_name='%(class)s_production_order')
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s : %s"%(self.user, self.production_order)


class Filling(models.Model):
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user') 
    value = models.CharField(max_length=100, verbose_name="value", null=False)
    filling_pro_ord = models.ForeignKey(FillingProOrd,  null=False, related_name='%(class)s_filling_pro_ord')
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s - %s : %s"%(self.user, self.filling_pro_ord, self.value)
    
    
class Qualifications(models.Model):
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_user') 
    comments = models.TextField(blank=True)
    value = models.IntegerField(default=4,  choices=((1,"Malo"),(2,"Regular"),(3,"Bueno"), (4,"Muy bueno"), (5,"Excelente")))
    qualification_pro_ord = models.ForeignKey(QualificationProOrd,  null=False, related_name='%(class)s_qualification_pro_ord')
    
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s : %s"%(self.user, self.qualification_pro_ord, self.value)