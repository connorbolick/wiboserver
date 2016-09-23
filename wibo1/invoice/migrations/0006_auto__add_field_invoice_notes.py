# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Invoice.notes'
        db.add_column('invoice_invoice', 'notes',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Invoice.notes'
        db.delete_column('invoice_invoice', 'notes')


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
        'cards.adjustmentcard': {
            'Meta': {'object_name': 'AdjustmentCard'},
            'admin_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'admin_approved_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'admin_approved_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cards_adjustmentcard_admin_set'", 'null': 'True', 'to': "orm['auth.User']"}),
            'approved_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'approved_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assigneduser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Employee']"}),
            'attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'client_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'cost_amt': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cards_adjustmentcard_created_set'", 'to': "orm['auth.User']"}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'external_amt': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_amt': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Material']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'price_ext': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'price_int': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'prod_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cards_adjustmentcard_updated_set'", 'to': "orm['auth.User']"}),
            'waste_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        'cards.cardquantity': {
            'Meta': {'object_name': 'CardQuantity'},
            'adjustment': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cards.AdjustmentCard']", 'null': 'True', 'blank': 'True'}),
            'height': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'history_lock': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_card': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cards.JobCard']", 'null': 'True', 'blank': 'True'}),
            'locked_cost': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'locked_price_ext': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'locked_price_int': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3'}),
            'material': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['inventory.Material']", 'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cards.ProductCard']", 'null': 'True', 'blank': 'True'}),
            'qtype': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'service': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cards.ServiceCard']", 'null': 'True', 'blank': 'True'}),
            'units': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'waste_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'waste_units': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'width': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        'cards.jobcard': {
            'Meta': {'object_name': 'JobCard'},
            'adjustments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.AdjustmentCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'admin_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'admin_approved_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'admin_approved_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cards_jobcard_admin_set'", 'null': 'True', 'to': "orm['auth.User']"}),
            'approved_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'approved_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assigneduser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Employee']"}),
            'attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billing_contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'billing'", 'to': "orm['contacts.Contact']"}),
            'client_last_contacted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'client_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job'", 'to': "orm['contacts.Contact']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cards_jobcard_created_set'", 'to': "orm['auth.User']"}),
            'dept_chartstring': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'job_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'job_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'job_number': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_roi': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'job'", 'null': 'True', 'to': "orm['roi.JobROI']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'price_level': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'prod_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.ProductCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.ServiceCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cards_jobcard_updated_set'", 'to': "orm['auth.User']"}),
            'waste_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        'cards.productcard': {
            'Meta': {'object_name': 'ProductCard'},
            'adjustments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.AdjustmentCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'admin_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'admin_approved_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'admin_approved_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cards_productcard_admin_set'", 'null': 'True', 'to': "orm['auth.User']"}),
            'approved_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'approved_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assigneduser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Employee']"}),
            'attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'client_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cards_productcard_created_set'", 'to': "orm['auth.User']"}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Material']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'price_ext': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'price_int': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'prod_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'product_name': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.ServiceCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cards_productcard_updated_set'", 'to': "orm['auth.User']"}),
            'waste_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        'cards.servicecard': {
            'Meta': {'object_name': 'ServiceCard'},
            'adjustments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.AdjustmentCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'admin_approved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'admin_approved_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'admin_approved_user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'cards_servicecard_admin_set'", 'null': 'True', 'to': "orm['auth.User']"}),
            'approved_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'approved_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assigneduser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Employee']"}),
            'attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'client_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'cost_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cards_servicecard_created_set'", 'to': "orm['auth.User']"}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'external_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'order_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'price_ext': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'price_int': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'prod_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cards_servicecard_updated_set'", 'to': "orm['auth.User']"}),
            'waste_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'employee.employee': {
            'Meta': {'object_name': 'Employee'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'birthday': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '254', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'graduation': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '24'}),
            'photo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'user_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'wibo_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'primary_key': 'True'})
        },
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
        },
        'invoice.invoice': {
            'Meta': {'object_name': 'Invoice'},
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billing_contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoice'", 'to': "orm['contacts.Contact']"}),
            'created_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoice_invoice_created_set'", 'to': "orm['auth.User']"}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'invoice_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'invoice_number': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'job_cards': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.JobCard']", 'through': "orm['invoice.InvQuantity']", 'symmetrical': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'taxable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated_user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invoice_invoice_updated_set'", 'to': "orm['auth.User']"})
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
            'payment_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'payment_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'payment_processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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
        'invoice.paymenteventgiftcard': {
            'Meta': {'object_name': 'PaymentEventGiftCard'},
            'gift_card_number': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'default': "'GIFT'", 'max_length': '5'}),
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
        'invoice.paymenteventmarketplace': {
            'Meta': {'object_name': 'PaymentEventMarketplace', '_ormbases': ['invoice.PaymentEvent']},
            'order_number': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'default': "'MARKET'", 'max_length': '10'}),
            'paymentevent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['invoice.PaymentEvent']", 'unique': 'True', 'primary_key': 'True'})
        },
        'invoice.paymenteventwebinvoice': {
            'Meta': {'object_name': 'PaymentEventWebInvoice', '_ormbases': ['invoice.PaymentEvent']},
            'payment_type': ('django.db.models.fields.CharField', [], {'default': "'WEB'", 'max_length': '5'}),
            'paymentevent_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['invoice.PaymentEvent']", 'unique': 'True', 'primary_key': 'True'}),
            'sent_to_client': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'web_invoice_number': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        },
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

    complete_apps = ['invoice']