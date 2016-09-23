# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AdjustmentCard'
        db.create_table('cards_adjustmentcard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('assigneduser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3)),
            ('prod_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('client_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('approved_by', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('approved_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('waste_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True)),
            ('attention', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('billable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price_int', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('price_ext', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('internal_amt', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('external_amt', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('cost_amt', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal('cards', ['AdjustmentCard'])

        # Adding model 'ServiceCard'
        db.create_table('cards_servicecard', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('due_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('assigneduser', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3)),
            ('prod_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('client_notes', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('approved_by', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('approved_on', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('waste_cost', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3, blank=True)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True)),
            ('attention', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('billable', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('archived', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('price_int', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('price_ext', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('internal_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('external_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
            ('cost_rate', self.gf('django.db.models.fields.DecimalField')(max_digits=9, decimal_places=3)),
        ))
        db.send_create_signal('cards', ['ServiceCard'])

        # Adding field 'DesignCard.name'
        db.add_column('cards_designcard', 'name',
                      self.gf('django.db.models.fields.CharField')(default='design card', max_length=255),
                      keep_default=False)

        # Adding field 'DesignCard.due_date'
        db.add_column('cards_designcard', 'due_date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)

        # Adding field 'DesignCard.assigneduser'
        db.add_column('cards_designcard', 'assigneduser',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'DesignCard.cost'
        db.add_column('cards_designcard', 'cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3),
                      keep_default=False)

        # Adding field 'DesignCard.prod_notes'
        db.add_column('cards_designcard', 'prod_notes',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DesignCard.client_notes'
        db.add_column('cards_designcard', 'client_notes',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DesignCard.approved_by'
        db.add_column('cards_designcard', 'approved_by',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'DesignCard.approved_on'
        db.add_column('cards_designcard', 'approved_on',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'DesignCard.waste_cost'
        db.add_column('cards_designcard', 'waste_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'DesignCard.attention'
        db.add_column('cards_designcard', 'attention',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'DesignCard.billable'
        db.add_column('cards_designcard', 'billable',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'DesignCard.archived'
        db.add_column('cards_designcard', 'archived',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CardQuantity.qtype'
        db.add_column('cards_cardquantity', 'qtype',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)

        # Adding field 'CardQuantity.service'
        db.add_column('cards_cardquantity', 'service',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cards.ServiceCard'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'CardQuantity.adjustment'
        db.add_column('cards_cardquantity', 'adjustment',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['cards.AdjustmentCard'], null=True, blank=True),
                      keep_default=False)

        # Deleting field 'JobCard.approved_date'
        db.delete_column('cards_jobcard', 'approved_date')

        # Adding field 'JobCard.name'
        db.add_column('cards_jobcard', 'name',
                      self.gf('django.db.models.fields.CharField')(default='job card', max_length=255),
                      keep_default=False)

        # Adding field 'JobCard.assigneduser'
        db.add_column('cards_jobcard', 'assigneduser',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'JobCard.cost'
        db.add_column('cards_jobcard', 'cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3),
                      keep_default=False)

        # Adding field 'JobCard.prod_notes'
        db.add_column('cards_jobcard', 'prod_notes',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'JobCard.approved_on'
        db.add_column('cards_jobcard', 'approved_on',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'JobCard.waste_cost'
        db.add_column('cards_jobcard', 'waste_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'JobCard.thumbnail'
        db.add_column('cards_jobcard', 'thumbnail',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'JobCard.attention'
        db.add_column('cards_jobcard', 'attention',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'JobCard.billable'
        db.add_column('cards_jobcard', 'billable',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'JobCard.archived'
        db.add_column('cards_jobcard', 'archived',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'JobCard.price'
        db.add_column('cards_jobcard', 'price',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3),
                      keep_default=False)


        # Changing field 'JobCard.approved_by'
        db.alter_column('cards_jobcard', 'approved_by', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'JobCard.payment_type'
        db.alter_column('cards_jobcard', 'payment_type', self.gf('django.db.models.fields.CharField')(max_length=100))
        # Deleting field 'ProductCard.product_notes'
        db.delete_column('cards_productcard', 'product_notes')

        # Deleting field 'ProductCard.production_status'
        db.delete_column('cards_productcard', 'production_status')

        # Adding field 'ProductCard.name'
        db.add_column('cards_productcard', 'name',
                      self.gf('django.db.models.fields.CharField')(default='product card', max_length=255),
                      keep_default=False)

        # Adding field 'ProductCard.assigneduser'
        db.add_column('cards_productcard', 'assigneduser',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User']),
                      keep_default=False)

        # Adding field 'ProductCard.cost'
        db.add_column('cards_productcard', 'cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3),
                      keep_default=False)

        # Adding field 'ProductCard.prod_notes'
        db.add_column('cards_productcard', 'prod_notes',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'ProductCard.client_notes'
        db.add_column('cards_productcard', 'client_notes',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'ProductCard.approved_by'
        db.add_column('cards_productcard', 'approved_by',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)

        # Adding field 'ProductCard.approved_on'
        db.add_column('cards_productcard', 'approved_on',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'ProductCard.waste_cost'
        db.add_column('cards_productcard', 'waste_cost',
                      self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=9, decimal_places=3, blank=True),
                      keep_default=False)

        # Adding field 'ProductCard.thumbnail'
        db.add_column('cards_productcard', 'thumbnail',
                      self.gf('django.db.models.fields.files.ImageField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'ProductCard.attention'
        db.add_column('cards_productcard', 'attention',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'ProductCard.billable'
        db.add_column('cards_productcard', 'billable',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'ProductCard.archived'
        db.add_column('cards_productcard', 'archived',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'ProductCard.status'
        db.add_column('cards_productcard', 'status',
                      self.gf('django.db.models.fields.CharField')(default='default', max_length=100),
                      keep_default=False)

        # Adding field 'ProductCard.price_int'
        db.add_column('cards_productcard', 'price_int',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3),
                      keep_default=False)

        # Adding field 'ProductCard.price_ext'
        db.add_column('cards_productcard', 'price_ext',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=9, decimal_places=3),
                      keep_default=False)


        # Changing field 'ProductCard.due_date'
        db.alter_column('cards_productcard', 'due_date', self.gf('django.db.models.fields.DateField')(null=True))

    def backwards(self, orm):
        # Deleting model 'AdjustmentCard'
        db.delete_table('cards_adjustmentcard')

        # Deleting model 'ServiceCard'
        db.delete_table('cards_servicecard')

        # Deleting field 'DesignCard.name'
        db.delete_column('cards_designcard', 'name')

        # Deleting field 'DesignCard.due_date'
        db.delete_column('cards_designcard', 'due_date')

        # Deleting field 'DesignCard.assigneduser'
        db.delete_column('cards_designcard', 'assigneduser_id')

        # Deleting field 'DesignCard.cost'
        db.delete_column('cards_designcard', 'cost')

        # Deleting field 'DesignCard.prod_notes'
        db.delete_column('cards_designcard', 'prod_notes')

        # Deleting field 'DesignCard.client_notes'
        db.delete_column('cards_designcard', 'client_notes')

        # Deleting field 'DesignCard.approved_by'
        db.delete_column('cards_designcard', 'approved_by')

        # Deleting field 'DesignCard.approved_on'
        db.delete_column('cards_designcard', 'approved_on')

        # Deleting field 'DesignCard.waste_cost'
        db.delete_column('cards_designcard', 'waste_cost')

        # Deleting field 'DesignCard.attention'
        db.delete_column('cards_designcard', 'attention')

        # Deleting field 'DesignCard.billable'
        db.delete_column('cards_designcard', 'billable')

        # Deleting field 'DesignCard.archived'
        db.delete_column('cards_designcard', 'archived')

        # Deleting field 'CardQuantity.qtype'
        db.delete_column('cards_cardquantity', 'qtype')

        # Deleting field 'CardQuantity.service'
        db.delete_column('cards_cardquantity', 'service_id')

        # Deleting field 'CardQuantity.adjustment'
        db.delete_column('cards_cardquantity', 'adjustment_id')

        # Adding field 'JobCard.approved_date'
        db.add_column('cards_jobcard', 'approved_date',
                      self.gf('django.db.models.fields.DateField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'JobCard.name'
        db.delete_column('cards_jobcard', 'name')

        # Deleting field 'JobCard.assigneduser'
        db.delete_column('cards_jobcard', 'assigneduser_id')

        # Deleting field 'JobCard.cost'
        db.delete_column('cards_jobcard', 'cost')

        # Deleting field 'JobCard.prod_notes'
        db.delete_column('cards_jobcard', 'prod_notes')

        # Deleting field 'JobCard.approved_on'
        db.delete_column('cards_jobcard', 'approved_on')

        # Deleting field 'JobCard.waste_cost'
        db.delete_column('cards_jobcard', 'waste_cost')

        # Deleting field 'JobCard.thumbnail'
        db.delete_column('cards_jobcard', 'thumbnail')

        # Deleting field 'JobCard.attention'
        db.delete_column('cards_jobcard', 'attention')

        # Deleting field 'JobCard.billable'
        db.delete_column('cards_jobcard', 'billable')

        # Deleting field 'JobCard.archived'
        db.delete_column('cards_jobcard', 'archived')

        # Deleting field 'JobCard.price'
        db.delete_column('cards_jobcard', 'price')


        # Changing field 'JobCard.approved_by'
        db.alter_column('cards_jobcard', 'approved_by', self.gf('django.db.models.fields.CharField')(max_length=30, null=True))

        # Changing field 'JobCard.payment_type'
        db.alter_column('cards_jobcard', 'payment_type', self.gf('django.db.models.fields.CharField')(max_length=10))
        # Adding field 'ProductCard.product_notes'
        db.add_column('cards_productcard', 'product_notes',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'ProductCard.production_status'
        db.add_column('cards_productcard', 'production_status',
                      self.gf('django.db.models.fields.CharField')(default='closed', max_length=10),
                      keep_default=False)

        # Deleting field 'ProductCard.name'
        db.delete_column('cards_productcard', 'name')

        # Deleting field 'ProductCard.assigneduser'
        db.delete_column('cards_productcard', 'assigneduser_id')

        # Deleting field 'ProductCard.cost'
        db.delete_column('cards_productcard', 'cost')

        # Deleting field 'ProductCard.prod_notes'
        db.delete_column('cards_productcard', 'prod_notes')

        # Deleting field 'ProductCard.client_notes'
        db.delete_column('cards_productcard', 'client_notes')

        # Deleting field 'ProductCard.approved_by'
        db.delete_column('cards_productcard', 'approved_by')

        # Deleting field 'ProductCard.approved_on'
        db.delete_column('cards_productcard', 'approved_on')

        # Deleting field 'ProductCard.waste_cost'
        db.delete_column('cards_productcard', 'waste_cost')

        # Deleting field 'ProductCard.thumbnail'
        db.delete_column('cards_productcard', 'thumbnail')

        # Deleting field 'ProductCard.attention'
        db.delete_column('cards_productcard', 'attention')

        # Deleting field 'ProductCard.billable'
        db.delete_column('cards_productcard', 'billable')

        # Deleting field 'ProductCard.archived'
        db.delete_column('cards_productcard', 'archived')

        # Deleting field 'ProductCard.status'
        db.delete_column('cards_productcard', 'status')

        # Deleting field 'ProductCard.price_int'
        db.delete_column('cards_productcard', 'price_int')

        # Deleting field 'ProductCard.price_ext'
        db.delete_column('cards_productcard', 'price_ext')


        # Changing field 'ProductCard.due_date'
        db.alter_column('cards_productcard', 'due_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 9, 13, 0, 0)))

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
            'approved_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'approved_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assigneduser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'client_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'cost_amt': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'external_amt': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_amt': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Material']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price_ext': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'price_int': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'prod_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
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
            'waste_units': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'width': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        'cards.designcard': {
            'Meta': {'object_name': 'DesignCard'},
            'approved_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'approved_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assigneduser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'client_approval': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'client_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'client_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'design_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'design_status': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'prod_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['cards.ProductCard']"}),
            'super_approval': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['employee.Employee']"}),
            'super_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'waste_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'}),
            'writer_approval': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': "orm['employee.Employee']"}),
            'writer_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'cards.jobcard': {
            'Meta': {'object_name': 'JobCard'},
            'adjustments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.AdjustmentCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'approved_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'approved_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assigneduser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'billed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billing_contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'billing'", 'to': "orm['contacts.Contact']"}),
            'client_last_contacted': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'client_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'job'", 'to': "orm['contacts.Contact']"}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'dept_chartstring': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'invoice_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'job_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'job_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'job_number': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'payment_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'price_level': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'prod_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'products': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.ProductCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.ServiceCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'waste_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        'cards.productcard': {
            'Meta': {'object_name': 'ProductCard'},
            'adjustments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.AdjustmentCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'approved_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'approved_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assigneduser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'client_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'designer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['employee.Employee']"}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'materials': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['inventory.Material']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price_ext': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'price_int': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'prod_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'product_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'services': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.ServiceCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'waste_cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3', 'blank': 'True'})
        },
        'cards.servicecard': {
            'Meta': {'object_name': 'ServiceCard'},
            'adjustments': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['cards.AdjustmentCard']", 'through': "orm['cards.CardQuantity']", 'symmetrical': 'False'}),
            'approved_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'approved_on': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'archived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assigneduser': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'attention': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'billable': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'client_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'cost': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '9', 'decimal_places': '3'}),
            'cost_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'due_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'external_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_rate': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'price_ext': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'price_int': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'prod_notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
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
        'roi.clientroi': {
            'Meta': {'object_name': 'ClientROI'},
            'cost': ('django.db.models.fields.DecimalField', [], {'max_digits': '9', 'decimal_places': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cards']