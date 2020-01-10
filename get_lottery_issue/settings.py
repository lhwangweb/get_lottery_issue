# -*- coding: utf-8 -*-

BOT_NAME = 'get_lottery_issue'

SPIDER_MODULES = ['get_lottery_issue.spiders']
NEWSPIDER_MODULE = 'get_lottery_issue.spiders'

ROBOTSTXT_OBEY = True

SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

# Pipeline 執行項目
ITEM_PIPELINES = {
  'get_lottery_issue.pipelines.GetLotteryIssuePipeline': 300,
}

# Splash 設定
SPLASH_URL = 'http://172.17.90.158:8050'

DOWNLOADER_MIDDLEWARES = {
    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
}

DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'

HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'

# LOG LEVEL
LOG_LEVEL = 'ERROR'

# DB
USERNAME = 'root'
PASSWORD = '123'
