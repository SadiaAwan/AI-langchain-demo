from langchain.agents import create_agent
from langchain.agents.middleware import before_model, AgentState
from langchain.messages import AIMessage
from langgraph.runtime import Runtime
from typing import Any

from util.models import get_model
from util.streaming_utils import STREAM_MODES, handle_stream
from util.pretty_print import get_user_input
from util.tools import get_current_time, calculate


@before_model(can_jump_to=["end"])
def filter_long_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    """Blockerar meddelanden som är över 100 tecken."""
    if not state["messages"]:
        return None

    last_message = state["messages"][-1]
    if len(str(last_message.content)) > 100:
        return {
            "messages": [AIMessage(content="Meddelandet är för långt, vänligen förenkla det.")],
            "jump_to": "end"
        }

    return None


def run():
    # Get predefined attributes
    model = get_model()

    # Create agent
    agent = create_agent(
        model=model,
        tools=[get_current_time, calculate],
        system_prompt=(
            "Du är en hjälpsam assistent"
        ),
        middleware=[filter_long_messages],
    )

    # Get user input
    user_input = get_user_input("Ställ din fråga")

    # Call the agent
    process_stream = agent.stream(
        {"messages": [{"role": "user", "content": user_input}]},
        stream_mode=STREAM_MODES,
    )

    # Stream the process
    handle_stream(process_stream)


if __name__ == "__main__":
    run()
