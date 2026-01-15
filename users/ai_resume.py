# users/ai_resume.py
import json
import os
from typing import Any, Dict, List, Optional, Tuple

import requests


def _enabled_sections(schema: Dict[str, Any]) -> List[str]:
    sections = (schema or {}).get("sections") or {}
    enabled = [k for k, v in sections.items() if (v or {}).get("enabled") is True]
    return enabled or ["header", "summary", "experience", "education", "skills", "projects"]


def _resume_schema_for(schema: Dict[str, Any]) -> Dict[str, Any]:
    enabled = set(_enabled_sections(schema))

    # base resume object (same as your frontend data structure)
    props: Dict[str, Any] = {
        "header": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "fullName": {"type": "string"},
                "jobTitle": {"type": "string"},
                "email": {"type": "string"},
                "phone": {"type": "string"},
                "location": {"type": "string"},
                "linkedin": {"type": "string"},
                "website": {"type": "string"},
            },
            "required": ["fullName", "jobTitle", "email", "phone", "location", "linkedin", "website"],
        },
        "summary": {"type": "string"},
        "experience": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "title": {"type": "string"},
                    "company": {"type": "string"},
                    "location": {"type": "string"},
                    "from": {"type": "string"},
                    "to": {"type": "string"},
                    "bullets": {"type": "array", "items": {"type": "string"}},
                },
                "required": ["title", "company", "location", "from", "to", "bullets"],
            },
        },
        "education": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "school": {"type": "string"},
                    "degree": {"type": "string"},
                    "from": {"type": "string"},
                    "to": {"type": "string"},
                },
                "required": ["school", "degree", "from", "to"],
            },
        },
        "skills": {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "programming": {"type": "array", "items": {"type": "string"}},
                "frameworks": {"type": "array", "items": {"type": "string"}},
                "tools": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["programming", "frameworks", "tools"],
        },
        "projects": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {"name": {"type": "string"}, "desc": {"type": "string"}},
                "required": ["name", "desc"],
            },
        },
        "certifications": {"type": "array", "items": {"type": "string"}},
        "languages": {"type": "array", "items": {"type": "string"}},
    }

    # Remove disabled sections (optional ones)
    # header is assumed enabled always in your builder but keep safe:
    for key in list(props.keys()):
        if key in ("certifications", "languages"):
            # only keep if enabled in schema
            if key not in enabled:
                props.pop(key, None)
        else:
            if key not in enabled:
                props.pop(key, None)

    required_fields = [k for k in props.keys() if k not in ("certifications", "languages")]

    # Final response schema (title + resume)
    return {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "title": {"type": "string"},
            "resume": {
                "type": "object",
                "additionalProperties": False,
                "properties": props,
                "required": required_fields,
            },
        },
        "required": ["title", "resume"],
    }


def _extract_output_text(resp_json: Dict[str, Any]) -> str:
    """
    Tries to extract assistant output text from Responses API result.
    """
    # New Responses API often returns output list with content items
    out = resp_json.get("output")
    if isinstance(out, list):
        chunks: List[str] = []
        for item in out:
            content = item.get("content") if isinstance(item, dict) else None
            if isinstance(content, list):
                for c in content:
                    if isinstance(c, dict) and c.get("type") in ("output_text", "text"):
                        t = c.get("text")
                        if isinstance(t, str) and t.strip():
                            chunks.append(t)
        if chunks:
            return "\n".join(chunks).strip()

    # Fallback (some SDK styles)
    if isinstance(resp_json.get("output_text"), str):
        return resp_json["output_text"].strip()

    raise ValueError("Could not extract output text from OpenAI response")


def generate_ai_resume(
    schema: Dict[str, Any],
    user_prompt: str,
    language: str = "en",
    model: str = "gpt-4o-mini",
    max_output_tokens: int = 1600,
) -> Tuple[str, Dict[str, Any]]:
    """
    Returns: (title, resume_dict)
    """
    api_key = os.getenv("OPENAI_API_KEY") or ""
    if not api_key:
        raise ValueError("OPENAI_API_KEY is missing in environment")

    json_schema = _resume_schema_for(schema)

    sys = (
        "You generate ATS-friendly resumes as STRICT JSON matching the provided schema. "
        "No extra keys. No markdown. "
        "Dates: use YYYY-MM when possible, else YYYY. "
        "Bullets: concise, impact-driven, metrics when possible."
    )
    if language.lower() == "hi":
        sys += " Output text values in Hindi (but keep JSON keys same)."
    elif language.lower() == "mr":
        sys += " Output text values in Marathi (but keep JSON keys same)."

    payload = {
        "model": model,
        "instructions": sys,
        "input": [
            {
                "role": "user",
                "content": (
                    "Generate a complete resume JSON.\n\n"
                    f"User details / requirements:\n{user_prompt}\n"
                ),
            }
        ],
        # Structured Outputs via Responses API text.format :contentReference[oaicite:4]{index=4}
        "text": {
            "format": {
                "type": "json_schema",
                "name": "resume_payload",
                "schema": json_schema,
                "strict": True,
            }
        },
        "max_output_tokens": max_output_tokens,
    }

    r = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",  # :contentReference[oaicite:5]{index=5}
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )
    if r.status_code >= 400:
        raise ValueError(f"OpenAI API error: {r.status_code} {r.text}")

    resp_json = r.json()
    text = _extract_output_text(resp_json)

    data = json.loads(text)
    title = data.get("title") or "AI Generated Resume"
    resume = data.get("resume") or {}
    return title, resume
