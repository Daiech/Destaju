#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User


class actions(models.Model):
    name = models.CharField(max_length=150, verbose_name="name")
    code = models.CharField(max_length=150, verbose_name="code", unique=True)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return "%s - %s " % (self.code,self.name)


class rel_user_action(models.Model):
    id_user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    id_action = models.ForeignKey(actions,  null=False, related_name='%(class)s_id_action')
    extra = models.TextField(blank=True)
    date_done = models.DateTimeField(auto_now=True)
    ip_address = models.CharField(max_length=100, verbose_name="IP_address")


class UpdateTables(models.Model):
    user = models.ForeignKey(User,  null=False, related_name='%(class)s_id_user')
    table_name = models.CharField(max_length=150, verbose_name="table_name")
    record_pk = models.CharField(max_length=15, verbose_name="record_pk")
    field = models.CharField(max_length=150, verbose_name="record_pk")
    last_data = models.TextField(blank=True)
    new_data = models.TextField(blank=True)
    modification_number = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u"%s - %s modificó el campo: %s de la tabla %s, ANTES: %s, DESPUES %s" % (self.record_pk, self.user.username, self.field, self.table_name , self.last_data, self.new_data )