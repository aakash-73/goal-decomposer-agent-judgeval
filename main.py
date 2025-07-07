from src.agents.goal_decomposer import goal_decomposer_agent, run_evaluation, GROQ_API_KEY, OPENAI_API_KEY

def main():
    print("Select which API to use for goal decomposition:")
    print("1 - Groq API")
    print("2 - OpenAI API")
    choice = input("Enter 1 or 2: ").strip()

    if choice == "1":
        use_groq = True
        if not GROQ_API_KEY:
            print("❌ Error: GROQ_API_KEY not set in environment variables.")
            return
    elif choice == "2":
        use_groq = False
        if not OPENAI_API_KEY:
            print("❌ Error: OPENAI_API_KEY not set in environment variables.")
            return
    else:
        print("❌ Invalid choice. Please enter 1 or 2.")
        return

    # ✅ Take goal and timeframe from terminal input
    user_goal = input("\nEnter your high-level goal: ").strip()
    if not user_goal:
        print("❌ Goal cannot be empty.")
        return

    timeframe = input("Enter the timeframe to complete this goal (default: 6 months): ").strip()
    if not timeframe:
        timeframe = "6 months"

    print(f"\n🔧 Running goal decomposition using {'Groq' if use_groq else 'OpenAI'} API...\n")
    result = goal_decomposer_agent(user_goal, timeframe=timeframe, use_groq=use_groq)

    print("🧩 Goal Decomposition Result:")
    print(result["decomposition"])

    print("\n📊 Running evaluation on the decomposition...\n")
    run_evaluation(user_goal, result["decomposition"])


if __name__ == "__main__":
    main()
