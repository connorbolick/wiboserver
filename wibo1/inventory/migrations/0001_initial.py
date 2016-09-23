# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Material'
        db.create_table('inventory_material', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('unit_price_int', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('unit_price_ext', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('unit_cost', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=5)),
        ))
        db.send_create_signal('inventory', ['Material'])


    def backwards(self, orm):
        # Deleting model 'Material'
        db.delete_table('inventory_material')


    models = {
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

    complete_apps = ['inventory']