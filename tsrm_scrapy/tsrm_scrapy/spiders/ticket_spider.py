#!/usr/bin/env python
#-*- coding:utf-8 -*-
from scrapy.spider import Spider
from tsrm_scrapy.items import TicketItem
import time,base64
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Request,FormRequest
from weblib import WebPage
import re,sys,datetime
from scrapy.selector import Selector
from app.models import Person,Ticket
reload(sys) 
sys.setdefaultencoding('utf-8') 


def to_unicode(s):
	
	if isinstance(s, str):
		s = unicode(s,'utf-8')
		return s
	elif isinstance(s, unicode):
		return s
	
	else:
		return unicode(str(s),'utf-8')
def xmlparse(response):
	xml =  WebPage(response.body)
	xml.parse(['input','button','a','li','img','span','label','textarea'],['id','title','text','ae','ev','alt','href','value'],VERBOSE = True)

def parse_list(xml):
	emptytext = "&nbsp;"
	emptytag = '<label ctype="label" title=""></label>'

	xml = WebPage(xml.replace(emptytext,emptytag))
	ticketdict = dict(xml.parse(['span'],['text','id']))
	ticket = [ k for k,v in ticketdict.items() if re.match("^(IN\d*)$",k)]
	print ticket
	print 'size of ticket',len(ticket)
	table =  xml.parse(['table'],['title'])
	
	table = [ v[0] for i,v  in enumerate(table)  if i % 2 == 0 ]

	headstart = table.index('Global Issue')
	headend = table.index('Owner Group')

	print("headstart:",headstart)
	print("headend:",headend)
	header = table[headstart:headend+1]
	
	print("header after fuzz match:",header)
	start = [ i for i,v in enumerate(table) if v == 'Global Issue： unchecked'  ] 
	start = [ v for i,v  in enumerate(start)  if i % 2 == 0 ]

	end = [ i for i,v in enumerate(table) if v == 'Locked： unchecked' ] 
	print("start field=",start)
	print("end field=",end)
	data = [] 
	for s, e in zip(start, end):
		print s,e
		data.append(dict([ (h,v) for h,v in zip(header,table[s+1:e])]))
	
	for i,d in enumerate(data):
		d['Incident'] = ticket[i]

	print "SIze of data",len(data)
	return data


