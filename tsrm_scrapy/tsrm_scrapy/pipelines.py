# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from app.models import Person,Ticket
from tsrm_scrapy.items import TicketItem

class TsrmScrapyPipeline(object):
    def process_item(self, item, spider):
		print 'item=',item
		if item:
			tt = Ticket.objects.filter(ticket=item["ticket"])
		
			if tt  :
				

				tt.update(ticket=item['ticket'],
						  owner=item['owner'],
                          target_finish = item['target_finish'],
                          summary=item['summary'],
						  owner_group=item['owner_group'],
		                  priority=item['priority'],
						  user=item['user'],
                          status=item['status'],
                          details=item['details'],
                          actual_finish=item['actual_finish'])

			else:
				
				
				tt = TicketItem(ticket=item['ticket'],owner=item['owner'],target_finish = item['target_finish'],summary=item['summary'],owner_group=item['owner_group'],priority=item['priority'],user=item['user'],status=item['status'],details=item['details'],actual_finish=item['actual_finish'])
				tt.save()

