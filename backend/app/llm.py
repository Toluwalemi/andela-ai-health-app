import json

from fastapi import HTTPException, status
from openai import AsyncOpenAI

from app.config import get_settings
from app.schemas import ConsultationResponse

SYSTEM_PROMPT = """You are a medical scribe assistant.
Given raw consultation notes, return JSON with exactly three fields:
- "summary": a concise clinical summary (2-3 sentences).
- "next_steps": recommended follow-up actions as a short bulleted list.
- "patient_email": a warm, plain-English email to the patient summarising the visit.

Do not diagnose. Always end the patient_email with a disclaimer instructing
the patient to contact their provider for medical advice.
Respond with JSON only, no prose outside the object."""


def _client() -> AsyncOpenAI:
    settings = get_settings()
    return AsyncOpenAI(
        api_key=settings.openrouter_api_key,
        base_url="https://openrouter.ai/api/v1",
    )


async def summarise_consultation(notes: str) -> ConsultationResponse:
    settings = get_settings()
    completion = await _client().chat.completions.create(
        model=settings.openrouter_model,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": notes},
        ],
    )
    raw = completion.choices[0].message.content or "{}"
    try:
        payload = json.loads(raw)
        return ConsultationResponse(**payload)
    except (json.JSONDecodeError, ValueError) as exc:
        raise HTTPException(
            status.HTTP_502_BAD_GATEWAY,
            f"Upstream model returned an unparseable response: {exc}",
        ) from exc
