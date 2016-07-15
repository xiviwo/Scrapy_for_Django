from django.contrib import admin

# Register your models here.

import xadmin
from xadmin import views
from models import Person,Ticket

#from dynamic_scraper.models import Scraper, SchedulerRuntime,Log,ScrapedObjClass,ScrapedObjAttr,ScraperElem


class MainDashboard(object):
    widgets = [
 
        [
			{"type": "html", "title": "Test Widget", "content": "<h3> Crawl </h3><p>this is test</p>"},
            {"type": "qbutton", "title": "Crawl Tsrm", "btns": [{'model': Ticket}]},
        
        ]
    ]
xadmin.site.register(views.website.IndexView, MainDashboard)


class TicketAdmin(object):

    list_display = ('ticket', 'owner', 'status','target_finish','user','summary')
    list_display_links = ('ticket')
    list_filter = ['owner','owner_group','status','user']

    search_fields = ['ticket','owner','owner_group','status','user']
 

xadmin.site.register(Ticket, TicketAdmin)

class PersonAdmin(object):

    list_display = ('name', 'affected_email', 'reported_email')
    list_display_links = ('name')


    search_fields = ['name']
 

xadmin.site.register(Person, PersonAdmin)

'''class ScraperAdmin(object):

	pass
 

xadmin.site.register(Scraper, ScraperAdmin)

class SchedulerRuntimeAdmin(object):

	pass
 

xadmin.site.register(SchedulerRuntime, SchedulerRuntimeAdmin)


class LogAdmin(object):

	pass
 

xadmin.site.register(Log, LogAdmin)

class ScrapedObjAttrAdmin(object):
	pass
xadmin.site.register(ScrapedObjAttr,ScrapedObjAttrAdmin)

class ScraperElemAdmin(object):
	pass
xadmin.site.register(ScraperElem,ScraperElemAdmin)

class ScrapedObjClassAdmin(object):
	pass
xadmin.site.register(ScrapedObjClass,ScrapedObjClassAdmin)'''
