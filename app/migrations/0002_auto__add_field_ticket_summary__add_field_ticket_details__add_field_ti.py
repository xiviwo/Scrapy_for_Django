# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Ticket.summary'
        db.add_column(u'app_ticket', 'summary',
                      self.gf('django.db.models.fields.CharField')(default='blank', max_length=128),
                      keep_default=False)

        # Adding field 'Ticket.details'
        db.add_column(u'app_ticket', 'details',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Ticket.actual_finish'
        db.add_column(u'app_ticket', 'actual_finish',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 12, 0, 0)),
                      keep_default=False)

        # Adding field 'Ticket.user'
        db.add_column(u'app_ticket', 'user',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['app.Person']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Ticket.summary'
        db.delete_column(u'app_ticket', 'summary')

        # Deleting field 'Ticket.details'
        db.delete_column(u'app_ticket', 'details')

        # Deleting field 'Ticket.actual_finish'
        db.delete_column(u'app_ticket', 'actual_finish')

        # Deleting field 'Ticket.user'
        db.delete_column(u'app_ticket', 'user_id')


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
            'actual_finish': ('django.db.models.fields.DateTimeField', [], {}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'owner_group': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'target_finish': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Person']"})
        }
    }

    complete_apps = ['app']