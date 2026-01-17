# users/ai_templates.py
from __future__ import annotations

import random
import urllib.parse
from typing import Any, Dict, List, Optional, Tuple


# -------------------------
# Helpers
# -------------------------
HEADING_VARIANTS = ["underline", "bar", "pill", "boxed", "leftBorder", "double"]
HEADER_VARIANTS = ["classic", "centered", "split", "banner", "minimal"]
PAPER_VARIANTS = ["plain", "card", "soft", "borderLeft", "borderTop"]
PATTERNS = [None, "dots", "lines", "grid", "diagonal"]

FONTS = [
    "Inter, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
    "Poppins, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
    "Montserrat, system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
    "Georgia, 'Times New Roman', Times, serif",
    "'Trebuchet MS', Trebuchet, Arial, sans-serif",
    "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
]

PALETTES: List[Tuple[str, str, str]] = [
    ("#2563eb", "#111827", "#6b7280"),  # blue
    ("#0f766e", "#0f172a", "#475569"),  # teal
    ("#7c3aed", "#111827", "#6b7280"),  # purple
    ("#be185d", "#111827", "#6b7280"),  # pink
    ("#c2410c", "#3f2a1d", "#7c5a3a"),  # orange-brown
    ("#15803d", "#052e16", "#14532d"),  # green
    ("#0b4a6f", "#0b1220", "#334155"),  # navy
    ("#b91c1c", "#111827", "#6b7280"),  # red
    ("#111827", "#111827", "#6b7280"),  # mono
    ("#0891b2", "#0f172a", "#475569"),  # cyan
    ("#9333ea", "#111827", "#6b7280"),  # violet
    ("#f59e0b", "#1f2937", "#6b7280"),  # amber (accent)
]

LAYOUTS = [
    "Single Column",
    "Two Column",
    "Sidebar Left",
    "Sidebar Right",
]


def _sections_base(extra_text: Optional[List[str]] = None) -> Dict[str, Any]:
    extra_text = extra_text or []
    s: Dict[str, Any] = {
        "header": {"enabled": True, "type": "header", "dataKey": "header"},
        "contacts": {"enabled": True, "type": "contacts", "dataKey": "header", "label": "CONTACT"},
        "summary": {"enabled": True, "type": "text", "dataKey": "summary", "label": "SUMMARY"},
        "experience": {"enabled": True, "type": "timeline", "dataKey": "experience", "label": "EXPERIENCE"},
        "education": {"enabled": True, "type": "timeline", "dataKey": "education", "label": "EDUCATION"},
        "skills": {"enabled": True, "type": "skills", "dataKey": "skills", "label": "SKILLS"},
        "projects": {"enabled": True, "type": "timeline", "dataKey": "projects", "label": "PROJECTS"},
        "certifications": {"enabled": True, "type": "list", "dataKey": "certifications", "label": "CERTIFICATIONS"},
        "languages": {"enabled": True, "type": "languages", "dataKey": "languages", "label": "LANGUAGES"},
        "achievements": {"enabled": True, "type": "list", "dataKey": "achievements", "label": "ACHIEVEMENTS"},
        "interests": {"enabled": False, "type": "list", "dataKey": "interests", "label": "INTERESTS"},
        "strengths": {"enabled": False, "type": "grid", "dataKey": "strengths", "label": "STRENGTHS"},
        "courses": {"enabled": False, "type": "list", "dataKey": "courses", "label": "COURSES"},
        "sidebarProfile": {"enabled": False, "type": "avatar", "dataKey": "header"},
    }
    for k in extra_text:
        s[k] = {"enabled": True, "type": "text", "dataKey": k, "label": k.upper()}
    return s


def _theme(
    primary: str,
    font: str,
    *,
    heading_variant: str,
    header_variant: str,
    paper_variant: str,
    pattern: Optional[str],
    text_color: str,
    muted_color: str,
    sidebar_bg: Optional[str] = None,
    sidebar_text: Optional[str] = None,
    sidebar_accent: Optional[str] = None,
    title_size: int = 12,
    body_size: int = 10,
    line_height: float = 1.45,
    card_radius: int = 14,
    card_padding: int = 32,
) -> Dict[str, Any]:
    return {
        "primary": primary,
        "fontFamily": font,
        "headingUppercase": True,
        "titleSize": title_size,
        "bodySize": body_size,
        "lineHeight": line_height,
        "headingVariant": heading_variant,
        "headerVariant": header_variant,
        "paperVariant": paper_variant,
        "pattern": pattern,
        "textColor": text_color,
        "mutedColor": muted_color,
        "sidebarBg": sidebar_bg,
        "sidebarText": sidebar_text,
        "sidebarAccent": sidebar_accent,
        "cardRadius": card_radius,
        "cardPadding": card_padding,
        "headerIcons": True,
        "showContactLabels": False,
    }


