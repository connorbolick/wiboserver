# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contact'
        db.create_table('contacts_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('company', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('default_price_level', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=254)),
            ('student_id', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
        ))
        db.send_create_signal('contacts', ['Contact'])

        # Adding model 'Address'
        db.create_table('contacts_address', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contacts.Contact'])),
            ('street_address', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal('contacts', ['Address'])

        # Adding model 'Telephone'
        db.create_table('contacts_telephone', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contact', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contacts.Contact'])),
            ('phone_type', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=24)),
        ))
        db.send_create_signal('contacts', ['Telephone'])


    def backwards(self, orm):
        # Deleting model 'Contact'
        db.delete_table('contacts_contact')

        # Deleting model 'Address'
        db.delete_table('contacts_address')

        # Deleting model 'Telephone'
        db.delete_table('contacts_telephone')


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