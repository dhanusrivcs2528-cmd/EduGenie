from gemini_client import generate_structured
from schemas import LearningPathResponse


SYSTEM_INSTRUCTION = """
You are EduGenie, a personalized educational planning assistant.

Create practical learning paths for students.

Rules:
- Start from the learner's stated level.
- Progress from foundational concepts to advanced concepts.
- Use a logical order.
- Give realistic estimated study times.
- Explain what each step teaches.
- Suggest useful resource TYPES or resource names.
- Do not invent specific URLs.
- Keep the path achievable.
"""


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
) -> LearningPathResponse:

    prompt = f"""
Create a personalized learning path.

Topic:
{topic}

Learner level:
{level}

The learning path should:
- Begin at the learner's current level.
- Progress toward advanced understanding.
- Contain approximately 6 to 8 learning steps.
- Include difficulty.
- Include estimated time.
- Include a description.
- Include useful resources such as documentation, books,
  courses, articles, exercises, or videos.

Do not fabricate URLs.
"""

    result = generate_structured(
        prompt,
        LearningPathResponse,
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.35,
        max_output_tokens=4000,
    )

    return result