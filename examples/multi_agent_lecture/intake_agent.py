def intake_agent(user_input):
    print("📥 Intake Agent körs...")

    profile = {
        "name": "Test User",
        "skills": ["Python", "AI"],
        "job_type": user_input.get("job_type", "developer"),
        "work_type": user_input.get("work_type", "heltid")
    }

    return profile