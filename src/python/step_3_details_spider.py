#!/usr/bin/env python
import os
import sys
import json
import nest_asyncio

# Add the project root to the Python path


from scrapy.crawler import CrawlerProcess
from spiders.details_spider import DetailsSpider

import argparse

def run_details_spider():
    nest_asyncio.apply()

    # Corrected paths to be relative to the project root
    output_dir = '../../data'
    links_input_file = os.path.join(output_dir, 'product_links.json')
    details_output_file = os.path.join(output_dir, 'products_details.json')

    if not os.path.exists(links_input_file):
        print(f"Error: Input file not found at {links_input_file}. Run the links spider first.")
        return

    product_links_with_site = []
    with open(links_input_file, 'r') as f:
        for line in f:
            if line.strip():
                product_links_with_site.append(json.loads(line))
    
    if not product_links_with_site:
        print("No product URLs found to scrape.")
        return



    process = CrawlerProcess(settings={
        'FEEDS': { details_output_file: {'format': 'jsonlines', 'overwrite': False} },
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

    print(f"Running spider to get details for {len(product_links_with_site)} products...")
    process.crawl(DetailsSpider, product_links_with_site=product_links_with_site)
    process.start()
    print(f"Detail scraping finished. Data saved to {details_output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    # Set the working directory to the script's directory to make paths consistent
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run_details_spider()