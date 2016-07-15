# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Crawl'
        db.create_table(u'app_crawl', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('run_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('log', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'app', ['Crawl'])


        # Changing field 'Person.reported_email'
        db.alter_column(u'app_person', 'reported_email', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))

        # Changing field 'Person.affected_email'
        db.alter_column(u'app_person', 'affected_email', self.gf('django.db.models.fields.CharField')(max_length=32, null=True))

        # Changing field 'Ticket.target_finish'
        db.alter_column(u'app_ticket', 'target_finish', self.gf('django.db.models.fields.DateTimeField')())

    def backwards(self, orm):
        # Deleting model 'Crawl'
        db.delete_table(u'app_crawl')


        # Changing field 'Person.reported_email'
        db.alter_column(u'app_person', 'reported_email', self.gf('django.db.models.fields.CharField')(default=' ', max_length=32))

        # Changing field 'Person.affected_email'
        db.alter_column(u'app_person', 'affected_email', self.gf('django.db.models.fields.CharField')(default=' ', max_length=32))

        # Changing field 'Ticket.target_finish'
        db.alter_column(u'app_ticket', 'target_finish', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))

    models = {
        u'app.crawl': {
            'Meta': {'object_name': 'Crawl'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'log': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'run_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'app.person': {
            'Meta': {'object_name': 'Person'},
            'affected_email': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'reported_email': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'})
        },
        u'app.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'actual_finish': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'owner_group': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'priority': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'summary': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'target_finish': ('django.db.models.fields.DateTimeField', [], {}),
            'ticket': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['app.Person']"})
        }
    }

    complete_apps = ['app']