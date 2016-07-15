#!/usr/bin/env python
#-*- coding:utf-8 -*-
import urllib, urllib2, cookielib
import os,re,sys
from bs4 import BeautifulSoup
import pycurl  
import StringIO,traceback,time
GREEN = u"\033[42m%s\033[m"
BLUE = u"\033[44m%s\033[m"
RED = u"\033[41m%s\033[0m"

def strstrip(string):
		return str(string).split(":")[0].split("(")[0].strip()
def to_unicode(s):
	
	if isinstance(s, str):
		s = unicode(s,'utf-8')
		return s
	elif isinstance(s, unicode):
		return s	
	else:
		return unicode(str(s),'utf-8')
class WebPage(str):
	def __init__(self,xml):
		super(WebPage,self).__init__(xml)
		
	def __new__(cls,*args,**kw):
		return str.__new__(cls,*args,**kw)

	def getxml(self):
		return self
	def search(self,regex):
		try:
			return re.search(regex,self).group(1)
		except	Exception as e:
			#print "Exception:", str(e)
			return ""
	def findall(self,regex):
		return re.findall(regex,self)
	#def parse(self,taglist,namelist =[],options = {}):
	#	return self.parsehtml(self,taglist,namelist,options)
	def get_response_msg(self):
		try:
			msg = re.search("(BMX[^\"'><]*)",self).group(1)
			#debug("msg=",msg)
		except:
			msg = ""
		msg2 = str(self.parse(['label'],['id','title']))
		#debug("msg2:",msg2)
		if 'message' in msg2.lower():
			#info("ERROR OCCURRED, Look into the following msg:")
			return msg2
		else:
			return msg
		

	def get_response_data(self):
		'''if value not null, just use that. or, remove (.*) from title , split by ': ',
		if found two part, and the second part is response data 
		'''
		response = self.parse(['input'],['title','value'])
		responsedata = []
		for k,v in response:
			if v:
				responsedata.append((strstrip(k),v))
			elif len(re.sub('(\([^\)]*\))*','',k).split(': ')) > 1:
				responsedata.append( (strstrip(k),k.split(': ')[1]))
			else:
				responsedata.append( (strstrip(k),""))
		responsedata = dict(responsedata)
		#debug("responsedata",responsedata)
		return responsedata
	def format_num(self,num):
		import locale
		locale.setlocale(locale.LC_NUMERIC, "")

		try:
			inum = int(num)
			return locale.format("%.*f", (0, inum), True)

		except (ValueError, TypeError):
			return to_unicode(num)

	def get_max_width(self,table, index):
		"""Get the maximum width of the given column index"""
		try:
			return max([len(self.format_num(row[index])) for row in table])
		except IndexError:
			return 0

	def get_paddings(self,table):
		col_paddings = []

		for i in range(len(table[0])):
			col_paddings.append(self.get_max_width(table, i))
		return col_paddings

	def tagparse(self,soup,tagname,attlist=[],options = {},VERBOSE=False):
		if soup and attlist and tagname :
			alltag = soup.findAll(tagname,options)
			length = len(alltag)
			#debug("len of %s"%tagname,length)
			if length == 0:
				return []
			if VERBOSE:
				for i in range(len(alltag)):
					try:
						#debug("Available attribute of tag:","")
						for att in alltag[i].attrs:
							#print att,
							print '',
						print
						break
					except:
						pass
			table = []
			header = [ ]
			maxheader = attlist[:]
			maxheader = [ x.upper() for x in maxheader]
			table.append(maxheader)
			for i,tag in enumerate(alltag):
				row = []
				for att in attlist:
					if tag.has_attr(att):
						row.append(tag[att].strip())
						#debug("tag[att]:",tag[att])
					else:
						nestatt = ''
						for subtag in  tag.findChildren(recursive=True):
							if  subtag.has_attr(att):
						
								nestatt = subtag[att].strip()
						if att.lower() == 'text':
							#debug("tag.text:",tag.name)
							nestatt=tag.text.strip()
						#debug("nestatt:",nestatt)
						row.append(nestatt)
			
				table.append(tuple(row))
			colwidth = self.get_paddings(table)
			#debug("colwidth:")
			#print colwidth
			if VERBOSE:
				if len(table) > 1:
					print '-'*20 + tagname + '-'*20
					for r,row in enumerate(table):
						if len(filter(None, row)) != 0:
							print r,
							for i in range(0, len(row)):
								width = colwidth[i]
								if width != 0:
									col = row[i].ljust(width )
									print col,
							print 
			del table[0]
			return table
		elif soup and tagname:
			alltag = soup.findAll(tagname,options)
			puretag = []
			for tag in alltag:
				#debug("pure tag=",tag)
				puretag.append(tag)
			return puretag

	def parse(self,taglist,attlist=[],options = {},VERBOSE=False):
		#debug('taglist',str(taglist))
		
		html = self
		if html and taglist:
			#to perserve CDATA
			html = re.sub(r'<!\[CDATA\[([^\]]*)\]\]',"\g<1>",html)
			soup = BeautifulSoup(html,'lxml')
			result =[]
			for tag in taglist:
			
				result.append(self.tagparse(soup,tag.lower(),attlist,options,VERBOSE))
			if len(result) == 1:
				return result[0]
			else:
				return result
		else:
			raise Exception("NO HTML found or tag list is nothing!")

