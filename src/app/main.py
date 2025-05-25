from crawlers import  DiyDotComProductSearchSpider, settings
from scrapy.crawler import CrawlerProcess

def main():
    process = CrawlerProcess(settings)
    process.crawl(DiyDotComProductSearchSpider, keyword="M6 Hex Bolts")
    process.start()


if __name__ == "__main__":
    main()
