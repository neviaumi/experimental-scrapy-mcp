from mcp.server.fastmcp import FastMCP
import crawlers.diy_dot_com_crawler as diy_dot_com_crawler

import json

mcp = FastMCP("Hardware Store", dependencies=["crawlee", "beautifulsoup4"])

# @mcp.resource("spider://diy.com/products/search/{keyword}")
@mcp.tool("search_products_on_diy_dot_com", "Search for products on diy.com based on a provided keyword.")
async def search_products_on_diy_dot_com(keyword: str) -> str:
    """Search for products on diy.com based on a provided keyword.

        Args:
            keyword (str): The search term to query diy.com’s product catalog.

        Returns:
            str: A JSON-encoded array of product data matching the given keyword.
                 Each product entry contains:
                    - "title" (str): The product name.
                    - "price" (str): The price of the product as a string.
                    - "url" (str): The full URL linking to the product's detail page.

        Example Result:
            [
                {
                    "title": "Hammer",
                    "price": "£9.99",
                    "url": "https://www.diy.com/hammer"
                },
                {
                    "title": "Drill",
                    "price": "£49.99",
                    "url": "https://www.diy.com/drill"
                }
            ]
        """
    result = await diy_dot_com_crawler.product_search(keyword)

    return json.dumps(result)


# @mcp.resource("spider://diy.com/products/{product_url}")
@mcp.tool("get_product_detail_on_diy_dot_com", "Retrieve detailed product information from diy.com for a specific product URL.")
async def get_product_detail_on_diy_dot_com(product_url: str) -> str:
    """Retrieve detailed product information from diy.com for a specific product URL.

    Args:
        product_url (str): The relative product URL (e.g., `/product/hammer`).

    Returns:
        str: A JSON-encoded object containing the product's detailed information:
                - "title" (str): The product name.
                - "price" (str): The price of the product as a string.
                - "detail" (str): Cleaned HTML content describing the product.

    Example Result:
        {
            "title": "Hammer",
            "price": "£9.99",
            "detail": "<div><h1>Hammer Details</h1><p>Durable and reliable design.</p></div>"
        }
    """

    result = await diy_dot_com_crawler.product_detail(product_url)
    return json.dumps(result)
