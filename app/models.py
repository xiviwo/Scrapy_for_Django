from django.db import models
#from dynamic_scraper.models import Scraper, SchedulerRuntime


# Create your models here.

class ConvertingDateTimeFeild(models.DateTimeField):

    def get_prep_value(self, value):
        return str(datetime.strptime(value, '%y-%m-%d %H:%M:%S'))


class Person(models.Model):
	name = models.CharField(max_length=64)

	affected_email = models.CharField(max_length=32,blank=True, null=True)
	reported_email = models.CharField(max_length=32,blank=True, null=True)
	#scraper = models.ForeignKey(Scraper, blank=True, null=True, on_delete=models.SET_NULL)
	#scraper_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL)
	def __unicode__(self):
		return self.name


class Ticket(models.Model):
	ticket = models.CharField(max_length=64)

	owner = models.CharField(max_length=32)
	owner_group = models.CharField(max_length=32)
	status = models.CharField(max_length=128)
	priority = models.CharField(max_length=128)
	#14-2-8 0:35:23
	target_finish = models.DateTimeField(auto_now=False)
	summary  = models.CharField(max_length=128)
	details = models.TextField(blank=True)
	actual_finish = models.DateTimeField(auto_now=False, blank=True, null=True)
	user = models.ForeignKey(Person)
	#checker_runtime = models.ForeignKey(SchedulerRuntime, blank=True, null=True, on_delete=models.SET_NULL),input_formats=['%y-%m-%d %H:%M:%S']
	def __unicode__(self):
		return self.ticket

class Crawl(models.Model):
	run_date = models.DateTimeField(auto_now=True)
	log = models.TextField(blank=True)
	def __init__(self):
		spider = TicketSpider()
		settings = get_project_settings()
		crawler = Crawler(settings)
		crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
		crawler.configure()
		crawler.crawl(spider)
		crawler.start()
		log.start()
		print log,dir(log)
		reactor.run()
	

