# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Material.category'
        db.alter_column('inventory_material', 'category', self.gf('django.db.models.fields.CharField')(max_length=50))

    def backwards(self, orm):

        # Changing field 'Material.category'
        db.alter_column('inventory_material', 'category', self.gf('django.db.models.fields.CharField')(max_length=5))

    models = {
        'inventory.material': {
            'Meta': {'object_name': 'Material'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
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