import httplib, ssl,socket

class HTTPSConnectionV3(httplib.HTTPSConnection):
	def __init__(self, *args, **kwargs):
		
		httplib.HTTPSConnection.__init__(self, *args, **kwargs)
		
	def connect(self):
		sock = socket.create_connection((self.host, self.port), self.timeout)
		if self._tunnel_host:
			self.sock = sock
			self._tunnel()
		try:
			self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv3)
		except ssl.SSLError, e:
			print("Trying SSLv3.")
			self.sock = ssl.wrap_socket(sock, self.key_file, self.cert_file, ssl_version=ssl.PROTOCOL_SSLv23)
		
class HTTPSHandlerV3(urllib2.HTTPSHandler):
	def https_open(self, req):
		
		return self.do_open(HTTPSConnectionV3, req)

def test(debug_type, debug_msg):
	print "debug(%d): %s" % (debug_type, debug_msg)
def to_string(s):
	if isinstance(s, str):
		return s
	elif isinstance(s, unicode):
		return s.encode("utf-8")
	else:
		return str(s)
class Requests:
	savepath = []
	cookieFile = './cookie.dat' 
	def __init__(self,savepath =[], VERBOSE=False,DEBUG=False,dryrun = False,XML="XML"): 
		
		self.savepath = savepath
		self.dry  = dryrun
		self.verbose = VERBOSE
		self.DEBUG = DEBUG
		self.XML= XML
		self.response =""
		self.cookie=cookielib.LWPCookieJar(self.cookieFile)
		self.cookieload=False
		self.html = ""
		self.debug("Flag:",str([VERBOSE,DEBUG,dryrun]))
		if os.path.isfile(self.cookieFile):
			try:
				self.cookie.load(ignore_discard=True)
				self.cookieload=True
			except Exception, e:
				self.debug( "Exception:",str(e))
				traceback.print_exc()
		self.debug('cookieload:',str(self.cookieload))

		if self.DEBUG:

			opener = urllib2.build_opener(HTTPSHandlerV3(debuglevel=1),urllib2.HTTPHandler(debuglevel=1),urllib2.HTTPCookieProcessor(self.cookie)) 
		else:
			opener = urllib2.build_opener(HTTPSHandlerV3(debuglevel=0),urllib2.HTTPHandler(debuglevel=0),urllib2.HTTPCookieProcessor(self.cookie)) 
		urllib2.install_opener(opener)
		self.base_init()
		self.c = pycurl.Curl()  
		self.c.setopt(pycurl.COOKIEFILE, 'cookie.txt')
		self.c.setopt(pycurl.COOKIEJAR, 'cookie.txt')  
		self.downloaded = 0

	def debug(self,msg,data=""):
		if self.DEBUG : 
			if data and isinstance(data,dict) :  
				print u"\033[41mDEBUG:%s\033[0m"%(msg)
				for k,v in sorted(data.iteritems(), key=lambda (k,v): v if v else k ):
		
					print u"\033[44m%s:%s\033[m"%(k.ljust(34),v)

			elif data and isinstance(data,list):
				print u"\033[41mDEBUG:%s\033[m"%(msg)
				for i in sorted(data):
					print BLUE%(str(i))
			else:
				print u"\033[41mDEBUG:%s\033[m"%(msg),
				print BLUE%(data)

	def find(self,pattern, path="."):
		import fnmatch
		result = []
		for root, dirs, files in os.walk(path):
			for name in files:
				if fnmatch.fnmatch(name, pattern):
				    result.append(os.path.join(root, name))
		return result

	def get_local_xml(self,filename,savepath = [] ):
		if not savepath:
			savepath = self.savepath
		try:
			self.debug("path=",str(savepath))
			path = self.XML + ''.join( "/" + i if i else '' for i in savepath)
			self.debug("local path of XML:",path)
			local_xml = self.find(filename+".*",path)[0]
			self.debug("Loading local : ", local_xml)
			return WebPage(open(local_xml).read())
		except IndexError:
			raise Exception("No local xml found! You shoull run every action upon server before dry run from local")

	def base_init(self):

		if not os.path.exists(self.XML):
			os.makedirs(self.XML)
		
	def save_xml(self,caller,savepath =[]):
		self.savepath = savepath
		xml = self.html
		try:
			ctype = self.response.info().getheader('Content-Type')
		except:
			ctype = self.response.getinfo(self.response.CONTENT_TYPE)
			
		ctype = ctype.split(";")[0].split("/")[1]
		self.debug('Content-Type',ctype)
		fullsavepath = self.savepath + [caller]
		self.debug("fullsavepath:",str(fullsavepath))
		filename = self.XML + ''.join( "/" + i if i else '' for i in fullsavepath)  + "." +  ctype
		self.debug("local filename of XML:",filename)
		if not os.path.exists(os.path.dirname(filename)):
			os.makedirs(os.path.dirname(filename))
		with open(filename,'wb') as f:
			if ctype in ['xml','html']:
				xml = re.sub(r'<!\[CDATA\[([^\]]*)\]\]',"\g<1>",xml)
				xml = BeautifulSoup(xml).prettify().decode('string-escape')
			self.debug("write reponse content :%s "%filename)
			f.write(xml)
	def get_header(self,url,caller="Unknown",header={},path=[]):
		self.savepath = path
		self.debug("Requests is being called by",caller)
		
		if not self.dry:
			self.debug('posting URL:',url)
			self.debug('Posting Header:',header)
			
			header = [ str(k + ':'+ v) for k,v in header.items() ] 
			header = header + [ "Expect:" ] 

			buf = StringIO.StringIO() 
			hbuf = StringIO.StringIO() 
			
			self.c.setopt(pycurl.WRITEFUNCTION, buf.write)
			self.c.setopt(pycurl.HEADERFUNCTION, hbuf.write)  
			
			self.c.setopt(pycurl.URL, to_string(url))
  			self.c.setopt(pycurl.FOLLOWLOCATION, False) 
			if self.DEBUG:
				self.c.setopt(pycurl.VERBOSE, 1)

			if header:
				self.c.setopt(pycurl.HTTPHEADER, header)  
			try:
				self.c.perform()  
			except pycurl.error, error:
				errno, errstr = error
				print 'We failed to reach a server.'
				raise Exception('Reason: '+ str(errstr))
			reheader = hbuf.getvalue()
			self.response  = self.c
			self.html = html
			buf.close
			hbuf.close
		else:
			
			reheader = self.get_local_xml(caller)
		return reheader

	def request2(self,url,post,caller="Unknown",header={},path=[]):
		self.savepath = path
		self.debug("Requests is being called by",caller)
		
		if not self.dry:
			self.debug('posting URL:',url)
			self.debug('Posting Header:',header)
			
			header = [ str(k + ':'+ v) for k,v in header.items() ] 
			header = header + [ "Expect:" ] 

			buf = StringIO.StringIO() 
			hbuf = StringIO.StringIO() 
			

			self.c.setopt(pycurl.WRITEFUNCTION, buf.write)
			self.c.setopt(pycurl.HEADERFUNCTION, hbuf.write)  
			
			self.c.setopt(pycurl.URL, to_string(url))
  			self.c.setopt(pycurl.FOLLOWLOCATION, True) 
			self.c.setopt(pycurl.MAXREDIRS, 5) 
			#self.c.setopt(pycurl.NOPROGRESS, 0)
			#self.c.setopt(pycurl.PROGRESSFUNCTION, self.progress)
			if self.DEBUG:
				self.c.setopt(pycurl.VERBOSE, 1)
			#if self.verbose:
			#	self.c.setopt(pycurl.DEBUGFUNCTION, test)
			if header:
				self.c.setopt(pycurl.HTTPHEADER, header)  
			if post:
				self.debug('Posting data:',post)
				if isinstance(post,dict):
					postdata = urllib.urlencode(post) 
				else:
					postdata = post
				self.c.setopt(pycurl.POST, 1)
				 
				self.c.setopt(pycurl.POSTFIELDS,  postdata)  
			try:
				self.c.perform()  
			except pycurl.error, error:
				print dir(pycurl.error)
				errno, errstr = error
				print 'We failed to reach a server.'
				raise Exception('Reason: '+ str(errstr))
			
			html = WebPage(buf.getvalue())
			 

			self.response  = self.c
			self.html = html
			#self.debug("cookie",hbuf['Set-Cookie'])
			for index, cookie in enumerate(self.cookie):
				self.debug("cookie", str(index) + ': ' + str(cookie))

			
			buf.close
			hbuf.close
		else:
			
			html = self.get_local_xml(caller)
			
		if self.verbose and html:
			
			html.parse(['input','button','a','li','img','span','label','textarea'],['id','name','title','ae','ev','alt','href','value'],VERBOSE = self.verbose)

		return html 
		
	def progress(self,download_total,downloaded,uploaded_total,upload):
		'''
		Function to display the progress
		'''
		if download_total and downloaded :
			time.sleep(1)
			print "Speed: " + str(downloaded - self.downloaded)
			if download_total > 0 :
				print "Percentage: " + str(downloaded/download_total*100)
			#print "Downloaded : " + str(downloaded)
			self.downloaded = downloaded


	def request(self,url,post,caller="Unknown",header={},path=[]):
		self.savepath = path
		self.debug("Requests is being called by",caller)
		
		if not self.dry:
			self.debug('posting URL:',url)
			self.debug('Posting Header:',header)

			if post:
				if isinstance(post,dict):
					postdata = urllib.urlencode(post) 
				else:
					postdata = post
				req = urllib2.Request(url, data=postdata,headers=header)  
				  

			else:
				self.debug('Gets Header:',header)
				req = urllib2.Request(url,headers=header) 
			try: 
				response = urllib2.urlopen(req)
				result = response.read().decode('utf-8') 
				ctype = response.info().getheader('Content-Type')
				ctype = ctype.split(";")[0].split("/")[1]
				self.debug("ctype",ctype)
				if ctype in ['html','xml']:
					self.debug("ctype",ctype)
					result = re.sub(r'<!\[CDATA\[([^\]]*)\]\]',"\g<1>",result)
					result = WebPage(BeautifulSoup(result).prettify().decode('string-escape'))
				else:
					result = WebPage(result)
			except  urllib2.URLError as e:
	
				if hasattr(e, 'reason'):
					print 'We failed to reach a server.'
					raise Exception('Reason: '+ str(e.reason))
				elif hasattr(e, 'code'):
					print 'The server couldn\'t fulfill the request.'
					print (result.get_response_msg())
					print ('Error code: ', str(e.code))
					raise Exception("HTTPError :" + str(e.read()))
				else:
					raise Exception("unhandled error")
			self.response  = response
			self.html = result
			self.debug("cookie",response.headers.get('Set-Cookie'))
			for index, cookie in enumerate(self.cookie):
				self.debug("cookie", str(index) + ': ' + str(cookie))

			self.cookie.save(ignore_discard=True)

		else:
			
			result = self.get_local_xml(caller)
			
		if self.verbose and result:
			
			result.parse(['input','button','a','li','img','span','label'],['id','name','title','ae','ev','alt','href','value'],VERBOSE = self.verbose)

		return result 


