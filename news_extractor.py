import urllib2
from lxml import etree
import pymysql
import timestring

#connect to the database
connection = pymysql.connect(host='localhost',
				user='root',
				password='password',
				db='stock_db')

#stock symbol you want to download news for
symbol = "SPY"

#this is the url where we grab the data
url_stub = "http://www.google.com/finance/company_news?output=rss&q="

#use urllib2 to download the data
response = urllib2.urlopen(url_stub + symbol)
xml = response.read()

#turn into an xml doc
doc = etree.fromstring(xml)
#we're only interested in tags under <item>
item_tags = doc.xpath('//channel/item')
for item in item_tags:
	#split up by the four tags
	date_tag = item.xpath('pubDate')
	title_tag = item.xpath('title')
	link_tag = item.xpath('link')
	description_tag = item.xpath('description')
	
	date_text = date_tag[0].text
	title_text = title_tag[0].text
	link_text = link_tag[0].text
	description_text = description_tag[0].text

	print 'date:' + date_text
	print 'title:' + title_text
	print 'link:' + link_text
	print 'description:' + description_text
	
	#insert into the database
	with connection.cursor() as cursor:
		sql = "INSERT INTO `stocknews` (`symbol`, `pubDate`, `title`, `link`, `description`) VALUES (%s, %s, %s, %s, %s)"
		cursor.execute(sql, (symbol, str(timestring.Date(date_text)), title_text, link_text, description_text))
	connection.commit()
