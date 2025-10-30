import scrapy
from scrapy_playwright.page import PageMethod


class DetailsSpider(scrapy.Spider):
    name = "details"

    def __init__(self, *args, **kwargs):
        super(DetailsSpider, self).__init__(*args, **kwargs)
        self.product_links_with_site = kwargs.get('product_links_with_site', [])

    async def start(self):
        for product_info in self.product_links_with_site:
            url = product_info['product_url']
            site = product_info['site']

            # if site == 'mercado_livre':
            #     yield scrapy.Request(
            #         url,
            #         meta={
            #             "playwright": True,
            #             "playwright_page_methods": [
            #                 PageMethod("wait_for_selector", "h1.ui-pdp-title"),
            #                 PageMethod("wait_for_selector", "section#highlighted_specs_attrs"),
            #             ],
            #             "site": site
            #         },
            #         callback=self.parse_mercado_livre
            #     )
            if site == 'kabum':
                yield scrapy.Request(
                    url,
                    meta={
                        "playwright": True,
                        "playwright_page_methods": [
                            PageMethod("wait_for_selector", "h1"),
                        ],
                        "site": site
                    },
                    callback=self.parse_kabum
                )
            else:
                self.logger.info(f"Skipping details scraping for site: {site} for URL: {url}")

    # def parse_mercado_livre(self, response):
    #     title = response.css('h1.ui-pdp-title::text').get()
    #     price = response.css('meta[itemprop="price"]::attr(content)').get()
    #     highlights = response.css('ul.ui-vpp-highlighted-specs__features-list li::text').getall()
    #     description_parts = response.css('p.ui-pdp-description__content ::text').getall()
    #     description = ' '.join(part.strip() for part in description_parts if part.strip())

    #     # Extração das características destacadas
    #     highlighted_features = {}
    #     for feature_element in response.css('.ui-vpp-highlighted-specs__key-value'):
    #         key = feature_element.css('.ui-vpp-highlighted-specs__key-value__labels__key-value span:first-child::text').get()
    #         value = feature_element.css('.ui-vpp-highlighted-specs__key-value__labels__key-value span:last-child::text').get()
    #         if key and value:
    #             highlighted_features[key.strip().replace(':', '')] = value.strip()

    #     # Extração das características completas
    #     complete_features = {}
    #     for row in response.css('section#highlighted_specs_attrs .ui-vpp-striped-specs__table tr'):
    #         key = row.css('th div::text').get() # Corrected selector
    #         value = row.css('td span::text').get()
    #         if key and value:
    #             complete_features[key.strip()] = value.strip()

    #     yield {
    #         'titulo_produto': title.strip() if title else 'N/A',
    #         'link': response.url,
    #         'preco': price.strip() if price else 'N/A',
    #         'destaques': [h.strip() for h in highlights] if highlights else [],
    #         'caracteristicas_destacadas': highlighted_features,
    #         'caracteristicas_completas': complete_features,
    #         'descricao': description if description else 'N/A',
    #         'site': response.meta['site']
    #     }

    def parse_kabum(self, response):
        title = response.css('h1.text-black-800.font-bold::text').get()
        price = response.css('h4.text-secondary-500::text').get()
        description_parts = response.css('div#description ::text').getall()
        description = ' '.join(part.strip() for part in description_parts if part.strip())
        
        item = {
            'titulo_produto': title.strip() if title else 'N/A',
            'link': response.url,
            'preco': price.strip() if price else 'N/A',
            'descricao': description if description else 'N/A',
            'site': response.meta['site']
        }

        informacoes_tecnicas = {}
        for row in response.css('div.sc-7e0ca514-0.eRzxSz > div'):
            key = row.css('div:nth-child(1) ::text').get()
            value = row.css('div:nth-child(2) ::text').get()
            if key and value:
                informacoes_tecnicas[key.strip().replace(':', '')] = value.strip()
        
        item.update(informacoes_tecnicas)

        yield item
