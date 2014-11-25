# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Inventory'
        db.create_table(u'inventory_inventory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tool', self.gf('django.db.models.fields.related.ForeignKey')(related_name='inventory_tool', to=orm['process_admin.Tools'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')(max_length=20)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['Inventory'])

        # Adding model 'ProviderOrder'
        db.create_table(u'inventory_providerorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_generator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='providerorder_user_generator', to=orm['auth.User'])),
            ('user_provider', self.gf('django.db.models.fields.related.ForeignKey')(related_name='providerorder_user_provider', to=orm['auth.User'])),
            ('user_approver', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='providerorder_user_approved', null=True, to=orm['auth.User'])),
            ('invoice_number', self.gf('django.db.models.fields.CharField')(default='---', max_length=50, null=True, blank=True)),
            ('details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status_order', self.gf('django.db.models.fields.CharField')(default='Waiting', max_length=20)),
            ('date_approved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['ProviderOrder'])

        # Adding model 'EmployedOrder'
        db.create_table(u'inventory_employedorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user_approver', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='employedorder_user_approver', null=True, to=orm['auth.User'])),
            ('user_generator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='employedorder_user_generator', to=orm['auth.User'])),
            ('production_order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='employedorder_production_order', to=orm['production_orders.ProductionOrder'])),
            ('type_order', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('details', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('status_order', self.gf('django.db.models.fields.CharField')(default='Waiting', max_length=20)),
            ('date_approved', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['EmployedOrder'])

        # Adding model 'QuantityProviderTool'
        db.create_table(u'inventory_quantityprovidertool', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tool', self.gf('django.db.models.fields.related.ForeignKey')(related_name='quantityprovidertool_tool', to=orm['process_admin.Tools'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')(max_length=20)),
            ('unit_value', self.gf('django.db.models.fields.FloatField')(max_length=30)),
            ('provider_order', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='quantityprovidertool_provider_order', null=True, to=orm['inventory.ProviderOrder'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['QuantityProviderTool'])

        # Adding model 'QuantityEmployedTool'
        db.create_table(u'inventory_quantityemployedtool', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tool', self.gf('django.db.models.fields.related.ForeignKey')(related_name='quantityemployedtool_tool', to=orm['process_admin.Tools'])),
            ('quantity', self.gf('django.db.models.fields.FloatField')(max_length=20)),
            ('employed_order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='quantityemployedtool_employed_order', to=orm['inventory.EmployedOrder'])),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'inventory', ['QuantityEmployedTool'])


    def backwards(self, orm):
        # Deleting model 'Inventory'
        db.delete_table(u'inventory_inventory')

        # Deleting model 'ProviderOrder'
        db.delete_table(u'inventory_providerorder')

        # Deleting model 'EmployedOrder'
        db.delete_table(u'inventory_employedorder')

        # Deleting model 'QuantityProviderTool'
        db.delete_table(u'inventory_quantityprovidertool')

        # Deleting model 'QuantityEmployedTool'
        db.delete_table(u'inventory_quantityemployedtool')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'inventory.employedorder': {
            'Meta': {'object_name': 'EmployedOrder'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_approved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'production_order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'employedorder_production_order'", 'to': u"orm['production_orders.ProductionOrder']"}),
            'status_order': ('django.db.models.fields.CharField', [], {'default': "'Waiting'", 'max_length': '20'}),
            'type_order': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'user_approver': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'employedorder_user_approver'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_generator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'employedorder_user_generator'", 'to': u"orm['auth.User']"})
        },
        u'inventory.inventory': {
            'Meta': {'object_name': 'Inventory'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'quantity': ('django.db.models.fields.FloatField', [], {'max_length': '20'}),
            'tool': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inventory_tool'", 'to': u"orm['process_admin.Tools']"})
        },
        u'inventory.providerorder': {
            'Meta': {'object_name': 'ProviderOrder'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_approved': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice_number': ('django.db.models.fields.CharField', [], {'default': "'---'", 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'status_order': ('django.db.models.fields.CharField', [], {'default': "'Waiting'", 'max_length': '20'}),
            'user_approver': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'providerorder_user_approved'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_generator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'providerorder_user_generator'", 'to': u"orm['auth.User']"}),
            'user_provider': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'providerorder_user_provider'", 'to': u"orm['auth.User']"})
        },
        u'inventory.quantityemployedtool': {
            'Meta': {'object_name': 'QuantityEmployedTool'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'employed_order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quantityemployedtool_employed_order'", 'to': u"orm['inventory.EmployedOrder']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'quantity': ('django.db.models.fields.FloatField', [], {'max_length': '20'}),
            'tool': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quantityemployedtool_tool'", 'to': u"orm['process_admin.Tools']"})
        },
        u'inventory.quantityprovidertool': {
            'Meta': {'object_name': 'QuantityProviderTool'},
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'provider_order': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'quantityprovidertool_provider_order'", 'null': 'True', 'to': u"orm['inventory.ProviderOrder']"}),
            'quantity': ('django.db.models.fields.FloatField', [], {'max_length': '20'}),
            'tool': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'quantityprovidertool_tool'", 'to': u"orm['process_admin.Tools']"}),
            'unit_value': ('django.db.models.fields.FloatField', [], {'max_length': '30'})
        },
        u'payroll.payroll': {
            'Meta': {'object_name': 'Payroll'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'payroll_admin'", 'to': u"orm['auth.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'process_admin.activities': {
            'Meta': {'object_name': 'Activities'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'measuring_unit': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modifications': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'activities_user'", 'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'max_length': '50'})
        },
        u'process_admin.places': {
            'Meta': {'object_name': 'Places'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modifications': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'places_user'", 'to': u"orm['auth.User']"})
        },
        u'process_admin.tools': {
            'Meta': {'object_name': 'Tools'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modifications': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tools_user'", 'to': u"orm['auth.User']"})
        },
        u'production_orders.productionorder': {
            'Meta': {'object_name': 'ProductionOrder'},
            'activity': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productionorder_activity'", 'to': u"orm['process_admin.Activities']"}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modifications': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'payroll': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productionorder_payroll'", 'null': 'True', 'to': u"orm['payroll.Payroll']"}),
            'place': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productionorder_place'", 'to': u"orm['process_admin.Places']"}),
            'responsible': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'tools': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['process_admin.Tools']", 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'productionorder_user'", 'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['inventory']