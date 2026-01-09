import json
from huggingface_hub import InferenceClient
from config import HF_API_KEY, MODEL_NAME
from prompts import CONCEPT_PROMPT, QUIZ_PROMPT

# Hugging Face client
client = InferenceClient(
    token=HF_API_KEY,
)

def _safe_json(text: str):
    """
    Llama may add text around JSON.
    Extract JSON array safely.
    """
    try:
        return json.loads(text)
    except Exception:
        start = text.find("[")
        end = text.rfind("]") + 1
        if start != -1 and end != -1:
            try:
                return json.loads(text[start:end])
            except Exception:
                pass
    return []

def _chat(prompt: str, temperature=0.7, max_tokens=2048):
    """
    Correct way to call Llama 3 via Hugging Face
    """
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": "You are a precise assistant that replies ONLY in valid JSON."},
            {"role": "user", "content": prompt},
        ],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return response.choices[0].message.content

def extract_concepts(text: str) -> list:
    prompt = CONCEPT_PROMPT.format(text=text[:12000])
    output = _chat(prompt, temperature=0.3, max_tokens=512)
    return _safe_json(output)

def generate_questions(text, n, include_explanations, difficulty_hint):
    prompt = QUIZ_PROMPT.format(
        text=text[:12000],
        n=n,
        difficulty=difficulty_hint,
        explanations=include_explanations
    )
    output = _chat(prompt, temperature=0.7, max_tokens=2048)
    return _safe_json(output)
