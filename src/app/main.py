import crawlers.diy_dot_com_crawler as diy_dot_com_crawler


async def main() -> None:
    items = await diy_dot_com_crawler.product_detail("https://www.diy.com/departments/verve-peat-free-multi-purpose-compost-50l/5059340368795_BQ.prd")
    print(items)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
