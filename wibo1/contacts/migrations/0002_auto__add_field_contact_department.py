# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Contact.department'
        db.add_column('contacts_contact', 'department',
                      self.gf('django.db.models.fields.CharField')(default='Add Department!!!', max_length=255),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Contact.department'
        db.delete_column('contacts_contact', 'department')


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
            'student_id': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'contacts.telephone': {
            'Meta': {'object_name': 'Telephone'},
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contacts.Contact']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'phone_type': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        }
    }

    complete_apps = ['contacts']