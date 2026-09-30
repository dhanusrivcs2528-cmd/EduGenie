from typing import List

from pydantic import BaseModel, Field


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000,
        description="Text supplied by the learner.",
    )


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="Question asked by the learner.",
    )


class TopicRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Topic the learner wants to study.",
    )

    level: str = Field(
        default="beginner",
        min_length=1,
        max_length=50,
        description="Learner's current level.",
    )


class QuizQuestion(BaseModel):
    question: str
    options: List[str] = Field(min_length=4, max_length=4)
    correct_answer: str
    explanation: str


class QuizResponse(BaseModel):
    title: str
    questions: List[QuizQuestion]


class LearningStep(BaseModel):
    order: int
    topic: str
    difficulty: str
    estimated_time: str
    description: str
    resources: List[str]


class LearningPathResponse(BaseModel):
    topic: str
    learner_level: str
    overview: str
    steps: List[LearningStep]