import urllib,urllib2
import threadpool
from lxml import etree
import codecs

base_url = 'http://pc5.sj.91.com/appnew/detail?f_id='
file = codecs.open('tag_2.csv', 'w', 'utf-8')

  
def spider(f_id):
	global base_url
	global file
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
		file.write(str(f_id)+","+app_name+","+child_tag+"\n")
  
def main():
	#global file
	start = 41700000
	end = 41700000
	step = 10000
	
	while(end<43000000):
		end = end+step
		pool = threadpool.ThreadPool(30) 
		requests = threadpool.makeRequests(spider, range(start,end))  
		[pool.putRequest(req) for req in requests]  
		pool.wait()
		#file.close()
		start = end
if __name__ == '__main__':
	main()
