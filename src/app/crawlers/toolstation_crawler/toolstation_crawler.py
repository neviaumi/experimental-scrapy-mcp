from typing import TypedDict
import urllib.parse

from crawlee.crawlers import HttpCrawler
from crawlee.http_clients import HttpxHttpClient
from crawlee.storage_clients import MemoryStorageClient
from crawlee import Request
from crawlee.crawlers import HttpCrawlingContext
from crawlee.router import Router
import json

router = Router[HttpCrawlingContext ]()
TOOLSTATION_API = "https://www.toolstation.com/api"


@router.handler(label="toolstation product search")
async def toolstation_product_search_handler(context: HttpCrawlingContext) -> None:
    body = json.loads(context.http_response.read())

    def _extract_product(product):
        return {
            'title': product["title"].strip(),
            "price": f"£{product['price']}",
            "url": product["url"].strip(),
            "promo": product['weboverlaytext'] if 'for' in product.get("weboverlaytext", '') else None
        }

    for product in body["response"]["docs"]:
        await context.push_data(_extract_product(product))

class ProductSearchResponse(TypedDict):
    title: str
    price: str
    url: str


async def product_search(keyword: str) -> list[ProductSearchResponse]:
    crawler = HttpCrawler(
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

    query = urllib.parse.urlencode(
        {"request_type": "search", "q": keyword, "start": "0", "search_type": "keyword",
         "skipCache": "true"})

    await crawler.run(
        [
            Request.from_url(
                f"{TOOLSTATION_API}/search/crs?{query}",
                label="toolstation product search"),
        ]
    )
    dataset = await crawler.get_data()
    result = [item for item in dataset.items]
    crawler.stop()
    return result
