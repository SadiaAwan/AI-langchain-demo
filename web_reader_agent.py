from langchain.agents import create_agent
from langchain.tools import tool

from util.models import get_model
import requests
from bs4 import BeautifulSoup

# =========================
# TOOL
# =========================
@tool
def read_webpage(url: str) -> str:
    """Fetch and return text content from a webpage."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")
        text = soup.get_text()

        return text[:4000]

    except Exception as e:
        return f"Error fetching webpage: {e}"


# =========================
# SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
ROLE:
You are a web analysis AI.

IMPORTANT RULES:
- You must only call the tool with the exact parameter: url
- Do NOT invent additional parameters
- Do NOT modify headers
- Do NOT attempt to bypass captcha
- Only use the tool exactly as defined

TASK:
1. Call the tool once.
2. Analyze returned text.
3. Provide:

OUTPUT FORMAT:
- Summary
- Key Topics
- Important Insights
"""


# =========================
# MAIN
# =========================
def main():
    model = get_model()

    agent = create_agent(
    model=model,
    tools=[read_webpage],
    system_prompt=SYSTEM_PROMPT,
)

    url = input("Enter URL: ")

    response = agent.invoke(
        {"messages": [("user", f"Analyze this webpage: {url}")]}
    )

    print(response["messages"][-1].content)

if __name__ == "__main__":
    main()