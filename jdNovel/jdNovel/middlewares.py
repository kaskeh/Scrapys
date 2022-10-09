# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import time
import warnings

from scrapy import signals
# from scrapy.http.response.html import HtmlResponse
from scrapy.http import HtmlResponse

from selenium import webdriver


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


# class JdnovelSpiderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the spider middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_spider_input(self, response, spider):
#         # Called for each response that goes through the spider
#         # middleware and into the spider.
#
#         # Should return None or raise an exception.
#         return None
#
#     def process_spider_output(self, response, result, spider):
#         # Called with the results returned from the Spider, after
#         # it has processed the response.
#
#         # Must return an iterable of Request, or item objects.
#         for i in result:
#             yield i
#
#     def process_spider_exception(self, response, exception, spider):
#         # Called when a spider or process_spider_input() method
#         # (from other spider middleware) raises an exception.
#
#         # Should return either None or an iterable of Request or item objects.
#         pass
#
#     def process_start_requests(self, start_requests, spider):
#         # Called with the start requests of the spider, and works
#         # similarly to the process_spider_output() method, except
#         # that it doesn’t have a response associated.
#
#         # Must return only requests (not items).
#         for r in start_requests:
#             yield r
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)
#
# class JdnovelDownloaderMiddleware:
#     # Not all methods need to be defined. If a method is not defined,
#     # scrapy acts as if the downloader middleware does not modify the
#     # passed objects.
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         # This method is used by Scrapy to create your spiders.
#         s = cls()
#         crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
#         return s
#
#     def process_request(self, request, spider):
#         # Called for each request that goes through the downloader
#         # middleware.
#
#         # Must either:
#         # - return None: continue processing this request
#         # - or return a Response object
#         # - or return a Request object
#         # - or raise IgnoreRequest: process_exception() methods of
#         #   installed downloader middleware will be called
#         return None
#
#     def process_response(self, request, response, spider):
#         # Called with the response returned from the downloader.
#
#         # Must either;
#         # - return a Response object
#         # - return a Request object
#         # - or raise IgnoreRequest
#         return response
#
#     def process_exception(self, request, exception, spider):
#         # Called when a download handler or a process_request()
#         # (from other downloader middleware) raises an exception.
#
#         # Must either:
#         # - return None: continue processing this exception
#         # - return a Response object: stops process_exception() chain
#         # - return a Request object: stops process_exception() chain
#         pass
#
#     def spider_opened(self, spider):
#         spider.logger.info('Spider opened: %s' % spider.name)

class seleniumMiddleware:
    def process_request(self, request, spider):
        url = request.url
        if "py21" in request.meta and "cat=" in url:
            print("selenium中间件")

            # warnings.simplefilter("ignore", ResourceWarning)

            # 可以使用无头模式
            chrome_optins = webdriver.ChromeOptions()
            chrome_optins.add_argument("--headless")
            chrome_optins.add_experimental_option("excludeSwitches", ["enable-logging"])
            chrome_optins.add_argument('--disable-gpu')    # 禁止gpu加速
            chrome_optins.add_argument("no-sandbox")       # 取消沙盒模式
            chrome_optins.add_argument("disable-blink-features=AutomationControlled")  # 禁用启用Blink运行时的功能
            chrome_optins.add_experimental_option('excludeSwitches', ['enable-automation'])    # 开发者模式
            driver = webdriver.Chrome(options=chrome_optins)
            # 移除 `window.navigator.webdriver`. scrapy 默认为True
            driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                            Object.defineProperty(navigator, 'webdriver', {
                              get: () =&gt; undefined
                            })
                          """
            })
            # driver = webdriver.Chrome()

            driver.get(url)
            # time.sleep(3)
            driver.implicitly_wait(5)
            data = driver.page_source
            # data = "<html><html/>"
            driver.close()

            # 创建响应对象
            res = HtmlResponse(url=url, body=data, encoding="utf-8", request=request)
            return res
        else:
            return None