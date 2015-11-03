# -*- coding: utf-8 -*-
import urllib,urllib2
import threadpool
from lxml import etree
import codecs

tag_dict_base_url = 'http://pc5.sj.91.com/appnew/'

base_url = 'http://pc5.sj.91.com/appnew/detail?f_id='
file = codecs.open('tag.csv', 'w', 'utf-8')

tag_dict={}

def dict_generator():
	my_url = tag_dict_base_url+"category.aspx"
	req = urllib2.Request(my_url) 
	response = urllib2.urlopen(req) 
	
	the_page = response.read()
	root = etree.HTML(the_page)
	parent_tag_dl = root.xpath("//dl[contains(@class,'category-item')]")[0]
	
	parent_tag_a = parent_tag_dl.xpath('dd/a/text()')
	parent_tag_href = parent_tag_dl.xpath('dd/a/@href')
	
	for i in range(0,len(parent_tag_a)):
		child_tag_spider(parent_tag_a[i],parent_tag_href[i])
	
	
def child_tag_spider(parent_tag,parent_href):
	my_url = tag_dict_base_url+parent_href
	req = urllib2.Request(my_url) 
	response = urllib2.urlopen(req) 
	
	the_page = response.read()
	root = etree.HTML(the_page)
	child_tag_dl = root.xpath("//dl[contains(@class,'category-item')]")[1]
	
	child_tag_a = child_tag_dl.xpath('dd/a/text()')
	for child_tag in child_tag_a:
		tag_dict[child_tag] = parent_tag
	
	
  
def main_spider(f_id):
	global base_url
	global file
	global dict
	my_url = base_url + str(f_id)
	req = urllib2.Request(my_url) 
	response = urllib2.urlopen(req) 
	the_page = response.read()
	print f_id
	if ("SoftNotFound" in response.url):
		return
	else:
		root = etree.HTML(the_page)
		app_name = root.xpath("//div[@class='s-fix-title']/span/text()")[0]
		child_tag = root.xpath("//div[@class='o-tip']/text()")[1].strip()[3:]
		if(tag_dict.has_key(child_tag)):
			file.write(str(f_id)+","+app_name+","+child_tag+","+tag_dict[child_tag].encode('utf-8').decode('utf-8')+"\n")
		else:
			file.write(str(f_id)+","+app_name+","+child_tag+","+u"\u5176\u4ed6"+"\n")
  
def main():
	#global file
	dict_generator()
	
	start = 40000000
	end = 40000000
	step = 10000
	
	while(end<=50000000):
		end = end+step
		pool = threadpool.ThreadPool(30) 
		requests = threadpool.makeRequests(main_spider, range(start,end))  
		[pool.putRequest(req) for req in requests]  
		pool.wait()
		#file.close()
		start = end

if __name__ == '__main__':
	main()