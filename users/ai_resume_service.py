# users/ai_resume_service.py
import json
import os
from typing import Any, Dict, List, Tuple

import requests


def _enabled_sections(schema: Dict[str, Any]) -> List[str]:
    sections = (schema or {}).get("sections") or {}
    enabled = [k for k, v in sections.items() if (v or {}).get("enabled") is True]
    return enabled or ["header", "summary", "experience", "education", "skills", "projects"]


def _build_resume_json_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
    enabled = set(_enabled_sections(schema))

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

    # Drop disabled sections
    for key in list(props.keys()):
        if key in ("certifications", "languages"):
            if key not in enabled:
                props.pop(key, None)
        else:
            if key not in enabled:
                props.pop(key, None)

    required_fields = [k for k in props.keys() if k not in ("certifications", "languages")]

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


def _extract_text(resp_json: Dict[str, Any]) -> str:
    # Responses API format: output -> content -> {type:"output_text", text:"..."} :contentReference[oaicite:2]{index=2}
    out = resp_json.get("output")
    if isinstance(out, list):
        chunks: List[str] = []
        for item in out:
            if not isinstance(item, dict):
                continue
            content = item.get("content")
            if not isinstance(content, list):
                continue
            for c in content:
                if isinstance(c, dict) and c.get("type") in ("output_text", "text"):
                    t = c.get("text")
                    if isinstance(t, str) and t.strip():
                        chunks.append(t)
        if chunks:
            return "\n".join(chunks).strip()

    # fallback
    if isinstance(resp_json.get("output_text"), str):
        return resp_json["output_text"].strip()

    raise ValueError("OpenAI response parse failed (no text found)")


def generate_ai_resume(schema: Dict[str, Any], prompt: str, language: str = "en") -> Tuple[str, Dict[str, Any]]:
    api_key = os.getenv("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY missing in environment/.env")

    json_schema = _build_resume_json_schema(schema)

    instructions = (
        "You are a professional resume writer. "
        "Return STRICT JSON matching the provided schema (no extra keys, no markdown). "
        "ATS-friendly, impact-driven bullets, use metrics where reasonable. "
        "Dates: YYYY-MM or YYYY, and 'Present' for current roles."
    )

    if language == "hi":
        instructions += " Write all text values in Hindi (JSON keys remain English)."
    elif language == "mr":
        instructions += " Write all text values in Marathi (JSON keys remain English)."

    payload = {
        "model": "gpt-4o-mini",
        "instructions": instructions,
        "input": [
            {
                "role": "user",
                "content": f"Generate resume JSON for this user:\n{prompt}",
            }
        ],
        # ✅ Structured Outputs for Responses: text.format json_schema strict :contentReference[oaicite:3]{index=3}
        "text": {
            "format": {
                "type": "json_schema",
                "name": "resume_payload",
                "schema": json_schema,
                "strict": True,
            }
        },
        "max_output_tokens": 1600,
        "store": False,
    }

    r = requests.post(
        "https://api.openai.com/v1/responses",
        headers={
            "Authorization": f"Bearer {api_key}",  # keep secret server-side :contentReference[oaicite:4]{index=4}
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=60,
    )

    if r.status_code >= 400:
        raise ValueError(f"OpenAI error {r.status_code}: {r.text}")

    text = _extract_text(r.json())
    data = json.loads(text)

    title = data.get("title") or "AI Generated Resume"
    resume = data.get("resume") or {}
    return title, resume