class TicketSpider(Spider):
	name = 'ticket'
	allowed_domains = ["ibm.com"]
	start_urls = ['https://w3-01.ibm.com/itd/igaism/webclient/login/login.jsp?appservauth=true']
	email = 'test@.com'
	password = base64.b64decode('fas==')
	csrftoken = ''
	uisessionid =''
	inputdict = ''
	searchdict = ''
	url = 'https://w3-01.ibm.com/itd/igaism/ui/maximo.jsp'
	def postdata(self,eventlist,requestType="SYNC",currentfocus=""):

		if isinstance(eventlist,dict):
			eventlist = [ eventlist]

		event = '[' + ','.join(self.gen_event_dict(**e) for e in eventlist) + ']'
		

		data = {'uisessionid':self.uisessionid,
		'csrftoken':self.csrftoken,
		'currentfocus':currentfocus,
		'scrollleftpos':'0',
		'scrolltoppos':'0',
		'requesttype':requestType,
		'responsetype':'text/xml',
		'events': event
		}
		print 'postdata',data
		return data
	def gen_event_dict(self,targetId,value="",requestType="SYNC",acttype="setvalue",options=[]):
		eventstr="{"
		event = [
				("type",acttype),
				("targetId",targetId),
				("value",value),
				("requestType",requestType),
				("csrftokenholder",self.csrftoken),
				]
		for k,v in event:
			
			eventstr +='"' + k + '":"' + to_unicode(v) + '",'
		if options:
			for k,v in options:
				eventstr +='"' + k + '":"' + to_unicode(v) + '",'
		eventstr =  eventstr.strip(',')+'}'
		print("one event str",eventstr)
		return eventstr

	def parse(self, response):
		#print response.body
		return [FormRequest.from_response(response,
		            formdata={'j_username':self.email,'j_password':self.password },
		            callback=self.after_login)]

		return TicketItem(name='rolando')
	def after_login(self,response):
		xmlparse(response)
		#print response.body
		xml = WebPage(response.body)
		token = dict(xml.parse(['input'],['id','value']))
		print token
		self.uisessionid= token['uisessionid']
		self.csrftoken= token['csrftokenholder']
		#event = {"acttype":"click","targetId":"mx181",'currentfocus':"mx181"}
		event = {'eventlist':{"acttype":"click","targetId":"mx181"},'currentfocus':"mx181"}
		data = self.postdata(**event)
		return [FormRequest(url=self.url,
                    formdata=data,
                    callback=self.after_change_app)]
	def after_change_app(self,response):
		xmlparse(response)
		#xml = WebPage(response.body)
		return Request('https://w3-01.ibm.com/itd/igaism/ui/?event=loadapp&value=incident&uisessionid=' + self.uisessionid + '&csrftoken=' + self.csrftoken,
                      callback=self.after_load_app)
		
	def after_load_app(self,response):
		xmlparse(response)
		xml = WebPage(response.body)
		inputdict = dict(xml.parse(['input'],['title','id']))
		print("inputdict:",inputdict)

		self.inputdict = inputdict
		#event = {"targetId":inputdict['Owner Name filter'],"value":"=xiong chang wu,=ji de he,=hua lei zhao,=QIAO LING",'currentfocus':inputdict['Owner Name filter']}
		event = {'eventlist':{"acttype":"find","targetId":inputdict['Find Incident']},'currentfocus':inputdict['Find Incident']}
		data = self.postdata(**event)
		return [FormRequest(url=self.url,formdata=data,callback=self.after_click_search)]

	def after_click_search(self,response):
		xmlparse(response)
		xml = WebPage(response.body)
		self.searchdict = dict(xml.parse(['input'],['title','id']))
		self.btn = dict(xml.parse(['button'],['text','id']))
		print("btndict:",self.btn)
		print("searchdict:",self.searchdict)

		event = {
		'eventlist':[
					{"targetId":self.searchdict['Owner'],"value":"=215579-672"},
					{"targetId":self.searchdict['Status'],"value":"=ASSIGNED,=SLAHOLD,=RESOLVED"},
					{"acttype":'click',"targetId":self.btn['Find'] } 
					],
		'currentfocus':self.btn['Find'],
		}
		#,=021943-672,=215210-672,=021262-672,=209884-672
		data = self.postdata(**event)
		return [FormRequest(url=self.url,meta={'data': {}},formdata=data,callback=self.after_search)]

	def after_input_status(self,response):
		xmlparse(response)

		event = {"targetId":self.searchdict['Owner'],"value":"=215579-672",'currentfocus':self.searchdict['Owner']}
		#event = event = {"targetId":"mx400",'acttype': "filterrows",'currentfocus':'mx400'}#1939"mx285",=021943-672,=215210-672,=021262-672,=209884-672,=CLOSED,=RESOLVED
		data = self.postdata(**event)
		return [FormRequest(url=self.url,formdata=data,callback=self.after_input_filter)]

	def after_input_filter(self,response):
		xmlparse(response)
		xml = WebPage(response.body)

		event = {"acttype":'click',"targetId":self.btn['Find'],'currentfocus':self.btn['Find']}
		#event = event = {"targetId":"mx400",'acttype': "filterrows",'currentfocus':'mx400'}#1939"mx285"
		data = self.postdata(**event)
		return [FormRequest(url=self.url,meta={'data': {}},formdata=data,callback=self.after_click_filter)]

	def parse_next_page(self,xml,response):
		import math
		data = [] 
		nextpage =  xml.parse(['img'],['id','alt'])

		nextpage = dict([ (v.split('[')[0].strip(),k) for k,v in nextpage ])

		print("nextpage buttons of list page = ",nextpage)

		total = int(re.search('title="\d{1,10}\s*-\s*\d{1,10}\s*of\s*(\d{1,10})"',xml).group(1))
	
		print("total=",total)
		page = int(math.ceil(total/20) - 1)
		print("page=",page)
		
		for i in range(0,page):
			print 'scrapyed for page:',str(i)
			data = []
			value = "true"
			event = {"targetId":  'mx336','acttype': "click",'value':value,'currentfocus':'mx336'}

			formdata = self.postdata(**event)
			yield  FormRequest(url=self.url,meta={'data': data},formdata=formdata,callback=self.get_next_page,dont_filter=True)

  
	def get_next_page(self,response):
	
		#print type(response),dir(response)
		xml = WebPage(response.body)
		data = response.meta['data']
		print 'Size of data<get_next_page>:',len(data)
		if data:
			data += parse_list(xml)
		else:
			data = parse_list(xml)

		for i,d in enumerate(data):
			p = Person(name=d['Affected Person Name'])
			p.save()
			tf = datetime.datetime.strptime(d['Target Finish'],'%y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
			tt = TicketItem(ticket=d['Incident'],owner=d['Owner Name'],target_finish = tf,summary=d['Summary'],owner_group=d['Owner Group'],priority=d['Internal Priority'],user=p,status=d['Status'])
			yield(tt)

	def save_page(self,data):
		print 'in save-page'
		for i,d in enumerate(data):
			p = Person.objects.filter(name=d['Affected Person Name'])
			if not p:
				p = Person(name=d['Affected Person Name'])
				p.save()
			tf = datetime.datetime.strptime(d['Target Finish'],'%y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
			tt = TicketItem(ticket=d['Incident'],owner=d['Owner Name'],target_finish = tf,summary=d['Summary'],owner_group=d['Owner Group'],priority=d['Internal Priority'],user=p,status=d['Status'])
			yield(tt)

	def after_search(self,response):

		xmlparse(response)
		xml = WebPage(response.body)
		''' 
		sel = Selector(response)
		sel.remove_namespaces()
		print sel.xpath('//a').extract()
		print sel.xpath('//table').extract()
		sites = sel.xpath('//td').extract()
		print sites
		formats= '%y-%m-%d %H:%M:%S'#xmlparse(response)'''
		xml = WebPage(response.body)
		#data = parse_list(xml)
		data = response.meta['data']
		print 'Size of data<get_next_page>:',len(data)
		if data:
			data += parse_list(xml)
		else:
			data = parse_list(xml)

		import math
		
		nextpage =  xml.parse(['img'],['id','alt'])

		nextpage = dict([ (v.split('[')[0].strip(),k) for k,v in nextpage ])

		print("nextpage buttons of list page = ",nextpage)

		current = int(re.search('title="\d{1,10}\s*-\s*(\d{1,10})\s*of\s*\d{1,10}"',xml).group(1))
		print("current=",current)

		if current%20 == 0 :
			print 'scrapyed for page:--------------------------------------------------------------------------',str(int(current/20))
			print 'Size of data<after_click_filter>:',len(data)

			event = {'eventlist':{"targetId":  'mx336','acttype': "click",'value':"true"},'currentfocus':'mx336'}

			formdata = self.postdata(**event)
			yield  FormRequest(url=self.url,meta={'data': data},dont_filter=True,formdata=formdata,callback=self.after_search)
			data = []
			print 'scrapyed for page:===========================================================================',str(int(current/20))
		else:
			for d in data:
				print d['Incident']
				event = {
				'eventlist':[
							{"targetId":"mx85",'value':d['Incident'],"requestType":"ASYNC"},
							{"targetId":"mx85",'acttype': "find"}, 
							],
				"requestType":"ASYNC",
				'currentfocus':"mx85",
				}

				form = self.postdata(**event)

				yield  FormRequest(url=self.url,dont_filter=True,formdata=form,callback=self.after_jmp)


	def jump_to_in(self,response):

		event = {"targetId":"mx85",'acttype': "find"}


		data = self.postdata(**event)

		return [FormRequest(url=self.url,dont_filter=True,formdata=data,callback=self.after_jmp)]

	def convertdate(self,datestr):
		if datestr:
			return datetime.datetime.strptime(datestr.strip(),'%y-%m-%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
		else:
			return None
	def after_jmp(self,response):


		xml = WebPage(response.body)
		data = dict(xml.parse(['input'],['title','value'],VERBOSE = True))
		data = dict( (k.split('：')[0],k.split('：')[1].strip()) if '：' in k else (k,'') if not v else (k.split('：')[0],v.strip()) for k,v in data.items() )
		print data
		d = data

		td = xml.parse(['textarea'],['text'],VERBOSE = True)
		print '-'*30,td,'-'*30
		if td:
			tdetails= xml.parse(['textarea'],['text'],VERBOSE = True)[0][0]
		else:
			tdetails = ''
		
		
		p = Person.objects.filter(name=d['Name'])
		if not p:
			p = Person(name=d['Name'],affected_email=d['Affected E-mail'],reported_email=d['Reported E-mail'])
			p.save()
		else:
			
			p = p[0]
		tf = self.convertdate(d['Target Finish'])
		af = self.convertdate(d['Actual Finish'])
		tt = TicketItem(ticket=d['Incident'],owner=d['Owner'],target_finish = tf,summary=d['Summary'],owner_group=d['Owner Group'],priority=d['Internal Priority'],user=p,status=d['Status'],details=tdetails,actual_finish=af)
		yield(tt)

