"""
Prompt Quality Scoring Agent
Evaluates prompts on 5 criteria: Clarity, Specificity, Context, Format, Persona.
"""
import os
import json
import re
from typing import Dict, List
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage


class PromptScore(BaseModel):
    """Structured output for prompt scoring."""
    final_score: float = Field(description="Overall score out of 10.")
    clarity: float = Field(description="Clarity score 0-10")
    specificity: float = Field(description="Specificity/Details score 0-10")
    context: float = Field(description="Context score 0-10")
    format_constraints: float = Field(description="Output Format & Constraints score 0-10")
    persona: float = Field(description="Persona/Role score 0-10")
    feedback: str = Field(description="General qualitative feedback.")
    suggestion_1: str = Field(description="First actionable improvement suggestion.")
    suggestion_2: str = Field(description="Second actionable improvement suggestion.")
    suggestion_3: str = Field(description="Third actionable improvement suggestion.")


SYSTEM_PROMPT = """You are an expert AI prompt engineer. Evaluate the user's prompt on 5 criteria:
1. Clarity — Is the request unambiguous and easy to understand?
2. Specificity/Details — Does it include enough detail (audience, scope, examples)?
3. Context — Is background or situational context provided?
4. Output Format & Constraints — Does it specify desired format, length, or constraints?
5. Persona/Role — Is a role or perspective assigned to the responder?

Score each 0-10. Final score = average. Provide 3 concrete suggestions.

Respond with ONLY valid JSON in this exact format:
{
  "final_score": 7.5,
  "clarity": 8.0,
  "specificity": 7.0,
  "context": 6.0,
  "format_constraints": 8.0,
  "persona": 7.5,
  "feedback": "Your feedback here.",
  "suggestion_1": "First suggestion.",
  "suggestion_2": "Second suggestion.",
  "suggestion_3": "Third suggestion."
}"""


def extract_json(text: str) -> dict:
    """Extract JSON from text, handling markdown code blocks."""
    # Try to find JSON in markdown code blocks
    pattern = r'```(?:json)?\s*(.*?)\s*```'
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return json.loads(matches[0])
    
    # Try to find raw JSON object
    pattern = r'\{.*\}'
    matches = re.findall(pattern, text, re.DOTALL)
    if matches:
        return json.loads(matches[0])
    
    raise ValueError("No JSON found in response")


def score_prompt_raw(user_prompt: str, api_key: str | None = None) -> dict:
    """Score a single prompt and return a plain dict."""
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        api_key=api_key or os.getenv("OPENAI_API_KEY"),
    )

    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=f"Score this prompt:\n---\n{user_prompt}"),
    ])

    data = extract_json(response.content)
    
    return {
        "prompt": user_prompt,
        "final_score": data.get("final_score", 0),
        "criteria_scores": {
            "Clarity": data.get("clarity", 0),
            "Specificity": data.get("specificity", 0),
            "Context": data.get("context", 0),
            "Format": data.get("format_constraints", 0),
            "Persona": data.get("persona", 0),
        },
        "feedback": data.get("feedback", ""),
        "suggestions": [
            data.get("suggestion_1", ""),
            data.get("suggestion_2", ""),
            data.get("suggestion_3", ""),
        ],
    }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Prompt Quality Scoring Agent")
    parser.add_argument("--prompt", type=str, required=True, help="Prompt to score")
    args = parser.parse_args()

    result = score_prompt_raw(args.prompt)
    print(f"\nFinal Score: {result['final_score']:.1f}/10")
    print("Criteria:")
    for k, v in result["criteria_scores"].items():
        print(f"  {k}: {v:.1f}")
    print(f"\nFeedback: {result['feedback']}")
    print("Suggestions:")
    for s in result["suggestions"]:
        print(f"  • {s}")
