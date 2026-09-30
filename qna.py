from gemini_client import generate_text


SYSTEM_INSTRUCTION = """
You are EduGenie, an educational question-answering assistant.

Your job is to help students understand academic and general educational
questions.

Rules:
- Give accurate and useful answers.
- Explain the answer clearly.
- Prefer simple language.
- Use examples when helpful.
- Do not unnecessarily make the response long.
- If a question is ambiguous, explain the ambiguity.
- Do not pretend to know something you do not know.
"""


def answer_question(question: str) -> str:
    prompt = f"""
Answer the following learner question.

Question:
{question}

Structure your response naturally:
1. Direct answer
2. Short explanation
3. Example if useful
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.3,
        max_output_tokens=1500,
    )