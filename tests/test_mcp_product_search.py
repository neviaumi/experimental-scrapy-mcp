from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
import json
import pytest

TEST_KEYWORD = "M6 Bolts"

pytestmark = pytest.mark.anyio

@pytest.fixture
def mcp_server_config():
    with open ("mcp.json") as f:
        yield json.load(f)["mcpServers"]

@pytest.fixture
async def mcp_client_session(mcp_server_config):
    async with streamablehttp_client(mcp_server_config["test"]["url"]) as (
            read_stream,
            write_stream,
            _,
    ):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            yield session


async def test_search_products_on_diy_dot_com(mcp_client_session):
    # Call a tool
    tool_result = await mcp_client_session.call_tool("search_products_on_diy_dot_com", {"keyword": TEST_KEYWORD})
    assert tool_result.isError is False, "Tool call should no Error"
    assert len(tool_result.content) > 0, "Tool call response content should not be empty"
    response = json.loads(tool_result.content[0].text)
    assert len(response) > 0, f"${TEST_KEYWORD} should always return something"


async def test_search_products_on_toolstation(mcp_client_session):
    # Call a tool
    tool_result = await mcp_client_session.call_tool("search_products_on_toolstation", {"keyword": TEST_KEYWORD})
    assert tool_result.isError is False, "Tool call should no Error"
    assert len(tool_result.content) > 0, "Tool call response content should not be empty"
    response = json.loads(tool_result.content[0].text)
    assert len(response) > 0, f"${TEST_KEYWORD} should always return something"


async def test_search_products_on_wickes(mcp_client_session):
    # Call a tool
    tool_result = await mcp_client_session.call_tool("search_products_on_wickes", {"keyword": TEST_KEYWORD})
    assert tool_result.isError is False, "Tool call should no Error"
    assert len(tool_result.content) > 0, "Tool call response content should not be empty"
    response = json.loads(tool_result.content[0].text)
    assert len(response) > 0, f"${TEST_KEYWORD} should always return something"


async def test_search_products_on_screwfix(mcp_client_session):
    # Call a tool
    tool_result = await mcp_client_session.call_tool("search_products_on_screwfix", {"keyword": TEST_KEYWORD})
    assert tool_result.isError is False, "Tool call should no Error"
    assert len(tool_result.content) > 0, "Tool call response content should not be empty"
    response = json.loads(tool_result.content[0].text)
    assert len(response) > 0, f"${TEST_KEYWORD} should always return something"