class downloader:
	def __init__(self,target_address,output_file,proxy=None):

		######## Set variables of the downloader ########
		self.output_file=output_file	# Downloaded file is stored here
		self.chunk=1*1024*1024				# Define the chunk size to be downloaded at once
		#################################################
		try:
			self.dir_name=self.output_file+"tmp"
			os.mkdir(self.dir_name)
		except OSError:
			pass
		######### Set the target of the Curl object ######

		self.curl_obj=pycurl.Curl()		# Initializing CURL object
		self.curl_obj.setopt(self.curl_obj.URL,to_string(target_address))	# Setting the target
		self.curl_obj.setopt(pycurl.VERBOSE, 1)
		if proxy != None:
			self.curl_obj.setopt(pycurl.PROXY,proxy)	# This should be set as "http://<username>[:<password>]@<proxy-host>[:<proxy-port>]"

		#################################################

		##### Set the size of the file to be downloaded ######
		# Create a temporary curl object to get the information
		tmp_curl_obj=pycurl.Curl()
		tmp_curl_obj.setopt(tmp_curl_obj.URL,to_string(target_address))	# Setting the target
		if proxy != None:
			self.curl_obj.setopt(pycurl.PROXY,proxy)	# This should be set as "http://<username>[:<password>]@<proxy-host>[:<proxy-port>]"
		# Set NO-body download to true
		tmp_curl_obj.setopt(tmp_curl_obj.NOBODY,True)
		#self.curl_obj.setopt(self.curl_obj.USERAGENT,"Mozilla/5.0 (compatible; pycurl)")
		# Send request
		try:
			print "Trying to get size of the file"
			tmp_curl_obj.perform()
			# get the size
			self.size = tmp_curl_obj.getinfo(tmp_curl_obj.CONTENT_LENGTH_DOWNLOAD)
		except Exception, e:
			print e
			self.delete_temp()
			self.size = 0
			#sys.exit (2)

		######## Set the progress function #############
		self.curl_obj.setopt(self.curl_obj.NOPROGRESS,1)
		self.curl_obj.setopt(self.curl_obj.PROGRESSFUNCTION,self.progress)


	def download(self):

		if (self.size>0):
			print "Starting download. Total size: "+str(self.size)+" bytes or "+str(self.size/1024/1024)+" MB"
		else:
			print "Starting download"
		# Download straight-away if the size is less than the limit

		if self.size <=self.chunk or self.size<0:
		# Set the output file
			self.curl_obj.fp = open(self.output_file, "wb")
			self.curl_obj.setopt(pycurl.WRITEDATA, self.curl_obj.fp)
			self.curl_obj.perform()
			self.delete_temp()
			sys.exit()


		# All errors are logged in the logfile
		log=open("/var/log/downloader.log","a")		# Opened in append mode (maintains all logs)

		num_proc=10				# This variable decides the number of concurrent processes.

		pid=[]					# This stores the list of PIDs of the children (processes)

		self.curl_obj.setopt(pycurl.TIMEOUT,60*10)	# Limits the maximum download time per download-connection to 10 minutes (This could be changed for slower connections)


		lim_l=0					# lower limit of the byte-range for download
		lim_u=self.chunk		# upper limit of the byte-range for download
		i=1
		while lim_l<=self.size :

			# Create a temporary filename
			temp_output=os.path.join(self.dir_name,"output"+str(i))
			#print temp_output
			# Ensure that it doesn't already exists
			# If it exists and its size is the same as that of the chunk downloaded each time, then go to the next chunk
			if os.path.exists(temp_output) and os.path.getsize(temp_output)==self.chunk:
				#print str(i)+" MB already downloaded"
				i=i+1
				r=str(lim_l)+"-"+str(lim_u-1)
				#print r
				lim_l=lim_l+self.chunk
				lim_u=lim_u+self.chunk
				continue

			self.curl_obj.fp = open(temp_output, "wb")		# Handle to the file to be written to.
			self.curl_obj.setopt(pycurl.WRITEDATA, self.curl_obj.fp) # Sets the pycurl option to write to the file

			# Define the range
			#print lim_l
			#print lim_u
			r=str(lim_l)+"-"+str(lim_u-1)
			#print r
			# Set the range
			self.curl_obj.setopt(pycurl.RANGE,r)

			# Create a child process
			tpid=os.fork()

			if tpid==-1:
				print "error"
			if tpid==0 :
				# Inside the child


					while True:
						try:
							# Start downloading
							self.curl_obj.perform()
							# print "Downloaded "+str(i)+" MB of "+str(self.size/(1024*1024)) + " MB"
							self.curl_obj.fp.close()	# Close the file
							break
						except pycurl.error, e:
							# Catch the error while downloading a file
							# and restart the download of the particular file

							# print "Pycurl error caught"
							log.write("Pycurl error caught "+str(e)+" while downloading at download range "+str(r)+" while storing to file "+str(temp_output)+"\n")

							# Close the existing file and reopen (otherwise data would be appended)
							self.curl_obj.fp.close()
							self.curl_obj.fp=open(temp_output,"wb")

							continue # Continues the loop

					exit()		# Exits the child process





			if tpid>0 :
				# In the parent
				pid.append(tpid)

			if len(pid)>num_proc-1:

				# This ensures that only the required number (num_proc) of child processes run at once

				(cpid,exitstatus)=os.wait()		# Wait for any child to exit

				#if not exitstatus==0:
					# If exit status is non-zero, implies a file smaller than the required is downloaded,
					# Hence (either the downloaded has ended, or error)
					# Stop any new downloads
					# TODO : Introduce provision to handle network errors
					#pid.remove(cpid)
					#print "breaking"
					#break
				#pid.remove(cpid)				# remove that child from the list

			# Define lower and upper limit of the next range.
			lim_l=lim_l+self.chunk
			lim_u=lim_u+self.chunk
			#self.print_percentage(i)
			i=i+1




		while len(pid)>0:
			# wait for all sub-processes to exit
			try:
				(cpid,exitstatus)=os.wait()		# wait for child to exit
				pid.remove(cpid)				# remove that child from the list
			except OSError:
				# Arises when children have already exit.
				break



	def concatenate(self):

		# Concatenate the files to finally create the desired output

		# TODO : Check that the file doesn't already exist

		# Open file in write mode (and close) to over-write any existing file
		# with same name
		fp=open(self.output_file,'w')
		fp.close()

		i=1
		while True:
			temp_output=os.path.join(self.dir_name,"output"+str(i))
			#print temp_output
			if os.path.exists(temp_output):

				# Open file to append to
				fp=open(self.output_file,'a')

				# Open the temporary file to read from
				tp=open(temp_output,"r")

				# Append to the output_file
				fp.write(tp.read())

				# Close files
				tp.close()
				fp.close()

				if os.path.getsize(temp_output)==self.chunk:
					i=i+1		# Increase only if the file size is equal to the chunk size
				else:
					break		# this takes care of redundant files downloaded

		fp.close()


	def delete_temp(self):

		# Remove the temporary files created
		i=1
		while True:
			temp_output=os.path.join(self.dir_name,"output"+str(i))
			#print temp_output
			if os.path.exists(temp_output):
				os.remove(temp_output)
			else:
				break
			i=i+1

		try:
			os.rmdir(self.dir_name)
		except Exception, e:
			pass


	def progress(self,download_total,downloaded,uploaded_total,upload):
		'''
		Function to display the progress
		'''
		print "To be downloaded" + str(download_total)
		print "Downloaded : " + str(downloaded)
