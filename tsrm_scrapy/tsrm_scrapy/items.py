# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from app.models import Ticket

class TicketItem(DjangoItem):
    django_model = Ticket

'''class TsrmScrapyItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass'''
