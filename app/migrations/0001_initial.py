# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'app_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('affected_email', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('reported_email', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal(u'app', ['Person'])

        # Adding model 'Ticket'
        db.create_table(u'app_ticket', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ticket', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('owner', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('owner_group', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('priority', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('target_finish', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'app', ['Ticket'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'app_person')

        # Deleting model 'Ticket'
        db.delete_table(u'app_ticket')


    models = {
        u'app.person': {
            'Meta': {'object_name': 'Person'},
            'affected_email': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'reported_email': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        u'app.ticket': {
            'Meta': {'object_name': 'Ticket'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'owner_group': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'target_finish': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['app']