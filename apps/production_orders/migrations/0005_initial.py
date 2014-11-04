# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProductionOrder'
        db.create_table(u'production_orders_productionorder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='productionorder_user', to=orm['auth.User'])),
            ('activity', self.gf('django.db.models.fields.related.ForeignKey')(related_name='productionorder_activity', to=orm['process_admin.Activities'])),
            ('place', self.gf('django.db.models.fields.related.ForeignKey')(related_name='productionorder_place', to=orm['process_admin.Places'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('modifications', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('payroll', self.gf('django.db.models.fields.related.ForeignKey')(related_name='productionorder_payroll', null=True, to=orm['payroll.Payroll'])),
        ))
        db.send_create_signal(u'production_orders', ['ProductionOrder'])

        # Adding M2M table for field responsible on 'ProductionOrder'
        m2m_table_name = db.shorten_name(u'production_orders_productionorder_responsible')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('productionorder', models.ForeignKey(orm[u'production_orders.productionorder'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['productionorder_id', 'user_id'])

        # Adding M2M table for field tools on 'ProductionOrder'
        m2m_table_name = db.shorten_name(u'production_orders_productionorder_tools')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('productionorder', models.ForeignKey(orm[u'production_orders.productionorder'], null=False)),
            ('tools', models.ForeignKey(orm[u'process_admin.tools'], null=False))
        ))
        db.create_unique(m2m_table_name, ['productionorder_id', 'tools_id'])

        # Adding model 'FillingProOrd'
        db.create_table(u'production_orders_fillingproord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fillingproord_user', to=orm['auth.User'])),
            ('production_order', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['production_orders.ProductionOrder'], unique=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'production_orders', ['FillingProOrd'])

        # Adding model 'QualificationProOrd'
        db.create_table(u'production_orders_qualificationproord', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='qualificationproord_user', null=True, to=orm['auth.User'])),
            ('user_value', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='qualificationproord_user_value', null=True, to=orm['auth.User'])),
            ('production_order', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['production_orders.ProductionOrder'], unique=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comments_value', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('value', self.gf('django.db.models.fields.IntegerField')(default=4)),
            ('is_qualified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('date_qualified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_verified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'production_orders', ['QualificationProOrd'])

        # Adding model 'Filling'
        db.create_table(u'production_orders_filling', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='filling_user', to=orm['auth.User'])),
            ('value', self.gf('django.db.models.fields.FloatField')(max_length=100)),
            ('filling_pro_ord', self.gf('django.db.models.fields.related.ForeignKey')(related_name='filling_filling_pro_ord', to=orm['production_orders.FillingProOrd'])),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'production_orders', ['Filling'])


    def backwards(self, orm):
        # Deleting model 'ProductionOrder'
        db.delete_table(u'production_orders_productionorder')

        # Removing M2M table for field responsible on 'ProductionOrder'
        db.delete_table(db.shorten_name(u'production_orders_productionorder_responsible'))

        # Removing M2M table for field tools on 'ProductionOrder'
        db.delete_table(db.shorten_name(u'production_orders_productionorder_tools'))

        # Deleting model 'FillingProOrd'
        db.delete_table(u'production_orders_fillingproord')

        # Deleting model 'QualificationProOrd'
        db.delete_table(u'production_orders_qualificationproord')

        # Deleting model 'Filling'
        db.delete_table(u'production_orders_filling')


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
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modifications': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tools_user'", 'to': u"orm['auth.User']"})
        },
        u'production_orders.filling': {
            'Meta': {'object_name': 'Filling'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'filling_pro_ord': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'filling_filling_pro_ord'", 'to': u"orm['production_orders.FillingProOrd']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'filling_user'", 'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.FloatField', [], {'max_length': '100'})
        },
        u'production_orders.fillingproord': {
            'Meta': {'object_name': 'FillingProOrd'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'production_order': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['production_orders.ProductionOrder']", 'unique': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fillingproord_user'", 'to': u"orm['auth.User']"})
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
        },
        u'production_orders.qualificationproord': {
            'Meta': {'object_name': 'QualificationProOrd'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comments_value': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'date_qualified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_verified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_qualified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'production_order': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['production_orders.ProductionOrder']", 'unique': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'qualificationproord_user'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'user_value': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'qualificationproord_user_value'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'value': ('django.db.models.fields.IntegerField', [], {'default': '4'})
        }
    }

    complete_apps = ['production_orders']