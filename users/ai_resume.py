# # users/ai_resume.py
# import json
# import os
# import requests

# OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
# # ✅ safest model for Structured Outputs
# OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini-2024-07-18")

# # ✅ IMPORTANT:
# # This must be the RAW JSON Schema object (NOT {"name":..,"schema":..} wrapper)
# RESUME_SCHEMA = {
#     "type": "object",
#     "additionalProperties": False,
#     "required": ["title", "data"],
#     "properties": {
#         "title": {"type": "string"},
#         "data": {
#             "type": "object",
#             "additionalProperties": False,
#             # ✅ MUST include ALL keys from properties when strict + additionalProperties=false
#             "required": [
#                 "header",
#                 "summary",
#                 "experience",
#                 "education",
#                 "skills",
#                 "projects",
#                 "certifications",
#                 "languages",
#                 "interests",
#                 "strengths",
#                 "achievements",
#                 "courses",
#             ],
#             "properties": {
#                 "header": {
#                     "type": "object",
#                     "additionalProperties": False,
#                     "required": [
#                         "fullName",
#                         "jobTitle",
#                         "email",
#                         "phone",
#                         "location",
#                         "linkedin",
#                         "website",
#                     ],
#                     "properties": {
#                         "fullName": {"type": "string"},
#                         "jobTitle": {"type": "string"},
#                         "email": {"type": "string"},
#                         "phone": {"type": "string"},
#                         "location": {"type": "string"},
#                         "linkedin": {"type": "string"},
#                         "website": {"type": "string"},
#                     },
#                 },
#                 "summary": {"type": "string"},
#                 "experience": {
#                     "type": "array",
#                     "items": {
#                         "type": "object",
#                         "additionalProperties": False,
#                         "required": ["title", "company", "location", "from", "to", "bullets"],
#                         "properties": {
#                             "title": {"type": "string"},
#                             "company": {"type": "string"},
#                             "location": {"type": "string"},
#                             "from": {"type": "string"},
#                             "to": {"type": "string"},
#                             "bullets": {"type": "array", "items": {"type": "string"}},
#                         },
#                     },
#                 },
#                 "education": {
#                     "type": "array",
#                     "items": {
#                         "type": "object",
#                         "additionalProperties": False,
#                         "required": ["school", "degree", "from", "to"],
#                         "properties": {
#                             "school": {"type": "string"},
#                             "degree": {"type": "string"},
#                             "from": {"type": "string"},
#                             "to": {"type": "string"},
#                         },
#                     },
#                 },
#                 "skills": {
#                     "type": "object",
#                     "additionalProperties": False,
#                     "required": ["programming", "frameworks", "tools"],
#                     "properties": {
#                         "programming": {"type": "array", "items": {"type": "string"}},
#                         "frameworks": {"type": "array", "items": {"type": "string"}},
#                         "tools": {"type": "array", "items": {"type": "string"}},
#                     },
#                 },
#                 "projects": {
#                     "type": "array",
#                     "items": {
#                         "type": "object",
#                         "additionalProperties": False,
#                         "required": ["name", "desc"],
#                         "properties": {
#                             "name": {"type": "string"},
#                             "desc": {"type": "string"},
#                         },
#                     },
#                 },

#                 # ✅ optional sections but REQUIRED by schema (return empty arrays if none)
#                 "certifications": {"type": "array", "items": {"type": "string"}},
#                 "languages": {"type": "array", "items": {"type": "string"}},
#                 "interests": {"type": "array", "items": {"type": "string"}},
#                 "strengths": {"type": "array", "items": {"type": "string"}},
#                 "achievements": {"type": "array", "items": {"type": "string"}},
#                 "courses": {"type": "array", "items": {"type": "string"}},
#             },
#         },
#     },
# }


# def call_openai_resume(prompt: str,response_schema: dict) -> dict:
#     if not OPENAI_API_KEY:
#         raise RuntimeError("OPENAI_API_KEY missing in environment (.env)")

#     url = "https://api.openai.com/v1/responses"
#     headers = {
#         "Authorization": f"Bearer {OPENAI_API_KEY}",
#         "Content-Type": "application/json",
#     }

#     instructions = (
#         "You are an expert resume writer.\n"
#         "Create a professional resume from the user's prompt.\n"
#         "Return ONLY JSON that matches the JSON Schema.\n"
#         "Use strong action verbs, quantified bullets, realistic dates.\n"
#         "If info missing, infer reasonable placeholders (but keep it believable).\n"
#     )

