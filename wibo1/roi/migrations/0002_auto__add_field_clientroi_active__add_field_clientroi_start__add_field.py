# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'JobROI'
        db.create_table('roi_jobroi', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('cost', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('roi', ['JobROI'])

        # Adding field 'ClientROI.active'
        db.add_column('roi_clientroi', 'active',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'ClientROI.start'
        db.add_column('roi_clientroi', 'start',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'ClientROI.end'
        db.add_column('roi_clientroi', 'end',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'JobROI'
        db.delete_table('roi_jobroi')

        # Deleting field 'ClientROI.active'
        db.delete_column('roi_clientroi', 'active')

        # Deleting field 'ClientROI.start'
        db.delete_column('roi_clientroi', 'start')

        # Deleting field 'ClientROI.end'
        db.delete_column('roi_clientroi', 'end')


    models = {
        'roi.clientroi': {
            'Meta': {'object_name': 'ClientROI'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'roi.jobroi': {
            'Meta': {'object_name': 'JobROI'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['roi']