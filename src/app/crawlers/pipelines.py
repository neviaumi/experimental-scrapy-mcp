# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AppPipeline:
    def process_item(self, item, spider):
        return item

class InMemoryStoragePipeline:
    def __init__(self, store):
        self.store = store

    @classmethod
    def from_crawler(cls, crawler):
        store = getattr(crawler, 'results_store')
        return cls(store=store)

    def process_item(self, item, _spider):
        print(item)
        self.store.append(item)
        return item

def with_in_memory_storage_pipeline(settings):
    crawler_settings = settings.copy()
    crawler_settings.set('ITEM_PIPELINES', {
        'crawlers.pipelines.InMemoryStoragePipeline': 0,
    })
    return crawler_settings

def with_result_store(crawler, store):
    setattr(crawler, 'results_store', store)
    return crawler
