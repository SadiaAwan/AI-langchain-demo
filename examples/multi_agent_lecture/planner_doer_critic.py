from typing import Literal, Optional

from pydantic import BaseModel, Field

from langchain.agents import create_agent
from util.models import AvailableModels, get_model
from util.streaming_utils import STREAM_MODES, handle_stream, handle_structured_stream
from util.pretty_print import get_user_input, print_section, Colors

MAX_ITERATIONS = 3


class CriticVerdict(BaseModel):
    """Structured verdict from the critic agent."""

    feedback: str = Field(
        description="Kort, konkret feedback på koden.",
    )
    status: Literal["APPROVED", "REJECTED"] = Field(
        description="APPROVED om koden uppfyller planens mål, annars REJECTED"
    )


def build_agents():
    big_model = get_model(AvailableModels.LLAMA_70B)
    small_model = get_model(AvailableModels.LLAMA_8B)

    planner_agent = create_agent(
        model=big_model,
        name="planner_agent",
        system_prompt=(
            "Du är Planner Agent i ett flöde för enkel kodgenerering. "
            "Din uppgift är att analysera användarens mål och skapa en liten, tydlig plan för implementation.\n\n"
            "Instruktioner:\n"
            "- Identifiera exakt vad funktionen ska göra.\n"
            "- Lista relevanta edge cases.\n"
            "- Föreslå 2–4 enkla testexempel med förväntat resultat.\n"
            "- Håll planen kort och konkret.\n"
            "- Skriv inte själva lösningen i kod.\n\n"
            "Returnera endast: mål, krav, edge cases, testexempel."
        ),
    )

    doer_agent = create_agent(
        model=small_model,
        name="doer_agent",
        system_prompt=(
            "Du är Doer Agent i ett flöde för enkel kodgenerering. "
            "Din uppgift är att skriva Python-kod utifrån en förbestämd plan.\n\n"
            "Instruktioner:\n"
            "- Skriv en liten, korrekt och lättläst Python-funktion som uppfyller målet.\n"
            "- Följ kraven och hantera edge cases som finns i den förbestämda planen.\n"
            "- Använd enkel och tydlig kod framför smarta men svårlästa lösningar.\n"
        ),
    )

    critic_agent = create_agent(
        model=big_model,
        name="critic_agent",
        response_format=CriticVerdict,
        system_prompt=(
            "Du är Verifier Agent i ett flöde för enkel kodgenerering. "
            "Din uppgift är att granska om den föreslagna Python-koden uppfyller planens mål och är begriplig.\n\n"
            "Instruktioner:\n"
            "- Kontrollera att koden löser användarens uppgift korrekt.\n"
            "- Kontrollera att relevanta edge cases är hanterade eller tydligt avgränsade.\n"
            "- Kontrollera att koden är lätt att förstå och rimligt namngiven.\n"
            "- Bedöm endast utifrån användarens mål, planen och den föreslagna koden.\n"
        ),
    )

    return planner_agent, doer_agent, critic_agent


def call_agent(agent, message: str, agent_name: str) -> str:
    return handle_stream(
        agent.stream(
            {"messages": [{"role": "user", "content": message}]},
            stream_mode=STREAM_MODES,
        ),
        agent_name=agent_name,
    )



def run():
    planner, doer, critic = build_agents()

    user_goal = get_user_input("Input")

    feedback = ""
    solution = ""
    plan = ""

    for iteration in range(1, MAX_ITERATIONS + 1):
        print_section(
            f"Iteration {iteration}/{MAX_ITERATIONS}",
            color=Colors.BRIGHT_CYAN,
        )

        # --- PLANNER ---
        planner_prompt = f"Mål: {user_goal}"
        if feedback:
            planner_prompt += (
                f"\n\nTidigare, ej godkänd lösning:\n{solution}"
                f"\n\nFeedback:\n{feedback}"
                "\n\nSkapa en ny plan."
            )
        plan = call_agent(planner, planner_prompt, "planner_agent")

        # --- DOER ---
        doer_prompt = f"Plan att utföra:\n{plan}"
        result = call_agent(doer, doer_prompt, "doer_agent")
        solution = result

        # --- CRITIC ---
        critic_prompt = (
            f"Plan:\n{plan}\n\n"
            f"Implementering:\n{result}"
        )
        verdict: CriticVerdict = handle_structured_stream(
            critic.stream(
                {"messages": [{"role": "user", "content": critic_prompt}]},
                stream_mode=STREAM_MODES,
            ),
            agent_name="critic_agent",
        )

        if verdict.status == "APPROVED":
            print_section("Godkänd!", color=Colors.BRIGHT_GREEN)
            return

        feedback = verdict.feedback or ""
        if iteration < MAX_ITERATIONS:
            print_section("Ej godkänd. Itera med feedback...", color=Colors.BRIGHT_YELLOW)

    print_section("Ej godkänd. Max iterationer nådda.", color=Colors.BRIGHT_YELLOW)


if __name__ == "__main__":
    run()
