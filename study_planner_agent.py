from langchain.agents import create_agent

from util.models import get_model

SYSTEM_PROMPT = """
ROLE:
You are an expert learning strategist AI.

TASK:
1. Break down a learning goal into sub-skills.
2. Define measurable milestones.
3. Create a structured study plan.
4. Suggest exercises.

OUTPUT FORMAT:
- Required Competencies
- Milestones
- Weekly Study Plan
- Practice Suggestions
"""

def main():
    model = get_model()

    agent = create_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
    )

    goal = input("Enter learning goal: ")

    response = agent.invoke(
        {"messages": [("user", goal)]}
    )

    print(response["messages"][-1].content)


if __name__ == "__main__":
    main()