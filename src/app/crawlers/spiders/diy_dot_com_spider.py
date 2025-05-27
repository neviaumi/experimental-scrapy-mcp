import scrapy
import urllib.parse
from bs4 import BeautifulSoup

DIY_DOT_COM_URL = "https://www.diy.com"


class DiyDotComProductSearchSpider(scrapy.Spider):
    name = "diy.com Product Search"

    def __init__(self, keyword, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyword = keyword

    # async def start(self):
    #     print("Started on start")
    #     query = urllib.parse.urlencode({"term": self.keyword})
    #     url = f"{DIY_DOT_COM_URL}/search?{query}"
    #     req = scrapy.Request(url, callback=self.parse)
    #     print(req.callback)
    #     yield req

    def start_requests(self):
        print("Started on start_requests")
        query = urllib.parse.urlencode({"term": self.keyword})
        url = f"{DIY_DOT_COM_URL}/search?{query}"
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        print("Started on parse")

        def _extract_product(product_selector):
            product_url = product_selector.css('[data-testid=\'product-link\']::attr(href)').get()
            return {
                'title': product_selector.css('[data-testid=\'product-name\']::text').get(),
                "price": product_selector.css('[data-testid=\'product-price\']::text').get(),
                "url": f"{DIY_DOT_COM_URL}{product_url}"
            }

        for product in response.css('[data-testid=\'product\']'):
            yield _extract_product(product)


def clean_html(html):
    soup = BeautifulSoup(html, 'lxml')
    for tag in soup.find_all(True):
        tag.attrs.pop('style', None)
        tag.attrs.pop('class', None)
    return str(soup)


class DiyDotComProductDetailSpider(scrapy.Spider):
    name = "diy.com Product Detail"

    def __init__(self, url, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        yield {
            "title": response.css('[data-testid=\'product-name\']::text').get(),
            "price": response.css('[data-testid=\'product-price\']::text').get(),
            "detail": clean_html(response.css('#product-details').get())
        }
