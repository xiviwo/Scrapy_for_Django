# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Person.scraper_runtime'
        db.delete_column(u'app_person', 'scraper_runtime_id')

        # Deleting field 'Person.scraper'
        db.delete_column(u'app_person', 'scraper_id')

        # Deleting field 'Ticket.checker_runtime'
        db.delete_column(u'app_ticket', 'checker_runtime_id')


        # Changing field 'Ticket.actual_finish'
        db.alter_column(u'app_ticket', 'actual_finish', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):
        # Adding field 'Person.scraper_runtime'
        db.add_column(u'app_person', 'scraper_runtime',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dynamic_scraper.SchedulerRuntime'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'Person.scraper'
        db.add_column(u'app_person', 'scraper',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dynamic_scraper.Scraper'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'Ticket.checker_runtime'
        db.add_column(u'app_ticket', 'checker_runtime',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dynamic_scraper.SchedulerRuntime'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)


        # Changing field 'Ticket.actual_finish'
        db.alter_column(u'app_ticket', 'actual_finish', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 3, 13, 0, 0)))

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
            'actual_finish': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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