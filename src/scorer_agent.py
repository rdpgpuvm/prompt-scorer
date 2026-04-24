"""
Prompt Quality Scoring Agent
Evaluates prompts on 5 criteria: Clarity, Specificity, Context, Format, Persona.
"""
import os
from typing import Dict, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


class PromptScore(BaseModel):
    """Structured output for prompt scoring."""
    prompt: str = Field(description="The submitted prompt.")
    final_score: float = Field(description="Overall score out of 10.")
    criteria_scores: Dict[str, float] = Field(
        description="Scores per criterion (Clarity, Specificity, Context, Format, Persona)."
    )
    feedback: str = Field(description="General qualitative feedback.")
    suggestions: List[str] = Field(description="2-3 actionable improvement suggestions.")


SYSTEM_PROMPT = (
    "You are an expert AI prompt engineer. Evaluate the user's prompt on 5 criteria:\n"
    "1. Clarity — Is the request unambiguous and easy to understand?\n"
    "2. Specificity/Details — Does it include enough detail (audience, scope, examples)?\n"
    "3. Context — Is background or situational context provided?\n"
    "4. Output Format & Constraints — Does it specify desired format, length, or constraints?\n"
    "5. Persona/Role — Is a role or perspective assigned to the responder?\n\n"
    "Score each 0-10. Final score = average. Provide 2-3 concrete suggestions."
)


def score_prompt(user_prompt: str, api_key: str | None = None) -> PromptScore:
    """Score a single prompt using structured LLM output."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
    )

    structured_llm = llm.with_structured_output(PromptScore)
    result = structured_llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Score this prompt:\n---\n{user_prompt}"),
    ])
    result.prompt = user_prompt
    return result


def score_prompt_raw(user_prompt: str, api_key: str | None = None) -> dict:
    """Return a plain dict (useful for API responses)."""
    score = score_prompt(user_prompt, api_key)
    return {
        "prompt": score.prompt,
        "final_score": score.final_score,
        "criteria_scores": score.criteria_scores,
        "feedback": score.feedback,
        "suggestions": score.suggestions,
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Prompt Quality Scoring Agent")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt to score")
    args = parser.parse_args()

    result = score_prompt(args.prompt)
    print(f"\nFinal Score: {result.final_score:.1f}/10")
    print("Criteria:")
    for k, v in result.criteria_scores.items():
        print(f"  {k}: {v:.1f}")
    print(f"\nFeedback: {result.feedback}")
    print("Suggestions:")
    for s in result.suggestions:
        print(f"  • {s}")
