from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from config import APP_NAME, GEMINI_API_KEY, GEMINI_MODEL
from explanation_module import explain_concept
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from schemas import (
    LearningPathResponse,
    QuestionRequest,
    QuizResponse,
    TextRequest,
    TopicRequest,
)
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title=APP_NAME,
    description="AI-powered educational learning assistant.",
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={
        "app_name": "EduGenie"
    }
)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "application": APP_NAME,
        "gemini_configured": bool(GEMINI_API_KEY),
        "gemini_model": GEMINI_MODEL,
    }


@app.post("/qa")
async def qa(request: QuestionRequest):
    try:
        answer = answer_question(request.question)

        return {
            "success": True,
            "answer": answer,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/explain")
async def explain(request: TextRequest):
    try:
        explanation = explain_concept(request.text)

        return {
            "success": True,
            "explanation": explanation,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/quiz", response_model=QuizResponse)
async def quiz(request: TextRequest):
    try:
        return generate_quiz(request.text)

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post("/summarize")
async def summarize(request: TextRequest):
    try:
        summary = summarize_text(request.text)

        return {
            "success": True,
            "summary": summary,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc


@app.post(
    "/learn/recommendations",
    response_model=LearningPathResponse,
)
async def learning_recommendations(request: TopicRequest):
    try:
        return get_learning_recommendations(
            request.topic,
            request.level,
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc