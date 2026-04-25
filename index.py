from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
import os
from jinja2 import Environment, FileSystemLoader

app = FastAPI(title="Prompt Quality Scorer")

# Use raw jinja2 to avoid starlette templating issues
jinja_env = Environment(loader=FileSystemLoader("templates"))

def render_template(name, **context):
    template = jinja_env.get_template(name)
    return template.render(**context)

# Simple scorer
def score_prompt_raw(prompt: str):
    words = len(prompt.split())
    clarity = min(10, max(2, words * 0.5 + 3))
    specificity = min(10, max(2, words * 0.3 + 2))
    context = min(10, max(1, words * 0.2 + 1))
    format_score = min(10, max(1, words * 0.15 + 1))
    persona = min(10, max(1, words * 0.25 + 1))
    final = round((clarity + specificity + context + format_score + persona) / 5, 1)
    
    return {
        "prompt": prompt,
        "final_score": final,
        "criteria_scores": {
            "Clarity": round(clarity, 1),
            "Specificity": round(specificity, 1),
            "Context": round(context, 1),
            "Format": round(format_score, 1),
            "Persona": round(persona, 1),
        },
        "feedback": f"This prompt has {words} words. " + ("Strong prompt with good detail." if final > 7 else "Consider adding more context, specificity, and format requirements."),
        "suggestions": [
            "Add target audience or persona",
            "Specify desired output format",
            "Include more context or examples"
        ]
    }

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    html = render_template("index.html", request=request, result=None)
    return HTMLResponse(content=html)

@app.post("/", response_class=HTMLResponse)
async def score(request: Request, prompt: str = Form(...)):
    result = score_prompt_raw(prompt)
    html = render_template("index.html", request=request, result=result)
    return HTMLResponse(content=html)

@app.post("/api/score")
async def api_score(prompt: str = Form(...)):
    return score_prompt_raw(prompt)
