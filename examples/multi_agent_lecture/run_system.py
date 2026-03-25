from .supervisor import run_system


if __name__ == "__main__":
    user_input = {
        "job_type": "AI",
        "work_type": "heltid"
    }

    result = run_system(user_input)

    print("\n✅ SLUTRESULTAT:")
    print(result)