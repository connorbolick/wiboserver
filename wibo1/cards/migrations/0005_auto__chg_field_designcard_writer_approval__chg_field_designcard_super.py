# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'DesignCard.writer_approval'
        db.alter_column('cards_designcard', 'writer_approval_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['employee.Employee']))

        # Changing field 'DesignCard.super_approval'
        db.alter_column('cards_designcard', 'super_approval_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['employee.Employee']))

    def backwards(self, orm):

        # Changing field 'DesignCard.writer_approval'
        db.alter_column('cards_designcard', 'writer_approval_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

        # Changing field 'DesignCard.super_approval'
        db.alter_column('cards_designcard', 'super_approval_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['auth.User']))

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
            'super_approval': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['employee.Employee']"}),
            'super_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'writer_approval': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['employee.Employee']"}),
            'writer_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'cards.jobcard': {
            'Meta': {'object_name': 'JobCard'},
            'approved_by': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'approved_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billing_contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'billing'", 'to': "orm['contacts.Contact']"}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job'", 'to': "orm['contacts.Contact']"}),
            'dept_chartstring': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'job_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'job_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'job_number': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'price_level': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.ProductCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'})
        },
        'cards.productcard': {
            'Meta': {'object_name': 'ProductCard'},
            'designer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Employee']"}),
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
            'department': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
        'employee.employee': {
            'Meta': {'object_name': 'Employee'},
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