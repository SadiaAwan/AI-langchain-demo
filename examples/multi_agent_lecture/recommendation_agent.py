from .tools import search_education


def ask_user():
    answer = input("Vill du bli kontaktad? (ja/nej): ")
    return answer.lower() == "ja"


def recommendation_agent(decision):
    print("📢 Recommendation Agent körs...")

    # Om matchningen är svag → föreslå utbildning
    if decision["needs_training"]:
        courses = search_education()

        result = {
            "message": "Vi rekommenderar utbildning innan du söker jobb.",
            "courses": courses
        }

    # Om matchningen är bra → visa jobb
    else:
        result = {
            "message": f"Du matchar jobbet: {decision['best_job']['title']}",
            "courses": []
        }

    # 🔁 Human-in-the-loop
    if ask_user():
        print("📞 Vi kontaktar dig!")
    else:
        print("❌ Ingen åtgärd.")

    return result