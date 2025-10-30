import os
import scrapy
from scrapy_playwright.page import PageMethod

class LinksSpider(scrapy.Spider):
    name = "links"

    def __init__(self, *args, **kwargs):
        super(LinksSpider, self).__init__(*args, **kwargs)
        self.site = kwargs.get('site', 'mercado_livre')
        self.start_url = kwargs.get('url', '')
        self.limit = int(kwargs.get('limit', 0))

    async def start(self):
        # if self.site == 'mercado_livre':
        #     yield scrapy.Request(
        #         self.start_url,
        #         meta={
        #             "playwright": True,
        #             "playwright_page_methods": [
        #                 PageMethod("screenshot", path="/mnt/ac39b5b4-d98f-4954-9849-56f595846151/code/Scrap_LLM/mercado_livre_initial_load_screenshot.png", full_page=True),
        #                 PageMethod("wait_for_selector", "a.poly-component__title", timeout=60000),
        #             ],
        #         },
        #         callback=self.parse_mercado_livre
        #     )
        if self.site == 'kabum':
            yield scrapy.Request(
                self.start_url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "a.productLink"),
                    ],
                },
                callback=self.parse_kabum
            )
        else:
            self.logger.info(f"Skipping links scraping for site: {self.site}")

    # def parse_mercado_livre(self, response):
    #     self.logger.info("Mercado Livre page loaded and selector found. Attempting to extract links.")
    #     product_links = response.css('a.poly-component__title::attr(href)').getall()
    #     count = 0
    #     for link in product_links:
    #         if self.limit > 0 and count >= self.limit:
    #             self.logger.info(f"Limite de {self.limit} links de produtos para {self.site} atingido.")
    #             break
    #         count += 1
    #         yield {
    #             'product_url': response.urljoin(link),
    #             'site': self.site
    #         }

    def parse_kabum(self, response):
        self.logger.info(f"Parsing page: {response.url}")
        product_links = response.css('a.productLink::attr(href)').getall()
        count = 0
        for link in product_links:
            if self.limit > 0 and count >= self.limit:
                self.logger.info(f"Limite de {self.limit} links de produtos para {self.site} atingido.")
                break
            count += 1
            yield {
                'product_url': response.urljoin(link),
                'site': self.site
            }

        next_page_selector = "//a[contains(@class, 'nextLink') and not(@aria-disabled='true')]"
        
        if response.xpath(next_page_selector):
            self.logger.info("Next page button found, clicking it.")
            yield scrapy.Request(
                response.url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("click", selector=next_page_selector),
                        PageMethod("wait_for_timeout", 5000),
                        PageMethod("wait_for_selector", "a.productLink"),
                    ],
                },
                callback=self.parse_kabum,
                dont_filter=True
            )
        else:
            self.logger.info("Next page button not found or is disabled.")