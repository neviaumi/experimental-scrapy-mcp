class InMemoryStoragePipeline:
    def __init__(self, store):
        self.store = store

    @classmethod
    def from_crawler(cls, crawler):
        store = getattr(crawler, 'results_store')
        return cls(store=store)

    def process_item(self, item, _spider):
        self.store.append(item)
        return item

def with_in_memory_storage_pipeline(settings):
    crawler_settings = settings.copy()
    crawler_settings.set('ITEM_PIPELINES', {
        'app.crawler.pipelines.InMemoryStoragePipeline': 0,
    })
    return crawler_settings

def with_result_store(crawler, store):
    setattr(crawler, 'results_store', store)
    return crawler
