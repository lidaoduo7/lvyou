# -*- coding: utf-8 -*-

from scrapy import cmdline


'''

scrapy crawl lvyou_spider
scrapy crawl lvyou_spider -o test.json
scrapy crawl lvyou_spider -o test.csv
'''



cmdline.execute("scrapy crawl lvyou_spider".split())