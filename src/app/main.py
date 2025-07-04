import crawlers.screwfix_crawler as screwfix_crawler
from crawlee import service_locator
from crawlee.storage_clients import MemoryStorageClient


async def main() -> None:
    service_locator.set_storage_client(
        MemoryStorageClient(
            storage_dir="",
            default_request_queue_id="",
            default_key_value_store_id="",
            default_dataset_id="",
            write_metadata=False,
            persist_storage=False,
        )
    )
    item = await screwfix_crawler.product_search(
        "Angle Grinder Diamond Wood Blade 115mm"
    )
    print(item)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
