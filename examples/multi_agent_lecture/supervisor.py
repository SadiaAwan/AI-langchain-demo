from .intake_agent import intake_agent
from .job_agent import job_matching_agent
from .evaluation_agent import evaluation_agent
from .recommendation_agent import recommendation_agent


def run_system(user_input):
    print("🧠 Supervisor startar systemet...\n")

    profile = intake_agent(user_input)

    jobs = job_matching_agent(profile)

    decision = evaluation_agent(jobs)

    result = recommendation_agent(decision)

    return result