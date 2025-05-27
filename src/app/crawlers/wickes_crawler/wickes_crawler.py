from typing import TypedDict
import urllib.parse
from bs4 import BeautifulSoup

from crawlee.crawlers import ParselCrawler
from crawlee.http_clients import HttpxHttpClient
from crawlee import Request
from crawlee.crawlers import ParselCrawlingContext
from crawlee.router import Router
from crawlee.storages import Dataset

router = Router[ParselCrawlingContext]()
WICKES_URL = "https://www.wickes.co.uk"


@router.handler(label="wickes product search")
async def wickes_product_search_handler(context: ParselCrawlingContext) -> None:
    def _extract_product(product_selector):
        product_url = product_selector.css('a::attr(href)').get()
        promo = product_selector.css('.products-list-v2__badge::text').get()
        return {
            'title': product_selector.css('a::attr(title)').get(),
            "price": product_selector.css('.product-card__price-value::text').get().strip(),
            "url": f"{WICKES_URL}{product_url}",
            "promo": promo.strip() if promo is not None and "for" in promo else None
        }

    for product in context.selector.css('[data-product-code]'):
        await context.push_data(_extract_product(product), dataset_name=context.request.id)

@router.handler(label="wickes product detail")
async def wickes_product_detail_handler(context: ParselCrawlingContext) -> None:
    def clean_html(html):
        soup = BeautifulSoup(html, 'lxml')
        for tag in soup.find_all(True):
            tag.attrs.pop('style', None)
            tag.attrs.pop('class', None)
        return str(soup)

    await context.push_data({
        "title": context.selector.css('title::text').get().strip(),
        "price": context.selector.css('.main-price__value::text').get().strip(),
        "description": context.selector.css('.product-main-info__description::text').get().strip(),
        "detail": clean_html(context.selector.css('.additional-info').get()),
        "promo": "".join(context.selector.css('.pdp-price__description *::text').getall())
    }, dataset_name=context.request.id)


class ProductDetailResponse(TypedDict):
    title: str
    price: str
    detail: str
    description: str
    promo: str | None

async def product_detail(url: str) -> ProductDetailResponse:
    request = Request.from_url(url, label="wickes product detail")
    dataset = await Dataset.open(name=request.id)
    crawler = ParselCrawler(
        configure_logging=False,
        request_handler=router,
        http_client=HttpxHttpClient()
    )
    await crawler.run(
        [
            request,
        ]
    )
    result = [item for item in (await dataset.get_data()).items]
    crawler.stop()
    await dataset.drop()
    return result[0]


class ProductSearchResponse(TypedDict):
    title: str
    price: str
    url: str
    promo: str | None


async def product_search(keyword: str) -> list[ProductSearchResponse]:
    query = urllib.parse.urlencode({"q": keyword})
    request = Request.from_url(f"{WICKES_URL}/search?{query}", label="wickes product search")
    dataset = await Dataset.open(name=request.id)
    crawler = ParselCrawler(
        configure_logging=False,
        request_handler=router,
        http_client=HttpxHttpClient()
    )


    await crawler.run(
        [
            request
        ]
    )
    result = [item for item in (await dataset.get_data()).items]
    crawler.stop()
    await dataset.drop()
    return result
