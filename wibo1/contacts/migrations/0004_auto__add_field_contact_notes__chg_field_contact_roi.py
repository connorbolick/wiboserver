# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Contact.notes'
        db.add_column('contacts_contact', 'notes',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


        # Changing field 'Contact.roi'
        db.alter_column('contacts_contact', 'roi_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['roi.ClientROI'], null=True))

    def backwards(self, orm):
        # Deleting field 'Contact.notes'
        db.delete_column('contacts_contact', 'notes')


        # Changing field 'Contact.roi'
        db.alter_column('contacts_contact', 'roi_id', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['roi.ClientROI']))

    models = {
        'contacts.address': {
            'Meta': {'object_name': 'Address'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contacts.Contact']"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'street_address': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'contacts.contact': {
            'Meta': {'object_name': 'Contact'},
            'company': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'default_price_level': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'department': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'roi': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['roi.ClientROI']", 'null': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'contacts.telephone': {
            'Meta': {'object_name': 'Telephone'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contacts.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'phone_type': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        'roi.clientroi': {
            'Meta': {'object_name': 'ClientROI'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['contacts']