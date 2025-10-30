#!/usr/bin/env python
import os
import sys
import nest_asyncio

# Add the project root to the Python path to allow imports from 'spiders'


from scrapy.crawler import CrawlerProcess
from spiders.links_spider import LinksSpider

import argparse

def run_links_spider(site, url, limit):
    nest_asyncio.apply()

    # Corrected path to be relative to the project root
    output_dir = '../../data'
    links_output_file = os.path.join(output_dir, 'product_links.json')
    
    os.makedirs(output_dir, exist_ok=True)



    process = CrawlerProcess(settings={
        'FEEDS': { links_output_file: {'format': 'jsonlines', 'overwrite': False} },
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'LOG_LEVEL': 'INFO',
        'CONCURRENT_REQUESTS_PER_DOMAIN': 3,
        'DOWNLOAD_HANDLERS': {
            'http': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
            'https': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
        },
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        'PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT': 120000,
        'DOWNLOAD_TIMEOUT': 120,
    })

    print(f"Running spider to get product links for {site}...")
    process.crawl(LinksSpider, site=site, url=url, limit=limit)
    process.start()
    print(f"Link scraping finished. Data saved to {links_output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--site', type=str, default='mercado_livre', help='The site to scrape (mercado_livre or kabum)')
    parser.add_argument('--url', type=str, help='The URL to scrape')
    parser.add_argument('--limit', type=int, default=0, help='The maximum number of product links to scrape per site.')
    args = parser.parse_args()

    # Set the working directory to the script's directory to make paths consistent
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_links_spider(args.site, args.url, args.limit)