def _svg_preview(theme: Dict[str, Any], layout: str) -> str:
    p = theme.get("primary", "#2563eb")
    stroke = "#e5e7eb"
    bg = "#ffffff"
    pill = "12"
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="170" height="120">
      <rect x="1" y="1" width="168" height="118" rx="12" fill="{bg}" stroke="{stroke}" />
      <rect x="12" y="10" width="88" height="10" rx="{pill}" fill="{p}"/>
      <rect x="12" y="26" width="145" height="6" rx="3" fill="#d1d5db"/>
      <rect x="12" y="38" width="120" height="6" rx="3" fill="#e5e7eb"/>
    """
    if layout == "Two Column":
        svg += f"""
        <rect x="12" y="52" width="72" height="56" rx="10" fill="#f8fafc" stroke="{stroke}" />
        <rect x="90" y="52" width="67" height="56" rx="10" fill="#ffffff" stroke="{stroke}" />
        <rect x="20" y="60" width="56" height="6" rx="3" fill="{p}" opacity="0.35" />
        <rect x="98" y="60" width="50" height="6" rx="3" fill="{p}" opacity="0.20" />
        """
    elif layout in ("Sidebar Left", "Sidebar Right"):
        if layout == "Sidebar Left":
            svg += f"""
            <rect x="12" y="52" width="50" height="56" rx="10" fill="{p}" opacity="0.14" stroke="{stroke}" />
            <rect x="66" y="52" width="91" height="56" rx="10" fill="#ffffff" stroke="{stroke}" />
            """
        else:
            svg += f"""
            <rect x="12" y="52" width="91" height="56" rx="10" fill="#ffffff" stroke="{stroke}" />
            <rect x="107" y="52" width="50" height="56" rx="10" fill="{p}" opacity="0.14" stroke="{stroke}" />
            """
        svg += f"""
        <rect x="20" y="60" width="36" height="6" rx="3" fill="{p}" opacity="0.25" />
        <rect x="74" y="60" width="70" height="6" rx="3" fill="{p}" opacity="0.18" />
        """
    else:
        svg += f"""
        <rect x="12" y="52" width="145" height="56" rx="10" fill="#ffffff" stroke="{stroke}" />
        <rect x="20" y="60" width="110" height="6" rx="3" fill="{p}" opacity="0.18" />
        <rect x="20" y="72" width="92" height="6" rx="3" fill="#e5e7eb" />
        <rect x="20" y="84" width="120" height="6" rx="3" fill="#e5e7eb" />
        """
    svg += "</svg>"
    return "data:image/svg+xml;utf8," + urllib.parse.quote(svg.strip())


def _schema_single(order: List[str], theme: Dict[str, Any], sections: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": 2,
        "layout": "Single Column",
        "theme": theme,
        "order": order,
        "columns": {"left": [], "right": []},
        "sections": sections,
    }


def _schema_two(left: List[str], right: List[str], theme: Dict[str, Any], sections: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": 2,
        "layout": "Two Column",
        "theme": theme,
        "order": [],
        "columns": {"left": left, "right": right},
        "sections": sections,
    }


def _schema_sidebar(layout: str, left: List[str], right: List[str], theme: Dict[str, Any], sections: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": 2,
        "layout": layout,
        "theme": theme,
        "order": [],
        "columns": {"left": left, "right": right},
        "sections": sections,
    }


def _make_template(i: int, name: str, layout: str, theme: Dict[str, Any], sections: Dict[str, Any]) -> Dict[str, Any]:
    key = f"ai-{i:02d}"

    if layout == "Single Column":
        orders = [
            ["header", "contacts", "summary", "experience", "education", "skills", "projects", "achievements", "certifications", "languages"],
            ["header", "contacts", "summary", "skills", "experience", "projects", "education", "achievements", "certifications", "languages"],
            ["header", "contacts", "summary", "experience", "projects", "skills", "education", "achievements", "certifications", "languages"],
        ]
        schema = _schema_single(orders[(i - 1) % len(orders)], theme, sections)

    elif layout == "Two Column":
        left_sets = [
            ["summary", "skills", "education", "certifications", "languages"],
            ["summary", "education", "skills", "languages", "certifications"],
            ["skills", "certifications", "languages", "education"],
        ]
        right_sets = [
            ["header", "contacts", "experience", "projects", "achievements"],
            ["header", "contacts", "experience", "achievements", "projects"],
            ["header", "contacts", "projects", "experience", "achievements"],
        ]
        schema = _schema_two(left_sets[(i - 1) % len(left_sets)], right_sets[(i - 1) % len(right_sets)], theme, sections)

    elif layout in ("Sidebar Left", "Sidebar Right"):
        # enable photo on some sidebar templates
        if i % 3 == 0:
            sections = dict(sections)
            sections["sidebarProfile"] = dict(sections.get("sidebarProfile", {}))
            sections["sidebarProfile"]["enabled"] = True

        sidebar = ["sidebarProfile", "header", "contacts", "skills", "languages", "certifications"]
        main = ["summary", "experience", "projects", "education", "achievements"]
        if layout == "Sidebar Left":
            schema = _schema_sidebar(layout, sidebar, main, theme, sections)
        else:
            schema = _schema_sidebar(layout, main, sidebar, theme, sections)

    else:
        schema = _schema_single(["header", "contacts", "summary", "experience", "education", "skills", "projects"], theme, sections)

    return {
        "key": key,
        "name": name,
        "layout": layout,
        "color": theme.get("primary"),
        "schema": schema,
        "preview_svg": _svg_preview(theme, layout),
    }


# -------------------------
# 42 templates
# -------------------------
AI_TEMPLATE_BANK: List[Dict[str, Any]] = []

NAMES = [
    "Canva-Clean", "Canva-Modern", "Canva-Bold", "Canva-Creative", "Canva-Minimal",
    "Neo-Tech", "Neo-Slate", "Neo-Ocean", "Neo-Orchid", "Neo-Citrus",
    "Atlas", "Horizon", "Prism", "Vertex", "Lumen",
    "Noir", "Obsidian", "Cobalt", "Sienna", "Lagoon",
    "Mint", "Crimson", "Iris", "Amber", "Matrix",
    "Pulse", "Kinetic", "Summit", "Cedar", "Nimbus",
    "Aurora", "Zen", "Muse", "Citrine", "Echo",
    "Sierra", "Monochrome", "Granite", "Rosewood", "Blueprint",
    "Executive", "Corporate",
]

for idx in range(1, 43):
    primary, text_color, muted = PALETTES[(idx - 1) % len(PALETTES)]
    font = FONTS[(idx - 1) % len(FONTS)]
    layout = LAYOUTS[(idx - 1) % len(LAYOUTS)]
    heading_variant = HEADING_VARIANTS[(idx - 1) % len(HEADING_VARIANTS)]
    header_variant = HEADER_VARIANTS[(idx - 1) % len(HEADER_VARIANTS)]
    paper_variant = PAPER_VARIANTS[(idx - 1) % len(PAPER_VARIANTS)]
    pattern = PATTERNS[(idx - 1) % len(PATTERNS)]

    # Make some templates more "Canva-like"
    if idx % 7 == 0:
        header_variant = "banner"
        paper_variant = "soft"
        pattern = "diagonal"
    if idx % 9 == 0:
        heading_variant = "pill"
    if idx % 11 == 0:
        heading_variant = "boxed"
        paper_variant = "borderTop"
    if idx % 13 == 0:
        paper_variant = "borderLeft"
        header_variant = "centered"

    sidebar_bg = None
    sidebar_text = None
    sidebar_accent = None
    if "Sidebar" in layout:
        if idx % 2 == 0:
            sidebar_bg = "#0b1220"
            sidebar_text = "#e5e7eb"
        else:
            sidebar_bg = "#f1f5f9"
            sidebar_text = "#0f172a"
        sidebar_accent = primary

    theme = _theme(
        primary,
        font,
        heading_variant=heading_variant,
        header_variant=header_variant,
        paper_variant=paper_variant,
        pattern=pattern,
        text_color=text_color,
        muted_color=muted,
        sidebar_bg=sidebar_bg,
        sidebar_text=sidebar_text,
        sidebar_accent=sidebar_accent,
        title_size=12 if idx % 5 else 13,
        body_size=10,
        line_height=1.45 if idx % 4 else 1.5,
        card_radius=14 if paper_variant in ("card", "soft") else 10,
        card_padding=32,
    )

    # Add a few "domain" extra text sections for variety
    extra = []
    if idx % 10 == 0:
        extra = ["communication", "leadership"]
    if idx % 14 == 0:
        extra = ["references"]
    sections = _sections_base(extra_text=extra)

    name = f"{NAMES[idx-1]} {idx:02d}"
    AI_TEMPLATE_BANK.append(_make_template(idx, name, layout, theme, sections))


def get_suggestions(n: int = 5) -> List[Dict[str, Any]]:
    bank = list(AI_TEMPLATE_BANK)
    random.shuffle(bank)
    return bank[:max(1, min(n, len(bank)))]


def pick_random_template() -> Dict[str, Any]:
    return random.choice(AI_TEMPLATE_BANK)


def get_template_by_key(key: str) -> Optional[Dict[str, Any]]:
    for t in AI_TEMPLATE_BANK:
        if t.get("key") == key:
            return t
    return None
