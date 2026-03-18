from langchain.agents import create_agent
from util.models import get_model
import os


# =========================
# SYSTEM PROMPT
# =========================
SYSTEM_PROMPT = """
ROLE:
You are a professional AI recruitment analyst.

OBJECTIVE:
Compare a CV with a job description and evaluate the match.

INSTRUCTIONS:
1. Extract required skills from the job description.
2. Extract skills from the CV.
3. Compare them logically.
4. Calculate a realistic match percentage.
5. Identify strengths.
6. Identify missing competencies.
7. Provide concrete improvement advice.

IMPORTANT:
- Do not hallucinate skills.
- Only use information explicitly found in the texts.
- Be objective and analytical.

OUTPUT FORMAT:

Match Score: <number>%

Matching Skills:
- skill 1
- skill 2

Missing Skills:
- skill 1
- skill 2

Strengths:
- explanation

Improvement Recommendations:
- recommendation 1
- recommendation 2
"""


# =========================
# FILE READER
# =========================
def read_file(filename):
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found in project root.")
    with open(filename, "r", encoding="utf-8") as f:
        return f.read()


# =========================
# MAIN
# =========================
def main():
    print("=== CV MATCH AGENT ===")

    model = get_model()

    agent = create_agent(
        model=model,
        system_prompt=SYSTEM_PROMPT,
    )

    try:
        cv_text = read_file("cv.txt")
        job_text = read_file("jobb.txt")
    except Exception as e:
        print(f"Error reading files: {e}")
        return

    user_prompt = f"""
    JOB DESCRIPTION:
    {job_text}

    CV:
    {cv_text}
    """

    response = agent.invoke(
        {"messages": [("user", user_prompt)]}
    )

    print("\n===== RESULT =====\n")
    print(response["messages"][-1].content)


if __name__ == "__main__":
    main()
