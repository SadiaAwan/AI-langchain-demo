def evaluation_agent(jobs):
    print("⚖️ Evaluation Agent körs...")

    best_match = max(jobs, key=lambda x: x["match"])

    decision = {
        "best_job": best_match,
        "needs_training": best_match["match"] < 75
    }

    return decision