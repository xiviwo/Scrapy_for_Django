# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Person.scraper'
        db.add_column(u'app_person', 'scraper',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dynamic_scraper.Scraper'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'Person.scraper_runtime'
        db.add_column(u'app_person', 'scraper_runtime',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dynamic_scraper.SchedulerRuntime'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)

        # Adding field 'Ticket.checker_runtime'
        db.add_column(u'app_ticket', 'checker_runtime',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dynamic_scraper.SchedulerRuntime'], null=True, on_delete=models.SET_NULL, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Person.scraper'
        db.delete_column(u'app_person', 'scraper_id')

        # Deleting field 'Person.scraper_runtime'
        db.delete_column(u'app_person', 'scraper_runtime_id')

        # Deleting field 'Ticket.checker_runtime'
        db.delete_column(u'app_ticket', 'checker_runtime_id')


    models = {
        u'app.person': {
            'Meta': {'object_name': 'Person'},
            'affected_email': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'reported_email': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'scraper': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dynamic_scraper.Scraper']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
            'scraper_runtime': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dynamic_scraper.SchedulerRuntime']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'})
        },
        u'app.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'actual_finish': ('django.db.models.fields.DateTimeField', [], {}),
            'checker_runtime': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dynamic_scraper.SchedulerRuntime']", 'null': 'True', 'on_delete': 'models.SET_NULL', 'blank': 'True'}),
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
        },
        u'dynamic_scraper.schedulerruntime': {
            'Meta': {'ordering': "['next_action_time']", 'object_name': 'SchedulerRuntime'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'next_action_factor': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'next_action_time': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'num_zero_actions': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'runtime_type': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'})
        },
        u'dynamic_scraper.scrapedobjclass': {
            'Meta': {'ordering': "['name']", 'object_name': 'ScrapedObjClass'},
            'checker_scheduler_conf': ('django.db.models.fields.TextField', [], {'default': '\'"MIN_TIME": 1440,\\n"MAX_TIME": 10080,\\n"INITIAL_NEXT_ACTION_FACTOR": 1,\\n"ZERO_ACTIONS_FACTOR_CHANGE": 5,\\n"FACTOR_CHANGE_FACTOR": 1.3,\\n\''}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'scraper_scheduler_conf': ('django.db.models.fields.TextField', [], {'default': '\'"MIN_TIME": 15,\\n"MAX_TIME": 10080,\\n"INITIAL_NEXT_ACTION_FACTOR": 10,\\n"ZERO_ACTIONS_FACTOR_CHANGE": 20,\\n"FACTOR_CHANGE_FACTOR": 1.3,\\n\''})
        },
        u'dynamic_scraper.scraper': {
            'Meta': {'ordering': "['name', 'scraped_obj_class']", 'object_name': 'Scraper'},
            'checker_ref_url': ('django.db.models.fields.URLField', [], {'max_length': '500', 'blank': 'True'}),
            'checker_type': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'checker_x_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'checker_x_path_result': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_type': ('django.db.models.fields.CharField', [], {'default': "'H'", 'max_length': '1'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_items_read': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'max_items_save': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'pagination_append_str': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'pagination_on_start': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pagination_page_replace': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'pagination_type': ('django.db.models.fields.CharField', [], {'default': "'N'", 'max_length': '1'}),
            'scraped_obj_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dynamic_scraper.ScrapedObjClass']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '1'})
        }
    }

    complete_apps = ['app']