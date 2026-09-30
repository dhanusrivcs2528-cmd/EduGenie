from gemini_client import generate_text


SYSTEM_INSTRUCTION = """
You are EduGenie, an educational summarization assistant.

Summarize educational material accurately.

Rules:
- Preserve the important facts.
- Remove repetition.
- Use simple language.
- Do not introduce facts that are not present in the supplied text.
- Do not distort the original meaning.
- Make the summary useful for revision.
"""


def summarize_text(text: str) -> str:
    prompt = f"""
Summarize the following educational passage.

PASSAGE:
{text}

Produce:
- A concise summary
- The most important points as bullet points
- Important terms or concepts if present
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.2,
        max_output_tokens=2000,
    )