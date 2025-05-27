from typing import TypedDict
import urllib.parse
from bs4 import BeautifulSoup

from crawlee.crawlers import ParselCrawler
from crawlee.http_clients import HttpxHttpClient
from crawlee.storage_clients import MemoryStorageClient
from crawlee import Request
from crawlee.crawlers import ParselCrawlingContext
from crawlee.router import Router

router = Router[ParselCrawlingContext]()
SCREWFIX_URL = "https://www.screwfix.com"


@router.handler(label="screwfix product search")
async def screwfix_product_search_handler(context: ParselCrawlingContext) -> None:
    def _extract_product(product_selector):
        product_url = product_selector.css('[data-qaid=\'product_description\']::attr(href)').get()
        return {
            'title': product_selector.css('[data-qaid=\'product_description\'] span::text').get(),
            "price": product_selector.css('[data-qaid=\'price\']::text').get(),
            "url": f"{SCREWFIX_URL}{product_url}",
            "promo": product_selector.css('[data-qaid=\'promo-banner\'] *::text').get()
        }

    for product in context.selector.css('[data-qaid=\'product-card\']'):
        await context.push_data(_extract_product(product))

@router.handler(label="screwfix product detail")
async def screwfix_product_detail_handler(context: ParselCrawlingContext) -> None:
    def clean_html(html):
        soup = BeautifulSoup(html, 'lxml')
        for tag in soup.find_all(True):
            tag.attrs.pop('style', None)
            tag.attrs.pop('class', None)
        return str(soup)

    await context.push_data({
        "title": context.selector.css('[data-qaid=\'pdp-product-name\'] *::text').get(),
        "price": "".join(context.selector.css('[data-qaid=\'pdp-price\'] *::text').getall()[:-1]),
        "description": context.selector.css('[data-qaid=\'pdp-product-overview\']::text').get(),
        "detail": clean_html(context.selector.css('[data-qaid=\'pdp-tabpanel-2\'] table').get()),
        "promo": context.selector.css('[data-qaid=\'promo-message\']::text').get()
    })


class ProductDetailResponse(TypedDict):
    title: str
    price: str
    detail: str
    description: str
    promo: str | None

async def product_detail(url: str) -> ProductDetailResponse:
    crawler = ParselCrawler(
        configure_logging=False,
        request_handler=router,
        http_client=HttpxHttpClient(),
        storage_client=MemoryStorageClient(
            storage_dir="",
            default_request_queue_id="",
            default_key_value_store_id="",
            default_dataset_id="",
            write_metadata=False,
            persist_storage=False),
    )
    await crawler.run(
        [
            Request.from_url(url, label="screwfix product detail"),
        ]
    )
    dataset = await crawler.get_data()
    result = [item for item in dataset.items]
    crawler.stop()
    return result[0]


class ProductSearchResponse(TypedDict):
    title: str
    price: str
    url: str
    promo: str | None


async def product_search(keyword: str) -> list[ProductSearchResponse]:
    crawler = ParselCrawler(
        configure_logging=False,
        request_handler=router,
        http_client=HttpxHttpClient(),
        storage_client=MemoryStorageClient(
            storage_dir="",
            default_request_queue_id="",
            default_key_value_store_id="",
            default_dataset_id="",
            write_metadata=False,
            persist_storage=False),
    )

    query = urllib.parse.urlencode({"search": keyword})

    await crawler.run(
        [
            Request.from_url(f"{SCREWFIX_URL}/search?{query}", label="screwfix product search"),
        ]
    )
    dataset = await crawler.get_data()
    result = [item for item in dataset.items]
    crawler.stop()
    return result
