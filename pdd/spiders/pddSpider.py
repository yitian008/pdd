#!/usr/bin/env python
# -*- coding: utf-8 -*-

import scrapy
import re
import time

from pdd.items import PddItem

'''
    8个字段
    数据格式:title,share_url,share_user,share_user_bd_id(分享用户的百度id),share_time,
    file_size,file_class(类别信息,文档,软件等分类),ford(file or dir 目录或者文件)
'''

class PddSpider(scrapy.Spider):
    name = 'pddspider'
    start_urls = [
                  'http://www.panduoduo.net/bd/1'
                  ]
    
    def parse(self, response):
        # print '开始啦'
        urls = response.css('a.blue::attr(href)').extract()
        # print 'urls长度为:', len(urls)
        for url in urls:
            url = 'http://www.panduoduo.net' + url
            yield scrapy.Request(url, callback=self.parse_item, meta={'url': url})

            # 如果有参数需要从parse传入到parse_item,可以使用meta,如下将url参数传递过去
            # yield scrapy.Request(url, callback=self.parse_item, meta={'url': url})
            # 在parse_item中使用url = response.meta['url']即可使用传递过来的url参数

        # 找到网页中的下一页按钮,继续爬取
        next_page_url = 'http://www.panduoduo.net' + response.css('div.page-list a::attr(href)').extract()[-2]
        # print 'next page url is :', next_page_url
        if next_page_url is not None:
            # print '马上开始yield'
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_item(self, response):
        item = PddItem()
        all_dd = response.css('dd')
        dd0 = all_dd[0]    # 分享用户 share_user
        dd1 = all_dd[1]    # 资源分类 file_class
        dd2 = all_dd[2]    # 文件大小 file_size
        # dd3 = all_dd[3]  # 资源类型 百度网盘
        # dd4 = all_dd[4]  # 浏览次数
        dd5 = all_dd[5]    # 发布日期 share_time
        dd6 = all_dd[6]    # 资源类别 ford
        # dd7 = all_dd[7]  # 其他
        
        item['share_user_bd_id'] = dd0.css('a::attr(href)').extract_first()
        item['share_user'] = dd0.css('a::text').extract_first()
        item['file_class'] = dd1.css('a::text').extract_first()
        item['file_size'] = dd2.css('b::text').extract_first()
        item['share_time'] = dd5.css('::text').extract_first()[5:]
        item['ford'] = dd6.css('::text').extract_first()[5:]
        
        item['title'] = response.css('h1::text').extract_first()

        share_url = response.css('a.dbutton2::attr(href)').extract_first()
        share_url = re.compile('http%3A.*').findall(share_url)[0]
        share_url = share_url.replace('%3A', ':').replace('%3F', '?').replace('%3D', '=').replace('%26', '&')
        item['share_url'] = share_url

        # 控制采集速度
        time.sleep(0.5)
        yield item

