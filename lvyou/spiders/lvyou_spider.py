# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from lvyou.items import LvyouItem
import re
import requests

class LvyouSpiderSpider(scrapy.Spider):
    name = 'lvyou_spider'
    allowed_domains = ['lvyou.baidu.com']
    # start_urls = ['http://lvyou.baidu.com/jishou/jingdian/']     #Forbidden by robots.txt

    start_urls = ['https://lvyou.baidu.com/qianzhougucheng/remark/',
                  'https://lvyou.baidu.com/dehang/remark/',
                  'https://lvyou.baidu.com/dehangdizhigongyuan/remark/',
                  'https://lvyou.baidu.com/liushapubu/remark/',
                  'https://lvyou.baidu.com/dehangmiaozhai/remark/',
                  'https://lvyou.baidu.com/xianglushangumiaozhai/remark/',
                  'https://lvyou.baidu.com/baxianhu/remark/']
    # start_urls = ['https://lvyou.baidu.com/qianzhougucheng/remark/']      #单个景点

    def parse(self, response):
        print("网页信息")
        print(response.url)

        selector = Selector(response)
        item = LvyouItem()
        numsum = selector.xpath('//*[@id="remark-container"]/div[1]/span/text()').extract()   #条点评
        # print(numsum[0])
        group = re.findall(r"\d{1,3}", numsum[0])
        remark_acccount = int(group[0])
        # print(remark_acccount)

        # https://lvyou.baidu.com/qianzhougucheng/remark/?rn=15&pn=15&style=hot#remark-container
        # 翻页
        # remarks = []
        # if remark_acccount > 15:
        #     for i in range(0, remark_acccount, 15):
        #         next_link = response.url + "?rn=15&pn=" + str(i) + "&style=hot#remark-container"
        #         remark_page = self.get_remark(requests.get(next_link))
        #         remarks.extend(remark_page)
        # else:
        #     remarks = self.get_remark(response)

        remarks = self.get_remark(response)    #每个景点只爬取最多15条评论
        # print(type(remarks))

        remarks_list = []
        for i in range(len(remarks)):
            remark_time = remarks[i][0]
            remark = remarks[i][1]
            comments_dict = {'comment_time': remark_time, 'remark': remark}
            remarks_list.append(comments_dict)
        item['remarks'] = remarks_list

        scene_name = self.get_scene_name(response.url)  # 景点的名称
        source = "website"
        item['source'] = source
        second_source = "lvyou_baidu"
        item['second_source'] = second_source
        item['remark_acccount'] = remark_acccount
        item['scene_name'] = scene_name
        yield item

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

    def get_remark(self,response):
        '''

        :param response:
        :return:
        '''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        }
        selector = Selector(response)
        numsum = selector.xpath('//*[@id="remark-container"]/div[1]/span/text()').extract()  # 条点评
        # print(numsum[0])
        group = re.findall(r"\d{1,3}", numsum[0])
        remark_acccount = int(group[0])
        tags = selector.xpath('//div[@class="remark-item clearfix"]')
        results = []
        for tag in tags:
            author = tag.xpath(
                './/div[@class="ri-avatar-wrap"]//a[@class="ri-uname"]/text()').extract_first()  # 作者暂时爬不出来
            time = tag.xpath(
                './/div[@class="ri-main"]//div[@class="ri-header"]//div[@class="ri-time"]/text()').extract_first()
            # remark = tag.xpath('.//div[2]/div[2]/div[1]/text()').extract_first()  # 评论内容，内部有超链接，内容缺失
            remark_lsts = tag.xpath('.//div[2]/div[2]/div[1]/text()').extract()
            remark = ""
            for every_remark in remark_lsts:
                remark += every_remark
            star_text = tag.xpath(
                './/div[@class="ri-main"]//div[@class="ri-header"]//div[@class="ri-rating"]//div/@class').extract_first()
            group = re.findall(r"ri-star ri-star-(\d)", star_text)  # 星级打分，基于AJAX，暂时爬不出来
            star = str(group[0])
            results.append((time, str(remark)))
        return results


    # def parse_remark(self,response):
    #     '''
    #     解析评论
    #     :param response:
    #     :return:
    #     '''
    #     selector = Selector(response)
    #     item = LvyouItem()
    #     scene_name = self.get_scene_name(response.url)  # 景点的名称
    #
    #     numsum = selector.xpath('//*[@id="remark-container"]/div[1]/span/text()').extract()  # 条点评
    #     # print(numsum[0])
    #     group = re.findall(r"\d{1,2}", numsum[0])
    #     remark_acccount = int(group[0])
    #     # print(remark_acccount)
    #
    #     tags = selector.xpath('//div[@class="remark-item clearfix"]')
    #     results = []
    #     for tag in tags:
    #         author = tag.xpath(
    #             './/div[@class="ri-avatar-wrap"]//a[@class="ri-uname"]/text()').extract_first()  # 作者暂时爬不出来
    #         time = tag.xpath(
    #             './/div[@class="ri-main"]//div[@class="ri-header"]//div[@class="ri-time"]/text()').extract_first()
    #         remark = tag.xpath('.//div[2]/div[2]/div[1]/text()').extract_first()  # 评论内容，内部有超链接，内容缺失
    #
    #         star_text= tag.xpath('.//div[@class="ri-main"]//div[@class="ri-header"]//div[@class="ri-rating"]//div/@class').extract_first()
    #         group = re.findall(r"ri-star ri-star-(\d)", star_text)   #星级打分，基于AJAX，暂时爬不出来
    #         star = str(group[0])
    #         results.append((time,remark))
    #         # https://lvyou.baidu.com/qianzhougucheng/remark/?rn=15&pn=15&style=hot#remark-container
    #         # 翻页
    #         if remark_acccount > 15:
    #             for i in range(0, remark_acccount, 15):
    #                 next_link = response.url + "?rn=15&pn=" + str(i) + "&style=hot#remark-container"
    #                 yield scrapy.Request(next_link, callback=self.parse_remark)  # 超过15条评论的会写入多次
    #         else:
    #             # index_link = response.url + "?rn=15&pn=0&style=hot#remark-container"
    #             # yield scrapy.Request(index_link, callback=self.parse_remark)
    #             pass
    #
    #
    #     remarks_list = []
    #     for i in range(len(results)):
    #         remark_time = results[i][0]
    #         remark = results[i][1]
    #         comments_dict = {'comment_time': remark_time, 'remark': remark}
    #         remarks_list.append(comments_dict)
    #     # item['remarks'] = remarks_list
    #
    #     source = "website"
    #     item['source'] = source
    #     second_source = "lvyou_baidu"
    #     item['second_source'] = second_source
    #     item['remark_acccount'] = remark_acccount
    #     item['scene_name'] = scene_name
    #     yield item









