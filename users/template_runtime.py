# users/template_runtime.py
from copy import deepcopy

DEFAULT_HEADER = {
    "fullName": "",
    "jobTitle": "",
    "email": "",
    "phone": "",
    "location": "",
    "linkedin": "",
    "website": "",
    "photoUrl": "",
}

def normalize_template_schema(schema: dict) -> dict:
    """
    Backward compatible normalizer.
    Ensures:
      - schema.version/layout/theme/columns/sections exist
      - every section has: enabled, type, dataKey, label
    """
    if not isinstance(schema, dict):
        schema = {}

    s = deepcopy(schema)
    s.setdefault("version", 1)
    s.setdefault("layout", "Single Column")
    s.setdefault("theme", {})
    s.setdefault("columns", {"left": [], "right": []})
    s.setdefault("order", [])
    s.setdefault("sections", {})

    sections = s.get("sections") or {}
    if not isinstance(sections, dict):
        sections = {}

    def ensure_section(sec_id: str, default_type: str, default_key: str, default_label: str):
        cfg = sections.get(sec_id) or {}
        if not isinstance(cfg, dict):
            cfg = {}
        cfg.setdefault("enabled", True)
        cfg.setdefault("type", default_type)
        cfg.setdefault("dataKey", default_key)
        cfg.setdefault("label", default_label)
        sections[sec_id] = cfg

    # ✅ common defaults (old templates auto work)
    ensure_section("header", "header", "header", "")
    ensure_section("summary", "text", "summary", "SUMMARY")
    ensure_section("experience", "timeline", "experience", "EXPERIENCE")
    ensure_section("education", "timeline", "education", "EDUCATION")
    ensure_section("projects", "timeline", "projects", "PROJECTS")
    ensure_section("skills", "skills", "skills", "SKILLS")
    ensure_section("certifications", "list", "certifications", "CERTIFICATIONS")
    ensure_section("languages", "languages", "languages", "LANGUAGES")

    # Optional / extra ids you already use
    if "courses" in sections:
        ensure_section("courses", "list", "courses", sections["courses"].get("label") or "TRAINING / COURSES")
    if "training" in sections:
        ensure_section("training", "list", "training", sections["training"].get("label") or "TRAINING / COURSES")
    if "achievements" in sections:
        ensure_section("achievements", "grid", "achievements", sections["achievements"].get("label") or "KEY ACHIEVEMENTS")
    if "strengths" in sections:
        ensure_section("strengths", "grid", "strengths", sections["strengths"].get("label") or "STRENGTHS")
    if "interests" in sections:
        ensure_section("interests", "list", "interests", sections["interests"].get("label") or "INTERESTS")
    if "contacts" in sections:
        # contacts reads header block
        ensure_section("contacts", "contacts", "header", sections["contacts"].get("label") or "CONTACTS")
    if "sidebarProfile" in sections:
        ensure_section("sidebarProfile", "avatar", "header", "")

    # If any new section is added without type => fallback guess
    for sec_id, cfg in list(sections.items()):
        if not isinstance(cfg, dict):
            continue
        cfg.setdefault("enabled", True)
        cfg.setdefault("label", sec_id.upper())
        if "type" not in cfg:
            if sec_id in ("experience", "education", "projects"):
                cfg["type"] = "timeline"
                cfg.setdefault("dataKey", sec_id)
            elif sec_id in ("summary", "objective"):
                cfg["type"] = "text"
                cfg.setdefault("dataKey", sec_id)
            elif sec_id == "skills":
                cfg["type"] = "skills"
                cfg.setdefault("dataKey", sec_id)
            elif sec_id == "languages":
                cfg["type"] = "languages"
                cfg.setdefault("dataKey", sec_id)
            elif sec_id in ("contacts",):
                cfg["type"] = "contacts"
                cfg.setdefault("dataKey", "header")
            elif sec_id in ("sidebarProfile", "avatar"):
                cfg["type"] = "avatar"
                cfg.setdefault("dataKey", "header")
            else:
                cfg["type"] = "list"
                cfg.setdefault("dataKey", sec_id)
        cfg.setdefault("dataKey", sec_id)

    s["sections"] = sections

    # Ensure columns/order is consistent
    layout = (s.get("layout") or "Single Column").lower()
    cols = s.get("columns") or {"left": [], "right": []}
    if not isinstance(cols, dict):
        cols = {"left": [], "right": []}
    cols.setdefault("left", [])
    cols.setdefault("right", [])
    s["columns"] = cols

    if not s.get("order"):
        # If no order provided, build from enabled sections
        # Keep header first if exists
        order = []
        if "header" in sections and sections["header"].get("enabled", True):
            order.append("header")
        for k in sections.keys():
            if k != "header" and sections[k].get("enabled", True):
                order.append(k)
        s["order"] = order

    return s


def default_resume_data_from_schema(schema: dict) -> dict:
    """
    Generates default data skeleton based on schema sections.
    So create/edit always has matching keys.
    """
    s = normalize_template_schema(schema or {})
    sections = s.get("sections") or {}

    data = {
        "header": deepcopy(DEFAULT_HEADER),
    }

    def ensure_list(key, item):
        if key not in data:
            data[key] = [deepcopy(item)]

    def ensure_text(key):
        data.setdefault(key, "")

    for sec_id, cfg in sections.items():
        if not cfg.get("enabled", True):
            continue
        t = cfg.get("type")
        dk = cfg.get("dataKey") or sec_id

        if t == "header" or dk == "header":
            data.setdefault("header", deepcopy(DEFAULT_HEADER))
        elif t == "text":
            ensure_text(dk)
        elif t == "timeline":
            if dk == "experience":
                ensure_list("experience", {"title": "", "company": "", "location": "", "from": "", "to": "", "bullets": [""]})
            elif dk == "education":
                ensure_list("education", {"school": "", "degree": "", "location": "", "from": "", "to": ""})
            elif dk == "projects":
                ensure_list("projects", {"name": "", "desc": ""})
            else:
                ensure_list(dk, {"title": "", "subtitle": "", "from": "", "to": "", "bullets": [""]})
        elif t == "skills":
            data.setdefault("skills", {"programming": [], "frameworks": [], "tools": []})
        elif t == "languages":
            ensure_list("languages", {"name": "", "level": "Beginner"})
        elif t in ("list", "grid"):
            # generic list of objects (title + desc)
            ensure_list(dk, {"title": "", "desc": ""})
        elif t == "contacts":
            data.setdefault("header", deepcopy(DEFAULT_HEADER))
        elif t == "avatar":
            data.setdefault("header", deepcopy(DEFAULT_HEADER))
        else:
            ensure_list(dk, {"title": "", "desc": ""})

    return data