#     body = {
#         "model": OPENAI_MODEL,
#         "instructions": instructions,
#         "input": [{"role": "user", "content": prompt}],
#         "temperature": 0.2,
#         "text": {
#             "format": {
#                 "type": "json_schema",
#                 "name": "resume_data",
#                 "strict": True,
#                 "schema": response_schema,
#             }
#         },
#         "max_output_tokens": 2000,
#     }

#     r = requests.post(url, headers=headers, data=json.dumps(body), timeout=60)

#     # ✅ show real OpenAI error (super helpful)
#     if r.status_code >= 400:
#         raise RuntimeError(f"OpenAI error {r.status_code}: {r.text}")

#     payload = r.json()

#     # Extract output_text
#     out_text = ""
#     for item in payload.get("output", []):
#         if item.get("type") == "message":
#             for c in item.get("content", []):
#                 if c.get("type") == "output_text":
#                     out_text += c.get("text", "")

#     if not out_text.strip():
#         raise RuntimeError(f"No output_text. Raw: {payload}")

#     return json.loads(out_text)

# def build_dynamic_resume_schema(extra_text_fields: list[str]) -> dict:
#     # extra_text_fields => ["communication", "leadership", "references"] etc

#     base_required = [
#         "header", "summary", "experience", "education", "skills", "projects",
#         "certifications", "languages", "interests", "strengths", "achievements", "courses"
#     ]

#     # Add extra text fields as required too
#     data_required = list(dict.fromkeys(base_required + extra_text_fields))

#     # Base properties
#     data_properties = {
#         "header": {
#             "type": "object",
#             "additionalProperties": False,
#             "required": ["fullName", "jobTitle", "email", "phone", "location", "linkedin", "website"],
#             "properties": {
#                 "fullName": {"type": "string"},
#                 "jobTitle": {"type": "string"},
#                 "email": {"type": "string"},
#                 "phone": {"type": "string"},
#                 "location": {"type": "string"},
#                 "linkedin": {"type": "string"},
#                 "website": {"type": "string"},
#             },
#         },
#         "summary": {"type": "string"},
#         "experience": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "additionalProperties": False,
#                 "required": ["title", "company", "location", "from", "to", "bullets"],
#                 "properties": {
#                     "title": {"type": "string"},
#                     "company": {"type": "string"},
#                     "location": {"type": "string"},
#                     "from": {"type": "string"},
#                     "to": {"type": "string"},
#                     "bullets": {"type": "array", "items": {"type": "string"}},
#                 },
#             },
#         },
#         "education": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "additionalProperties": False,
#                 "required": ["school", "degree", "from", "to"],
#                 "properties": {
#                     "school": {"type": "string"},
#                     "degree": {"type": "string"},
#                     "from": {"type": "string"},
#                     "to": {"type": "string"},
#                 },
#             },
#         },
#         "skills": {
#             "type": "object",
#             "additionalProperties": False,
#             "required": ["programming", "frameworks", "tools"],
#             "properties": {
#                 "programming": {"type": "array", "items": {"type": "string"}},
#                 "frameworks": {"type": "array", "items": {"type": "string"}},
#                 "tools": {"type": "array", "items": {"type": "string"}},
#             },
#         },
#         "projects": {
#             "type": "array",
#             "items": {
#                 "type": "object",
#                 "additionalProperties": False,
#                 "required": ["name", "desc"],
#                 "properties": {
#                     "name": {"type": "string"},
#                     "desc": {"type": "string"},
#                 },
#             },
#         },

#         "certifications": {"type": "array", "items": {"type": "string"}},
#         "languages": {"type": "array", "items": {"type": "string"}},
#         "interests": {"type": "array", "items": {"type": "string"}},
#         "strengths": {"type": "array", "items": {"type": "string"}},
#         "achievements": {"type": "array", "items": {"type": "string"}},
#         "courses": {"type": "array", "items": {"type": "string"}},
#     }

#     # Add template-driven extra fields as TEXT sections
#     for k in extra_text_fields:
#         data_properties[k] = {"type": "string"}

#     return {
#         "type": "object",
#         "additionalProperties": False,
#         "required": ["title", "data"],
#         "properties": {
#             "title": {"type": "string"},
#             "data": {
#                 "type": "object",
#                 "additionalProperties": False,
#                 "required": data_required,
#                 "properties": data_properties,
#             },
#         },
#     }

# users/ai_resume.py
import json
import os
import requests
from typing import List, Dict, Any

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini-2024-07-18")

# Base optional arrays we always force (OpenAI strict requires required contains all keys)
OPTIONAL_ARRAY_KEYS = [
    "certifications",
    "languages",
    "interests",
    "strengths",
    "achievements",
    "courses",
]

