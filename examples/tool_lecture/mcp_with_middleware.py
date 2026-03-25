import asyncio
from typing import Callable
from langchain.agents import create_agent
from langchain.agents.middleware import wrap_tool_call
from langchain.tools.tool_node import ToolCallRequest
from langchain_mcp_adapters.client import MultiServerMCPClient

from util.models import get_model
from util.streaming_utils import STREAM_MODES, handle_stream_async
from util.pretty_print import get_user_input

MAX_RESPONSE_LENGTH = 300

@wrap_tool_call
def truncate_tool_output(
    request: ToolCallRequest,
    handler: Callable,
):
    """Trunkerar verktygsresponser till MAX_RESPONSE_LENGTH tecken."""

    # Call the tool and get the tool result
    result = handler(request)

    content_str = str(result.content)
    if len(content_str) > MAX_RESPONSE_LENGTH:
        truncated = content_str[:MAX_RESPONSE_LENGTH]
        result.content = f"{truncated}..."

    return result


async def run_async():
    # Get predefined attributes
    model = get_model()
    mcp_client = MultiServerMCPClient({
        "math_server": {
            "transport": "streamable_http",
            "url": "http://localhost:8001/mcp",
        }
    })

    # Get and filter tools from MCP server
    all_tools = await mcp_client.get_tools()

    # Create agent
    agent = create_agent(
        model=model,
        tools=all_tools,
        middleware=[truncate_tool_output],
        system_prompt=(
            "Du är en hjälpsam assistent som svarar på användarens frågor. "
        )
    )

    # Get user input
    user_input = get_user_input("Ställ din fråga")

    # Call the agent
    process_stream = agent.astream(
        {"messages": [{"role": "user", "content": user_input}]},
        stream_mode=STREAM_MODES,
    )

    # Stream the process
    await handle_stream_async(process_stream)


def run():
    asyncio.run(run_async())


if __name__ == "__main__":
    run()
