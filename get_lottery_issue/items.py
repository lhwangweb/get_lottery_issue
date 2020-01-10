# -*- coding: utf-8 -*-
import scrapy

class GetLotteryIssueItem(scrapy.Item):
    """
    自訂 Item - 這邊定為『一期彩票資訊』
    """
    # 時間日期
    datetime = scrapy.Field()
    # 期數
    serial_no = scrapy.Field()
    # 開獎號碼
    issue_no = scrapy.Field()
    # 大小
    bigger_smaller_no = scrapy.Field()
    # 單雙
    odd_even_no = scrapy.Field()
    # 和
    sum_1 = scrapy.Field()
    # 和
    sum_2 = scrapy.Field()
    # 和
    sum_3 = scrapy.Field()
    # 龍虎
    dragon = scrapy.Field()
    # 前三
    f3 = scrapy.Field()
    # 中三
    m3 = scrapy.Field()
    # 後三
    b3 = scrapy.Field()
    
