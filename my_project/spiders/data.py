# -*- coding: utf-8 -*-
import os
import re

import scrapy
from scrapy.http.response.html import HtmlResponse


class DataSpider(scrapy.Spider):
    marketMaxPageNumber=1
    blogMaxPageNumber=1
    securityMaxPageNumber=1
    mainMaxPageNumber=1
    name = 'data'
    allowed_domains = ['finance.sina.com.cn','blog.sina.com.cn']
    start_urls = ['http://finance.sina.com.cn/stock/jyts',#交易提示
                  "http://finance.sina.com.cn/roll/index.d.html?cid=56605",#市场研究
                  "http://finance.sina.com.cn/roll/index.d.html?cid=56615",#主力动向
                  "http://finance.sina.com.cn/roll/index.d.html?cid=230808",#证券自媒体综合
                  "https://finance.sina.com.cn/roll/index.d.html?cid=57563",#博客
                  ]  # 起始url，从第一页开始爬取

    paths=["交易提示","博客","市场研究","主力动向","证券自媒体综合"]
    for path in paths:
        path=path+".txt"
        if os.path.exists(path):  # 如果文件存在
            os.remove(path)
    def parse(self, response: HtmlResponse):
        cateGory=response.xpath("//h2/text()").extract_first()
        if cateGory=="交易提示":
            vals = response.xpath("//ul[@class='list_009']/li/a/@href").extract()
            for v in vals:
                yield scrapy.Request(v, callback=self.parseTrading)
        elif cateGory=="博客":
            vals=response.xpath("//ul[@class='list_009']/li/a[1]/@href").extract()
            for v in vals:
                yield scrapy.Request(v, callback=self.parseBlog)
            nextPage = response.xpath("//span[@class='pagebox_next']/a/@href").extract_first()
            if nextPage is not None:
                if int(nextPage.split("page=")[1]) > self.blogMaxPageNumber:
                    return
                # if "page=10" in nextPage:
                #   return
                yield scrapy.Request(nextPage, callback=self.parse)
        elif cateGory=="市场研究":
            vals=response.xpath("//ul[@class='list_009']/li/a/@href").extract()
            for v in vals:
                yield scrapy.Request(v,callback=self.parseMarket)
            nextPage = response.xpath("//span[@class='pagebox_next']/a/@href").extract_first()
            if nextPage is not None:
                if int(nextPage.split("page=")[1]) > self.marketMaxPageNumber:
                    return
                # if "page=10" in nextPage:
                #   return
                yield scrapy.Request(nextPage, callback=self.parse)
        elif cateGory=="主力动向":
            vals=response.xpath("//ul[@class='list_009']/li/a/@href").extract()
            for v in vals:
                yield scrapy.Request(v,callback=self.parseMain)
            nextPage = response.xpath("//span[@class='pagebox_next']/a/@href").extract_first()
            if nextPage is not None:
                if int(nextPage.split("page=")[1]) > self.mainMaxPageNumber:
                    return
                # if "page=10" in nextPage:
                #   return
                yield scrapy.Request(nextPage, callback=self.parse)
        elif cateGory == "证券自媒体综合":
            vals = response.xpath("//ul[@class='list_009']/li/a/@href").extract()
            for v in vals:
                yield scrapy.Request(v, callback=self.parseSecurity)
            nextPage = response.xpath("//span[@class='pagebox_next']/a/@href").extract_first()
            if nextPage is not None:
                if int(nextPage.split("page=")[1]) > self.securityMaxPageNumber:
                    return
                # if "page=10" in nextPage:
                #   return
                yield scrapy.Request(nextPage, callback=self.parse)


    def parseTrading(self,response: HtmlResponse):
        info=response.xpath("//div[@class='date-source']/span/text()").extract()
        if len(info)!=2:
            return
        time=info[0]
        type=info[1]
        title=response.xpath("//h1/text()").extract_first()
        contents=response.xpath("//div[@class='article']/p/text()").extract()
        content=re.sub('\s', ' ', "".join(contents))
        dict={
            "title":title,
            "time":time,
            "type":type,
            "contents":"".join(content.split(" ")),
        }
        with open("交易提示.txt",'a+') as f:
            f.write(str(dict))
            f.write('\n')
            f.close()

    def parseBlog(self,response: HtmlResponse):
        title=response.xpath("//h1/text()").extract_first()
        time=response.xpath("//div[@class='artinfo']/span/text()").extract_first()
        type=response.xpath("//div[@class='artinfo']/span[position()>1]/text()").extract_first()
        contents=response.xpath("//div[@class='articalContent']/p//text()").extract()
        if len(contents)==0:
            contents=response.xpath("//div[@class='articalContent']/div//text()").extract()
        content=re.sub('\s', ' ', "".join(contents))
        dict={
            "title":title,
            "time":time,
            "type":type,
            "contents":"".join(content.split(" ")),
        }
        with open("博客.txt",'a+') as f:
            f.write(str(dict))
            f.write('\n')
            f.close()
    def parseMarket(self,response: HtmlResponse):
        title=response.xpath("//h1/text()").extract_first()
        time=response.xpath("//div[@class='date-source']/span[@class='date']/text()").extract_first()
        type=response.xpath("//div[@class='date-source']/span[@class='source ent-source']/text()").extract_first()
        contents=response.xpath("//div[@class='article']/p/text()").extract()
        content = re.sub('\s', ' ', "".join(contents))
        dict = {
            "title": title,
            "time": time,
            "type":type,
            "contents": "".join(content.split(" ")),
        }
        with open("市场研究.txt", 'a+') as f:
            f.write(str(dict))
            f.write('\n')
            f.close()
    def parseMain(self,response: HtmlResponse):
        title = response.xpath("//h1/text()").extract_first()
        time = response.xpath("//div[@class='date-source']/span[@class='date']/text()").extract_first()
        type = response.xpath("//div[@class='date-source']/span[@class='source ent-source']/text()").extract_first()
        contents = response.xpath("//div[@class='article']/p/text()").extract()
        content = re.sub('\s', ' ', "".join(contents))
        dict = {
            "title": title,
            "time": time,
            "type": type,
            "contents": "".join(content.split(" ")),
        }
        with open("主力动向.txt", 'a+') as f:
            f.write(str(dict))
            f.write('\n')
            f.close()
    def parseSecurity(self,response: HtmlResponse):
        title = response.xpath("//h1/text()").extract_first()
        time = response.xpath("//div[@class='date-source']/span[@class='date']/text()").extract_first()
        type = response.xpath("//div[@class='date-source']/a[@class='source ent-source']/text()").extract_first()
        contents = response.xpath("//div[@class='article']/p/font/text()").extract()
        content = re.sub('\s', ' ', "".join(contents))
        dict = {
            "title": title,
            "time": time,
            "type": type,
            "contents": "".join(content.split(" ")),
        }
        with open("证券自媒体综合.txt", 'a+') as f:
            f.write(str(dict))
            f.write('\n')
            f.close()