from crawlers import  DiyDotComProductSearchSpider, settings
from scrapy.crawler import CrawlerProcess
import app.crawler.pipelines as pipelines
def main():
    result = []
    crawler_settings = pipelines.with_in_memory_storage_pipeline(settings)
    crawler_settings.set('LOG_ENABLED', False)
    process = CrawlerProcess(crawler_settings)
    crawler = pipelines.with_result_store(process.create_crawler(DiyDotComProductSearchSpider), result)
    process.crawl(crawler, keyword="M6 Hex Bolts")
    process.start()
    print(result)


if __name__ == "__main__":
    main()
