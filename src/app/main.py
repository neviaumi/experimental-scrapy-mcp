import crawlers.diy_dot_com_crawler as diy_dot_com_crawler


async def main() -> None:
    items = await diy_dot_com_crawler.product_search("M6 Hex Bolts")
    print(items)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
