from mcp.server.fastmcp import FastMCP
from crawlers import DiyDotComProductSearchSpider, settings, DiyDotComProductDetailSpider
from scrapy.crawler import CrawlerProcess
import app.crawler.pipelines as pipelines
import json
import logging

mcp = FastMCP("Hardware Store", dependencies=["crawlers", "app"])

logging.info("Running?")
@mcp.resource("spider://diy.com/products/search/{keyword}")
def search_products_on_diy_dot_com(keyword: str) -> str:
    """
        MCP Resource: Search for products on diy.com based on a provided keyword.

        Args:
            keyword (str): The search term to query diy.com’s product catalog.

        Returns:
            str: A JSON-encoded array of product data matching the given keyword.
                 Each product entry contains:
                    - "title" (str): The product name.
                    - "price" (str): The price of the product as a string.
                    - "url" (str): The full URL linking to the product's detail page.

        Example Result:
            [
                {
                    "title": "Hammer",
                    "price": "£9.99",
                    "url": "https://www.diy.com/hammer"
                },
                {
                    "title": "Drill",
                    "price": "£49.99",
                    "url": "https://www.diy.com/drill"
                }
            ]
        """
    result = []
    crawler_settings = pipelines.with_in_memory_storage_pipeline(settings)
    crawler_settings.set('LOG_ENABLED', False)
    process = CrawlerProcess(crawler_settings)
    crawler = pipelines.with_result_store(process.create_crawler(DiyDotComProductSearchSpider), result)
    process.crawl(crawler, keyword=keyword)
    process.start()
    return json.dumps(result)


@mcp.resource("spider://diy.com/products/{product_url}")
def get_product_detail_on_diy_dot_com(product_url: str) -> str:
    """
    MCP Resource: Retrieve detailed product information from diy.com for a specific product URL.

    Args:
        product_url (str): The relative product URL (e.g., `/product/hammer`).

    Returns:
        str: A JSON-encoded object containing the product's detailed information:
                - "title" (str): The product name.
                - "price" (str): The price of the product as a string.
                - "detail" (str): Cleaned HTML content describing the product.

    Example Result:
        {
            "title": "Hammer",
            "price": "£9.99",
            "detail": "<div><h1>Hammer Details</h1><p>Durable and reliable design.</p></div>"
        }
    """

    result = []
    crawler_settings = pipelines.with_in_memory_storage_pipeline(settings)
    crawler_settings.set('LOG_ENABLED', False)
    process = CrawlerProcess(crawler_settings)
    crawler = pipelines.with_result_store(process.create_crawler(DiyDotComProductDetailSpider), result)
    process.crawl(crawler, url=product_url)
    process.start()
    return json.dumps(result[0])
