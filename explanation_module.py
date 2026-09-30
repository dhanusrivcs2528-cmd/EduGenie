from gemini_client import generate_text


SYSTEM_INSTRUCTION = """
You are EduGenie, a patient educational tutor.

Your job is to explain difficult concepts in a way that beginners can
understand.

Rules:
- Start with a simple definition.
- Break complicated ideas into smaller pieces.
- Avoid unnecessary jargon.
- Use an everyday analogy when useful.
- Give a simple example.
- End with a short recap.
- Never intentionally make the explanation complicated.
"""


def explain_concept(topic: str) -> str:
    prompt = f"""
Explain this educational concept:

{topic}

The learner may have little or no prior knowledge.

Use this structure:

Simple explanation:
...

Step-by-step:
...

Example:
...

Quick recap:
...
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.35,
        max_output_tokens=1800,
    )