from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from langchain_core.runnables import RunnableConfig

from util.models import get_model
from util.pretty_print import get_user_decision, get_user_input, print_interrupt_info
from util.streaming_utils import STREAM_MODES, handle_stream

from typing import Annotated
from pydantic import Field


@tool
def read_file(file_path: Annotated[str, Field(description="Filväg att läsa")]) -> str:
    """Read the content of a file. Safe operation that does not require approval."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f"Content from {file_path}:\n{f.read()}"
    except FileNotFoundError:
        return f"File {file_path} not found."
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"


@tool
def write_file(file_path: Annotated[str, Field(description="Filväg att skriva till")], 
               content: Annotated[str, Field(description="Innehåll att skriva till filen")]) -> str:
    """Write content to a file. SENSITIVE OPERATION - requires approval!"""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Wrote to {file_path} successfully"
    except Exception as e:
        return f"Error writing to {file_path}: {str(e)}"


def run():
    model = get_model()
    config: RunnableConfig = {"configurable": {"thread_id": "demo_thread_001"}}

    agent = create_agent(
        model=model,
        tools=[read_file, write_file],
        system_prompt=(
            "Du är en filhanteringsassistent som hjälper användare att läsa och skriva till filer."
        ),
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={
                    "write_file": True,
                    "read_file": False,
                },
            ),
        ],
        checkpointer=InMemorySaver(),
    )

    while True:
        user_input = get_user_input()

        process_stream = agent.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,
            stream_mode=STREAM_MODES,
        )
        handle_stream(process_stream)

        state = agent.get_state(config)
        interrupts = [
            interrupt
            for task in state.tasks
            for interrupt in task.interrupts
        ]

        if interrupts and print_interrupt_info({"__interrupt__": interrupts}):
            decision = get_user_decision()
            resume_stream = agent.stream(
                Command(resume={"decisions": [decision]}),
                config=config,
                stream_mode=STREAM_MODES,
            )
            handle_stream(resume_stream)


if __name__ == "__main__":
    run()