BASE_KEYS = [
    "header",
    "summary",
    "experience",
    "education",
    "skills",
    "projects",
] + OPTIONAL_ARRAY_KEYS


def build_dynamic_resume_schema(extra_text_fields: List[str]) -> Dict[str, Any]:
    """
    extra_text_fields: list of keys like ["communication", "leadership", "references"]
    These will be added as string fields in data and REQUIRED (OpenAI strict + closed schema).
    """

    extra_text_fields = [x for x in extra_text_fields if isinstance(x, str) and x.strip()]
    extra_text_fields = list(dict.fromkeys(extra_text_fields))  # unique

    data_properties: Dict[str, Any] = {
        "header": {
            "type": "object",
            "additionalProperties": False,
            "required": ["fullName", "jobTitle", "email", "phone", "location", "linkedin", "website"],
            "properties": {
                "fullName": {"type": "string"},
                "jobTitle": {"type": "string"},
                "email": {"type": "string"},
                "phone": {"type": "string"},
                "location": {"type": "string"},
                "linkedin": {"type": "string"},
                "website": {"type": "string"},
            },
        },
        "summary": {"type": "string"},
        "experience": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["title", "company", "location", "from", "to", "bullets"],
                "properties": {
                    "title": {"type": "string"},
                    "company": {"type": "string"},
                    "location": {"type": "string"},
                    "from": {"type": "string"},
                    "to": {"type": "string"},
                    "bullets": {"type": "array", "items": {"type": "string"}},
                },
            },
        },
        "education": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["school", "degree", "from", "to"],
                "properties": {
                    "school": {"type": "string"},
                    "degree": {"type": "string"},
                    "from": {"type": "string"},
                    "to": {"type": "string"},
                },
            },
        },
        "skills": {
            "type": "object",
            "additionalProperties": False,
            "required": ["programming", "frameworks", "tools"],
            "properties": {
                "programming": {"type": "array", "items": {"type": "string"}},
                "frameworks": {"type": "array", "items": {"type": "string"}},
                "tools": {"type": "array", "items": {"type": "string"}},
            },
        },
        "projects": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["name", "desc"],
                "properties": {
                    "name": {"type": "string"},
                    "desc": {"type": "string"},
                },
            },
        },
        "certifications": {"type": "array", "items": {"type": "string"}},
        "languages": {"type": "array", "items": {"type": "string"}},
        "interests": {"type": "array", "items": {"type": "string"}},
        "strengths": {"type": "array", "items": {"type": "string"}},
        "achievements": {"type": "array", "items": {"type": "string"}},
        "courses": {"type": "array", "items": {"type": "string"}},
    }

    # Add extra template-driven fields as strings
    for k in extra_text_fields:
        data_properties[k] = {"type": "string"}

    # ✅ OpenAI strict requirement: required must include ALL property keys
    data_required = list(data_properties.keys())

    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["title", "data"],
        "properties": {
            "title": {"type": "string"},
            "data": {
                "type": "object",
                "additionalProperties": False,
                "required": data_required,
                "properties": data_properties,
            },
        },
    }


def call_openai_resume(prompt: str, response_schema: Dict[str, Any]) -> dict:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY missing in .env / environment")

    url = "https://api.openai.com/v1/responses"
    headers = {"Authorization": f"Bearer {OPENAI_API_KEY}", "Content-Type": "application/json"}

    instructions = (
        "You are an expert resume writer.\n"
        "Create a professional resume from the user's prompt.\n"
        "Return ONLY JSON that matches the JSON Schema.\n"
        "Rules:\n"
        "- Use strong action verbs, quantified bullets, realistic dates.\n"
        "- Always include optional arrays keys even if empty: certifications,languages,interests,strengths,achievements,courses.\n"
        "- For any template-driven text fields, return meaningful text or empty string.\n"
    )

    body = {
        "model": OPENAI_MODEL,
        "instructions": instructions,
        "input": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "text": {
            "format": {
                "type": "json_schema",
                "name": "resume_data",   # ✅ required
                "strict": True,
                "schema": response_schema,
            }
        },
        "max_output_tokens": 2000,
    }

    r = requests.post(url, headers=headers, data=json.dumps(body), timeout=60)

    if r.status_code >= 400:
        raise RuntimeError(f"OpenAI error {r.status_code}: {r.text}")

    payload = r.json()

    out_text = ""
    for item in payload.get("output", []):
        if item.get("type") == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    out_text += c.get("text", "")

    if not out_text.strip():
        raise RuntimeError("No output_text from OpenAI response")

    return json.loads(out_text)
