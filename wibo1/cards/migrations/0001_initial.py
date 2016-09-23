# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProductCard'
        db.create_table('cards_productcard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('due_date', self.gf('django.db.models.fields.DateField')()),
            ('production_status', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('product_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('designer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('cards', ['ProductCard'])

        # Adding model 'JobCard'
        db.create_table('cards_jobcard', (
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('job_number', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('job_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='job', to=orm['contacts.Contact'])),
            ('price_level', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('billed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('billing_contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='billing', to=orm['contacts.Contact'])),
            ('dept_chartsrting', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('approved_by', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
            ('approved_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('billing_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('cards', ['JobCard'])

        # Adding model 'DesignCard'
        db.create_table('cards_designcard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cards.ProductCard'])),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('design_status', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('super_approval', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('super_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('client_approval', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('client_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('writer_approval', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['auth.User'])),
            ('writer_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('design_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('cards', ['DesignCard'])

        # Adding model 'CardQuantity'
        db.create_table('cards_cardquantity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('material', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['inventory.Material'], null=True, blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cards.ProductCard'], null=True, blank=True)),
            ('job_card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cards.JobCard'], null=True, blank=True)),
            ('units', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('width', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3, blank=True)),
            ('height', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3, blank=True)),
            ('waste_units', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3, blank=True)),
            ('waste_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('history_lock', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('locked_price_int', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('locked_price_ext', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
            ('locked_cost', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal('cards', ['CardQuantity'])


    def backwards(self, orm):
        # Deleting model 'ProductCard'
        db.delete_table('cards_productcard')

        # Deleting model 'JobCard'
        db.delete_table('cards_jobcard')

        # Deleting model 'DesignCard'
        db.delete_table('cards_designcard')

        # Deleting model 'CardQuantity'
        db.delete_table('cards_cardquantity')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cards.cardquantity': {
            'Meta': {'object_name': 'CardQuantity'},
            'height': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'history_lock': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cards.JobCard']", 'null': 'True', 'blank': 'True'}),
            'locked_cost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'locked_price_ext': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'locked_price_int': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'material': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Material']", 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cards.ProductCard']", 'null': 'True', 'blank': 'True'}),
            'units': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'waste_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'waste_units': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'width': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        'cards.designcard': {
            'Meta': {'object_name': 'DesignCard'},
            'client_approval': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'client_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'design_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'design_status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cards.ProductCard']"}),
            'super_approval': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'super_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'writer_approval': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['auth.User']"}),
            'writer_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'cards.jobcard': {
            'Meta': {'object_name': 'JobCard'},
            'approved_by': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'approved_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billing_contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'billing'", 'to': "orm['contacts.Contact']"}),
            'billing_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job'", 'to': "orm['contacts.Contact']"}),
            'dept_chartsrting': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'job_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'job_number': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'price_level': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.ProductCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'})
        },
        'cards.productcard': {
            'Meta': {'object_name': 'ProductCard'},
            'designer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'due_date': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Material']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'product_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'product_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'production_status': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'contacts.contact': {
            'Meta': {'object_name': 'Contact'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'default_price_level': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'student_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'inventory.material': {
            'Meta': {'object_name': 'Material'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'unit_cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'unit_price_ext': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'unit_price_int': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'})
        }
    }

    complete_apps = ['cards']