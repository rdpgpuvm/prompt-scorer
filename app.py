import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from scorer_agent import score_prompt_raw

app = FastAPI(title="Prompt Quality Scorer")

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "result": None})


@app.post("/", response_class=HTMLResponse)
async def score(request: Request, prompt: str = Form(...)):
    result = score_prompt_raw(prompt)
    return templates.TemplateResponse("index.html", {"request": request, "result": result})


@app.post("/api/score")
async def api_score(prompt: str = Form(...)):
    return score_prompt_raw(prompt)
