

from twisted.internet.defer import DeferredList
import asyncio
from scrapy.utils.reactor import install_reactor
# Install the asyncio reactor before importing other modules
install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')

from twisted.internet import reactor
from crawlers import DiyDotComProductSearchSpider, settings, with_in_memory_storage_pipeline, with_result_store
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import time


def run_crawler():
    result = []
    crawler_settings = with_in_memory_storage_pipeline(settings)
    # crawler_settings.set('LOG_ENABLED', False)
    configure_logging(crawler_settings)  # Ensures proper logging configuration

    runner = CrawlerRunner(crawler_settings)

    # Create the crawler and store the result list
    crawler = runner.create_crawler(DiyDotComProductSearchSpider)
    crawler = with_result_store(crawler, result)

    # Start the crawler
    d = runner.crawl(crawler, keyword="M6 Hex Bolts")

    # Set a timeout to stop the reactor after 8 seconds (safety measure)
    # reactor.callLater(8, reactor.stop)

    # Add a callback to stop the reactor when the crawl is complete
    d.addBoth(lambda _: reactor.callLater(0, reactor.stop))

    # Start the reactor
    # reactor.run(installSignalHandlers=False)  # Disable signal handlers for better integration
    reactor.run()

    return result


def main():
    result = run_crawler()
    print(result)


if __name__ == "__main__":
    main()
