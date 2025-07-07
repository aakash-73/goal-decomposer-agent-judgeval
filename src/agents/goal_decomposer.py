import os
from dotenv import load_dotenv
from groq import Groq
from openai import OpenAI
from judgeval.tracer import Tracer
from judgeval import JudgmentClient
from judgeval.data import Example
from judgeval.scorers import FaithfulnessScorer

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
JUDGMENT_API_KEY = os.getenv("JUDGMENT_API_KEY")
JUDGMENT_ORG_KEY = os.getenv("JUDGMENT_ORG_KEY")

if not JUDGMENT_API_KEY:
    raise ValueError("JUDGMENT_API_KEY is required for Judgeval tracing and evaluation.")

PROJECT_NAME = os.getenv("JUDGMENT_PROJECT_NAME", "goal-decomposer-agent")

groq_client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

tracer_kwargs = {
    "api_key": JUDGMENT_API_KEY,
    "project_name": PROJECT_NAME
}
if JUDGMENT_ORG_KEY:
    tracer_kwargs["org_key"] = JUDGMENT_ORG_KEY

judgment = Tracer(**tracer_kwargs)

eval_client = JudgmentClient()


@judgment.observe(span_type="function")
def goal_decomposer_agent(goal: str, timeframe: str = "6 months", use_groq: bool = True) -> dict:
    """
    Decomposes a goal into subtasks using Groq or OpenAI.
    """
    system_prompt = (
        "You are an expert planner. Given a high-level goal, you will break it into actionable, chronological subtasks. "
        "Each task should include:\n"
        "- step (name of the subtask)\n"
        "- priority (High, Medium, Low)\n"
        "- duration (how long it takes)\n"
        "- resources (helpful links or topics)\n"
        "- depends_on (list of previous steps)\n"
        "Output as a JSON list."
    )

    user_prompt = f"My goal is: '{goal}' to be completed in {timeframe}. Please decompose it into detailed steps."

    try:
        if use_groq:
            if not groq_client:
                raise RuntimeError("GROQ_API_KEY is missing or invalid.")
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )
        else:
            if not openai_client:
                raise RuntimeError("OPENAI_API_KEY is missing or invalid.")
            response = openai_client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
            )

        content = response.choices[0].message.content
        return {
            "goal": goal,
            "decomposition": content
        }

    except Exception as e:
        raise RuntimeError(f"Failed to get response from {'Groq' if use_groq else 'OpenAI'} API: {e}")


def run_evaluation(goal: str, decomposition: str):
    """
    Evaluates the decomposition using Judgeval.
    """
    example = Example(
        input=goal,
        actual_output=decomposition,
        retrieval_context=[
            "To become an AI Engineer, you typically need to learn Python, machine learning, deep learning, and build projects."
        ],
    )

    scorer = FaithfulnessScorer(threshold=0.5)

    try:
        eval_client.assert_test(
            examples=[example],
            scorers=[scorer],
            model="gpt-4.1"
        )
        print("✅ Evaluation passed successfully!")

    except Exception as e:
        if "Project limit exceeded" in str(e):
            print("❌ Project limit exceeded. Please upgrade your plan or use a different org/project.")
        else:
            print(f"❌ Evaluation failed: {e}")
