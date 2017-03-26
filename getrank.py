from lxml import html
import requests
import cv2
import csv

page = requests.get('https://www.thebluealliance.com/event/2017njtab#rankings')
tree = html.fromstring(page.content)
#print tree.xpath('//table[@id="rankingsTable"]/text()')
content =  [td.text_content().replace(" ","").replace("\n","") for td in tree.xpath('//table[@id="rankingsTable"]//thead//tr//th')]
#print len([td.text_content() for td in tree.xpath('//table[@id="rankingsTable"]//thead//tr//th//div')])

with open("ranking.txt", 'wb') as csvfile:
	csvWrite = csv.writer(csvfile, dialect='excel', delimiter=',')

	chunks = lambda content, n=12: [content[i:i+n] for i in range(0, len(content), n)]
	chunklen = 12
	for i in chunks(content):
		csvWrite.writerow(i)


	content =  [td.text_content().replace(" ","").replace("\n","") for td in tree.xpath('//table[@id="rankingsTable"]//tbody//tr//td')]
	#print len([td.text_content() for td in tree.xpath('//table[@id="rankingsTable"]//tbody//tr//td')])
	chunks = lambda content, n=12: [content[i:i+n] for i in range(0, len(content), n)]
	chunklen = 12
	for i in chunks(content):
		csvWrite.writerow(i)
