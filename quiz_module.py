from gemini_client import generate_structured
from schemas import QuizResponse


SYSTEM_INSTRUCTION = """
You are EduGenie, an educational quiz generator.

Generate high-quality multiple-choice questions from the supplied material.

Rules:
- Generate exactly 3 questions.
- Every question must have exactly 4 options.
- Exactly one option must be correct.
- The correct_answer must exactly match one of the options.
- Questions must be answerable from the supplied material.
- Distractors should be plausible but clearly incorrect.
- Provide a short explanation for every correct answer.
- Do not include Markdown formatting inside fields.
"""


def generate_quiz(text: str) -> QuizResponse:
    prompt = f"""
Create a three-question educational quiz from this material:

{text}

Return:
- A suitable quiz title.
- Exactly 3 multiple-choice questions.
- Exactly 4 options per question.
- One correct answer per question.
- A short explanation for each answer.
"""

    result = generate_structured(
        prompt,
        QuizResponse,
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.25,
        max_output_tokens=2500,
    )

    # Defensive validation.
    if len(result.questions) != 3:
        raise RuntimeError(
            "The AI did not return exactly 3 quiz questions."
        )

    for question in result.questions:
        if len(question.options) != 4:
            raise RuntimeError(
                "A quiz question did not contain exactly 4 options."
            )

        if question.correct_answer not in question.options:
            raise RuntimeError(
                "A correct answer was not present in the options."
            )

    return result