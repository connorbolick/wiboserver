# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Invoice'
        db.create_table('invoice_invoice', (
            ('invoice_number', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('invoice_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('billing_contact', self.gf('django.db.models.fields.related.ForeignKey')(related_name='invoice', to=orm['contacts.Contact'])),
            ('invoice_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('billed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('taxable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('invoice', ['Invoice'])

        # Adding model 'PaymentEvent'
        db.create_table('invoice_paymentevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invoice.Invoice'])),
            ('payment_user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['auth.User'])),
            ('payment_date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('payment_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('payment_amount', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('payment_proccessed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('payment_received', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('invoice', ['PaymentEvent'])

        # Adding model 'PaymentEventCash'
        db.create_table('invoice_paymenteventcash', (
            ('paymentevent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['invoice.PaymentEvent'], unique=True, primary_key=True)),
            ('receipt_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(default='CASH', max_length=5)),
        ))
        db.send_create_signal('invoice', ['PaymentEventCash'])

        # Adding model 'PaymentEventCheck'
        db.create_table('invoice_paymenteventcheck', (
            ('paymentevent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['invoice.PaymentEvent'], unique=True, primary_key=True)),
            ('receipt_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(default='CHECK', max_length=5)),
            ('check_number', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('invoice', ['PaymentEventCheck'])

        # Adding model 'PaymentEventIDO'
        db.create_table('invoice_paymenteventido', (
            ('paymentevent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['invoice.PaymentEvent'], unique=True, primary_key=True)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(default='IDO', max_length=5)),
            ('dept_chartstring', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('approved_by', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('approved_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('invoice', ['PaymentEventIDO'])

        # Adding model 'PaymentEventWebInvoice'
        db.create_table('invoice_paymenteventwebinvoice', (
            ('paymentevent_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['invoice.PaymentEvent'], unique=True, primary_key=True)),
            ('payment_type', self.gf('django.db.models.fields.CharField')(default='WEB', max_length=5)),
            ('web_invoice_number', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('sent_to_client', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('invoice', ['PaymentEventWebInvoice'])

        # Adding model 'InvQuantity'
        db.create_table('invoice_invquantity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('invoice', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['invoice.Invoice'])),
            ('job_card', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cards.JobCard'])),
            ('units', self.gf('django.db.models.fields.DecimalField')(default=1, max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal('invoice', ['InvQuantity'])


    def backwards(self, orm):
        # Deleting model 'Invoice'
        db.delete_table('invoice_invoice')

        # Deleting model 'PaymentEvent'
        db.delete_table('invoice_paymentevent')

        # Deleting model 'PaymentEventCash'
        db.delete_table('invoice_paymenteventcash')

        # Deleting model 'PaymentEventCheck'
        db.delete_table('invoice_paymenteventcheck')

        # Deleting model 'PaymentEventIDO'
        db.delete_table('invoice_paymenteventido')

        # Deleting model 'PaymentEventWebInvoice'
        db.delete_table('invoice_paymenteventwebinvoice')

        # Deleting model 'InvQuantity'
        db.delete_table('invoice_invquantity')


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
        },
        'invoice.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billing_contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoice'", 'to': "orm['contacts.Contact']"}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'invoice_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_number': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.JobCard']", 'through': "orm['invoice.InvQuantity']", 'symmetrical': 'False'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'taxable': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'invoice.invquantity': {
            'Meta': {'object_name': 'InvQuantity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invoice.Invoice']"}),
            'job_card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cards.JobCard']"}),
            'units': ('django.db.models.fields.DecimalField', [], {'default': '1', 'max_digits': '9', 'decimal_places': '3'})
        },
        'invoice.paymentevent': {
            'Meta': {'object_name': 'PaymentEvent'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'invoice': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['invoice.Invoice']"}),
            'payment_amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'payment_date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'payment_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'payment_proccessed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_received': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['auth.User']"})
        },
        'invoice.paymenteventcash': {
            'Meta': {'object_name': 'PaymentEventCash'},
            'payment_type': ('django.db.models.fields.CharField', [], {'default': "'CASH'", 'max_length': '5'}),
            'paymentevent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['invoice.PaymentEvent']", 'unique': 'True', 'primary_key': 'True'}),
            'receipt_number': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'invoice.paymenteventcheck': {
            'Meta': {'object_name': 'PaymentEventCheck'},
            'check_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'default': "'CHECK'", 'max_length': '5'}),
            'paymentevent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['invoice.PaymentEvent']", 'unique': 'True', 'primary_key': 'True'}),
            'receipt_number': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'invoice.paymenteventido': {
            'Meta': {'object_name': 'PaymentEventIDO', '_ormbases': ['invoice.PaymentEvent']},
            'approved_by': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'approved_date': ('django.db.models.fields.DateField', [], {}),
            'dept_chartstring': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'default': "'IDO'", 'max_length': '5'}),
            'paymentevent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['invoice.PaymentEvent']", 'unique': 'True', 'primary_key': 'True'})
        },
        'invoice.paymenteventwebinvoice': {
            'Meta': {'object_name': 'PaymentEventWebInvoice', '_ormbases': ['invoice.PaymentEvent']},
            'payment_type': ('django.db.models.fields.CharField', [], {'default': "'WEB'", 'max_length': '5'}),
            'paymentevent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['invoice.PaymentEvent']", 'unique': 'True', 'primary_key': 'True'}),
            'sent_to_client': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'web_invoice_number': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['invoice']