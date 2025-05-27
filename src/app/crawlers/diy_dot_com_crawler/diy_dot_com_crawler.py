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
DIY_DOT_COM_URL = "https://www.diy.com"


@router.handler(label="diy.com product search")
async def diy_dot_com_product_search_handler(context: ParselCrawlingContext) -> None:
    def _extract_product(product_selector):
        product_url = product_selector.css('[data-testid=\'product-link\']::attr(href)').get()
        return {
            'title': product_selector.css('[data-testid=\'product-name\']::text').get(),
            "price": product_selector.css('[data-testid=\'product-price\']::text').get(),
            "url": f"{DIY_DOT_COM_URL}{product_url}"
        }

    for product in context.selector.css('[data-testid=\'product\']'):
        await context.push_data(_extract_product(product))

@router.handler(label="diy.com product detail")
async def diy_dot_com_product_detail_handler(context: ParselCrawlingContext) -> None:
    def clean_html(html):
        soup = BeautifulSoup(html, 'lxml')
        for tag in soup.find_all(True):
            tag.attrs.pop('style', None)
            tag.attrs.pop('class', None)
        return str(soup)

    await context.push_data({
        "title": context.selector.css('[data-testid=\'product-name\']::text').get(),
        "price": context.selector.css('[data-testid=\'product-price\']::text').get(),
        "detail": clean_html(context.selector.css('#product-details').get())
    })


class ProductDetailResponse(TypedDict):
    title: str
    price: str
    detail: str

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
            Request.from_url(url, label="diy.com product detail"),
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

    query = urllib.parse.urlencode({"term": keyword})

    await crawler.run(
        [
            Request.from_url(f"{DIY_DOT_COM_URL}/search?{query}", label="diy.com product search"),
        ]
    )
    dataset = await crawler.get_data()
    result = [item for item in dataset.items]
    crawler.stop()
    return result
