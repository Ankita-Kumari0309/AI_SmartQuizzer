CONCEPT_PROMPT = """
Extract the most important learning concepts from the text below.

Rules:
- Return ONLY a valid JSON array
- Do NOT include markdown, comments, or explanations
- Each item must be a short noun phrase (3–6 words)
- Avoid full sentences
- Avoid duplicates or overlapping ideas
- Keep concepts meaningful and distinct
- Maximum 15 concepts

Example output:
["Neural Networks", "Backpropagation", "Gradient Descent"]

TEXT:
{text}
"""


QUIZ_PROMPT = """
Generate {n} high-quality multiple-choice questions from the text below.

STRICT RULES:
- Output MUST be valid JSON only
- Do NOT include markdown
- Do NOT include any text outside JSON
- Each question must test a DIFFERENT concept
- Questions must be clear, concise, and unambiguous
- Difficulty level must strictly follow: {difficulty}
- Each question must have exactly 4 options:
  - 1 correct answer
  - 3 incorrect but realistic distractors
- Distractors must NOT repeat the correct answer
- Avoid vague or opinion-based questions
- Avoid repeating similar wording across questions
- Explanation must clearly justify why the answer is correct
- Explanation length: 1–3 sentences
- Use simple, student-friendly language

JSON FORMAT (must match exactly):
[
  {{
    "question": "string",
    "answer": "string",
    "distractors": ["string", "string", "string"],
    "difficulty": "easy | medium | hard",
    "explanation": "string"
  }}
]

TEXT:
{text}
"""
