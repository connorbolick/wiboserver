# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ClientROI'
        db.create_table('roi_clientroi', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('roi', ['ClientROI'])


    def backwards(self, orm):
        # Deleting model 'ClientROI'
        db.delete_table('roi_clientroi')


    models = {
        'roi.clientroi': {
            'Meta': {'object_name': 'ClientROI'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['roi']