# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from lvyou.items import LvyouItem
import re

class LvyouSpiderSpider(scrapy.Spider):
    name = 'lvyou_spider'
    allowed_domains = ['lvyou.baidu.com']
    start_urls = ['http://lvyou.baidu.com/jishou/jingdian/']     #Forbidden by robots.txt

    start_urls = ['https://lvyou.baidu.com/qianzhougucheng/remark/',
                  'https://lvyou.baidu.com/dehang/remark/',
                  'https://lvyou.baidu.com/dehangdizhigongyuan/remark/',
                  'https://lvyou.baidu.com/liushapubu/remark/',
                  'https://lvyou.baidu.com/dehangmiaozhai/remark/',
                  'https://lvyou.baidu.com/xianglushangumiaozhai/remark/',
                  'https://lvyou.baidu.com/baxianhu/remark/']
    # start_urls = ['https://lvyou.baidu.com/qianzhougucheng/remark/']      #单个景点


    def get_scene_name(self,url):
        '''
        从网址中解析出景点的名称
        :param url:
        :return:
        '''
        group = re.findall(r"https://lvyou.baidu.com/(.*)/remark",url)
        scene_name = str(group[0])
        name_dict = {"qianzhougucheng":"乾州古城",
                     "dehang":"德夯",
                     "dehangdizhigongyuan":"德夯地址公园",
                     "liushapubu":"流沙瀑布",
                     "dehangmiaozhai":"德夯苗寨",
                     "xianglushangumiaozhai":"香炉山古苗寨",
                     "baxianhu":"八仙湖"}
        return name_dict[scene_name]

    def parse_remark(self,response):
        '''
        解析评论
        :param response:
        :return:
        '''
        selector = Selector(response)
        item = LvyouItem()
        scene_name = self.get_scene_name(response.url)  # 景点的名称

        numsum = selector.xpath('//*[@id="remark-container"]/div[1]/span/text()').extract()  # 条点评
        # print(numsum[0])
        group = re.findall(r"\d{1,2}", numsum[0])
        remark_acccount = int(group[0])
        print(remark_acccount)

        tags = selector.xpath('//div[@class="remark-item clearfix"]')

        for tag in tags:
            # author = tag.xpath('.//div[1]/a/text()').extract_first()
            author = tag.xpath(
                './/div[@class="ri-avatar-wrap"]//a[@class="ri-uname"]/text()').extract_first()  # 作者暂时爬不出来
            time = tag.xpath(
                './/div[@class="ri-main"]//div[@class="ri-header"]//div[@class="ri-time"]/text()').extract_first()
            remark = tag.xpath('.//div[2]/div[2]/div[1]/text()').extract_first()  # 内部有超链接，内容缺失

            star_text= tag.xpath('.//div[@class="ri-main"]//div[@class="ri-header"]//div[@class="ri-rating"]//div/@class').extract_first()
            group = re.findall(r"ri-star ri-star-(\d)", star_text)   #星级打分，基于AJAX，
            star = str(group[0])

            item['star'] = star
            item['remark'] = remark
            item['time'] = time
            item['remark_acccount'] = remark_acccount
            item['scene_name'] = scene_name
            source = "lvyou_baidu"
            item['source'] = source
            yield item


    def parse(self, response):
        print("网页信息")
        print(response.url)

        selector = Selector(response)
        numsum = selector.xpath('//*[@id="remark-container"]/div[1]/span/text()').extract()   #条点评
        # print(numsum[0])
        group = re.findall(r"\d{1,2}", numsum[0])
        remark_acccount = int(group[0])
        print(remark_acccount)

        #https://lvyou.baidu.com/qianzhougucheng/remark/?rn=15&pn=15&style=hot#remark-container
        # 翻页
        if remark_acccount > 15:
            for i in range(0,remark_acccount,15):
                next_link = response.url + "?rn=15&pn=" + str(i) + "&style=hot#remark-container"
                yield scrapy.Request(next_link,callback=self.parse_remark)
        else:
            index_link = response.url + "?rn=15&pn=0&style=hot#remark-container"
            yield scrapy.Request(index_link, callback=self.parse_remark)





