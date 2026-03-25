from langchain.agents import create_agent
from langchain.tools import tool
from util.models import get_model
from util.streaming_utils import STREAM_MODES, handle_stream
from util.pretty_print import get_user_input
from util.tools import calculate, get_html_crud_tool
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.runnables import RunnableConfig
from typing import Annotated
from pydantic import Field


def build_agents():
    model = get_model()

    math_agent = create_agent(
        model=model,
        tools=[calculate],
        name="math_agent",
        system_prompt=(
            "You are a mathematics specialist. Solve math problems step by step. "
            "Use the calculate tool for computations. Show your work clearly "
            "and explain the reasoning behind each step."
        ),
    )

    browser_agent = create_agent(
        model=model,
        tools=get_html_crud_tool(),
        name="browser_agent",
        system_prompt=(
            "You are a browser specialist. Answer factual questions "
            "thoroughly and accurately. Use the web search tool to find information "
        ),
    ) 

    creative_agent = create_agent(
        model=model,
        tools=[],
        name="creative_agent",
        system_prompt=(
            "You are a creative writing specialist. Help with creative tasks "
            "such as writing stories, poems, marketing copy, brainstorming ideas, "
            "and any other creative content. Be imaginative, engaging, and adapt "
            "your style to match the request."
        ),
    )

    @tool("ask_math_agent", description="Math specialist. Use for calculations, equations, math problems, statistics, and numerical analysis.")
    def call_math_agent(query: Annotated[str, Field(description="Math question")]) -> str:
        return handle_stream(
            math_agent.stream(
                {"messages": [{"role": "user", "content": query}]},
                stream_mode=STREAM_MODES,
            ),
            agent_name="math_agent",
        )

    @tool("ask_browser_agent", description="Browser specialist. Use this for searching specific web pages.")
    def call_browser_agent(webpage_url: Annotated[str, Field(description="Webpage URL")], user_query: Annotated[str, Field(description="User query")]) -> str:
        return handle_stream(
            browser_agent.stream(
                {"messages": [{"role": "user", "content": user_query + ". Webpage URL: " + webpage_url}]},
                stream_mode=STREAM_MODES,
            ),
            agent_name="browser_agent",
        )

    @tool("ask_creative_agent", description="Creative writing specialist. Use for stories, poems, marketing copy, brainstorming, naming, and any creative content.")
    def call_creative_agent(query: Annotated[str, Field(description="Creative question")]) -> str:
        return handle_stream(
            creative_agent.stream(
                {"messages": [{"role": "user", "content": query}]},
                stream_mode=STREAM_MODES,
            ),
            agent_name="creative_agent",
        )

    router_agent = create_agent(
        model=model,
        tools=[call_math_agent, call_browser_agent, call_creative_agent],
        name="router",
        system_prompt=(
            "You are a routing agent that dispatches user queries to the most appropriate specialist."
        ),
        checkpointer=InMemorySaver(),
    )

    return router_agent


def run():
    router_agent = build_agents()
    thread_id = "conversation_001"
    config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
    while True:
        user_input = get_user_input("Ställ din fråga")
        process_stream = router_agent.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            stream_mode=STREAM_MODES,
            config=config,
        )

        # Stream the process
        handle_stream(process_stream)


if __name__ == "__main__":
    run()
