from langchain.agents import create_agent

from langgraph.checkpoint.memory import MemorySaver
from langchain.tools import tool


from util.models import get_model
from util.streaming_utils import STREAM_MODES, handle_stream
from util.pretty_print import get_user_input

# =========================
# TOOL
# =========================
@tool
def calculator(expression: str) -> str:
    """Används för att räkna matematiska uttryck."""
    try:
        return str(eval(expression))
    except Exception:
        return "Kunde inte räkna ut uttrycket."
    

# =========================
# TOOL: File Reader
# =========================

@tool
def read_file(file_path: str) -> str:
    """Läser innehållet i en textfil från datorn."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Fel vid läsning av fil: {str(e)}"


from langchain.tools import tool
import os


@tool
def read_file(file_path: str) -> str:
    """Läser en textfil."""
    if not os.path.exists(file_path):
        return "Filen hittades inte."
    
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


@tool
def improve_cv(cv_text: str, job_text: str) -> str:
    """Analyserar CV mot jobbannons och ger förbättringsförslag."""
    return f"""
    Analys av CV mot jobbannons:

    CV:
    {cv_text}

    Jobbannons:
    {job_text}

    Ge förbättringsförslag och skriv om CV så det matchar bättre.
    """


# =========================
# MAIN
# =========================

def run():
    # Get predefined attributes
    model = get_model(
    temperature= 0.7,
    top_p= 0.01

    )

    # Skapa memory saver
    memory = MemorySaver()
    exit
    # Create agent med minne
    agent = create_agent(
        model=model,
        tools=[read_file, improve_cv],
        system_prompt=(
            "Du är en karriärcoach. "
            "När användaren vill optimera sitt CV ska du läsa filer och använda verktyg. "
            "Svara professionellt på svenska."
        ),
        checkpointer=memory,  # 🔹 Viktig rad

    )


        # tools=[read_file],
        # system_prompt=(
        #     "Du är en hjälpsam assistent som svarar på användarens frågor."
        #     "Svara alltid på svenska och var koncis men informativ."
    #     ),
    #     checkpointer=memory,  # 🔹 Viktig rad
    # )

    print("Startar konversation. Skriv 'exit' för att avsluta.\n")

    # Thread ID krävs för att MemorySaver ska fungera
    config = {"configurable": {"thread_id": "conversation_1"}}

    while True:
        user_input = get_user_input("Ställ din fråga")

        if user_input.lower() == "exit":
            print("Avslutar konversation.")
            break

        process_stream = agent.stream(
            {"messages": [{"role": "user", "content": user_input}]},
            config=config,  # 🔹 Viktig rad
            stream_mode=STREAM_MODES,
        )

        handle_stream(process_stream)


if __name__ == "__main__":
    run()



    