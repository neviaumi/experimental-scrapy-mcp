import crawlers.diy_dot_com_crawler as diy_dot_com_crawler
from crawlee import service_locator
from crawlee.storage_clients import MemoryStorageClient



async def main() -> None:
    service_locator.set_storage_client(MemoryStorageClient(
        storage_dir="",
        default_request_queue_id="",
        default_key_value_store_id="",
        default_dataset_id="",
        write_metadata=False,
        persist_storage=False))
    service_locator.get_configuration()
    print(service_locator._configuration_was_retrieved)
    items = await diy_dot_com_crawler.product_search("M6 coach screw table leg")
    print(service_locator._configuration_was_retrieved)
    print(await diy_dot_com_crawler.product_detail(items[0]["url"]))

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
