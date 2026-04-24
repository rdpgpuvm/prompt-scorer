# 🔮 Prompt Quality Scorer

AI-powered prompt evaluation tool. Scores any prompt across 5 dimensions and gives actionable feedback.

## Scoring Criteria (0-10 each)

| Criterion | What it measures |
|-----------|-----------------|
| **Clarity** | Is the request unambiguous? |
| **Specificity** | Enough detail (audience, scope, examples)? |
| **Context** | Background or situational info provided? |
| **Format** | Desired output format/length specified? |
| **Persona** | Role or perspective assigned? |

**Final Score** = average of the 5 criteria.

## Quick Start

```bash
pip install -r requirements.txt
python src/scorer_agent.py --prompt "Your prompt here"
```

## Web UI

```bash
uvicorn api.main:app --reload
# Open http://localhost:8000
```

## API Endpoint

```bash
curl -X POST https://your-app.vercel.app/api/score \
  -d "prompt=Explain quantum computing to a 10-year-old"
```

## Test Examples

| Prompt | Expected Score | Why |
|--------|---------------|-----|
| "What is AI?" | ~2/10 | No context, format, or specificity |
| "Write a summary of the French Revolution." | ~5/10 | Clear but missing audience, format, depth |
| "Act as a senior marketing consultant. Draft 5 catchy taglines for sustainable coffee beans targeting millennials who value ethical sourcing." | ~9/10 | Strong persona, specificity, context, format |

## Deploy

```bash
npx vercel --prod
```

Requires `OPENAI_API_KEY` environment variable.
