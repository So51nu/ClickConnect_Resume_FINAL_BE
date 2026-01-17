"""users/marketplace_templates.py

✅ Marketplace template catalogue (31 templates) with DISTINCT designs.

Key rule (so your resume editor works across all templates):
- All templates use the SAME section IDs and data keys:
  header, summary, experience, education, skills, projects, certifications, languages, interests, strengths, achievements, courses, contacts, sidebarProfile

Only these differ per template:
- layout (Single Column / Two Column / Sidebar Left / Sidebar Right)
- columns arrangement / order
- theme (colors/fonts/heading style/header variant/sidebar styling/paper styling/background pattern)

Preview images:
- Put PNGs in Django static:
  static/marketplace/tpl-01.png ... static/marketplace/tpl-31.png
"""

from __future__ import annotations

from typing import Dict, List, Any


def _sections_base() -> Dict[str, Any]:
    # Keep everything consistent across templates.
    # Optional sections default disabled so empty data doesn't look weird.
    return {
        "header": {"enabled": True, "type": "header", "dataKey": "header"},
        "summary": {"enabled": True, "type": "text", "dataKey": "summary"},
        "experience": {"enabled": True, "type": "timeline", "dataKey": "experience"},
        "education": {"enabled": True, "type": "timeline", "dataKey": "education"},
        "skills": {"enabled": True, "type": "skills", "dataKey": "skills"},
        "projects": {"enabled": True, "type": "timeline", "dataKey": "projects"},
        "certifications": {"enabled": False, "type": "list", "dataKey": "certifications"},
        "languages": {"enabled": False, "type": "languages", "dataKey": "languages"},
        "interests": {"enabled": False, "type": "list", "dataKey": "interests"},
        "strengths": {"enabled": False, "type": "grid", "dataKey": "strengths"},
        "achievements": {"enabled": False, "type": "grid", "dataKey": "achievements"},
        "courses": {"enabled": False, "type": "list", "dataKey": "courses"},
        # Contacts reads header data
        "contacts": {"enabled": False, "type": "contacts", "dataKey": "header"},
        "sidebarProfile": {"enabled": False, "type": "avatar", "dataKey": "header"},
    }


def _schema_single(order: List[str], theme: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": 2,
        "layout": "Single Column",
        "theme": theme,
        "order": order,
        "columns": {"left": [], "right": []},
        "sections": _sections_base(),
    }


def _schema_two(left: List[str], right: List[str], theme: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "version": 2,
        "layout": "Two Column",
        "theme": theme,
        "order": [],
        "columns": {"left": left, "right": right},
        "sections": _sections_base(),
    }


def _schema_sidebar(side: str, sidebar: List[str], main: List[str], theme: Dict[str, Any]) -> Dict[str, Any]:
    assert side in ("Sidebar Left", "Sidebar Right")
    if side == "Sidebar Left":
        cols = {"left": sidebar, "right": main}
    else:
        cols = {"left": main, "right": sidebar}

    return {
        "version": 2,
        "layout": side,
        "theme": theme,
        "order": [],
        "columns": cols,
        "sections": _sections_base(),
    }


def _theme(
    primary: str,
    *,
    font: str,
    heading_variant: str,
    header_variant: str,
    paper_variant: str,
    pattern: str | None = None,
    sidebar_bg: str | None = None,
    sidebar_text: str | None = None,
    sidebar_accent: str | None = None,
    text_color: str = "#111827",
    muted_color: str = "#6b7280",
) -> Dict[str, Any]:
    return {
        "primary": primary,
        "textColor": text_color,
        "mutedColor": muted_color,
        "fontFamily": font,
        "headingUppercase": True,
        "titleSize": 12,
        "bodySize": 10,
        "lineHeight": 1.45,

        # Rendering variants used by frontend ResumePreview
        "headingVariant": heading_variant,  # underline | bar | pill | boxed | leftBorder | double
        "headerVariant": header_variant,    # classic | centered | split | banner | minimal
        "paperVariant": paper_variant,      # plain | card | soft | borderLeft | borderTop
        "pattern": pattern,                 # none | dots | lines | grid | diagonal

        # Sidebar options
        "sidebarBg": sidebar_bg,
        "sidebarText": sidebar_text,
        "sidebarAccent": sidebar_accent,

        # Small toggles
        "headerIcons": True,
        "showContactLabels": False,
    }


# 31 distinct designs.
# NOTE: names are safe + stable; you can change display names anytime.

_TPLS: List[Dict[str, Any]] = []

# A small palette bank
PALETTES = [
    ("#2563eb", "system-ui, -apple-system, Segoe UI, Roboto, sans-serif"),
    ("#0f766e", "system-ui, -apple-system, Segoe UI, Roboto, sans-serif"),
    ("#7c3aed", "system-ui, -apple-system, Segoe UI, Roboto, sans-serif"),
    ("#b91c1c", "Georgia, 'Times New Roman', Times, serif"),
    ("#1f2937", "Georgia, 'Times New Roman', Times, serif"),
    ("#0891b2", "'Trebuchet MS', Trebuchet, Arial, sans-serif"),
    ("#c2410c", "'Segoe UI', system-ui, sans-serif"),
    ("#334155", "'Inter', system-ui, -apple-system, Segoe UI, Roboto, sans-serif"),
    ("#15803d", "'Inter', system-ui, -apple-system, Segoe UI, Roboto, sans-serif"),
    ("#be185d", "'Poppins', system-ui, -apple-system, Segoe UI, Roboto, sans-serif"),
]

HEADING_VARIANTS = ["underline", "bar", "pill", "boxed", "leftBorder", "double"]
HEADER_VARIANTS = ["classic", "centered", "split", "banner", "minimal"]
PAPER_VARIANTS = ["plain", "card", "soft", "borderLeft", "borderTop"]
PATTERNS = [None, "dots", "lines", "grid", "diagonal"]


def _mk(i: int, name: str, layout: str, theme: Dict[str, Any], *, order=None, left=None, right=None, sidebar=None, main=None):
    key = f"tpl-{i:02d}"
    base = {
        "key": key,
        "name": name,
        "category": "Modern" if i % 3 else "Classic",
        "layout": layout,
        "color": theme.get("primary") or "#2563eb",
        "price_type": "free",
        "price": 0,
        # We store a static path; the view will convert it to an absolute URL
        "preview_static_path": f"marketplace/{key}.png",
    }

    if layout == "Single Column":
        base["schema"] = _schema_single(order or ["header", "summary", "experience", "education", "skills", "projects"], theme)
    elif layout == "Two Column":
        base["schema"] = _schema_two(left or ["summary", "skills", "education"], right or ["header", "experience", "projects"], theme)
    elif layout in ("Sidebar Left", "Sidebar Right"):
        base["schema"] = _schema_sidebar(layout, sidebar or ["header", "skills", "education"], main or ["summary", "experience", "projects"], theme)
    else:
        base["schema"] = _schema_single(["header", "summary", "experience", "education", "skills", "projects"], theme)

    _TPLS.append(base)


# Build 31 templates by mixing variants in a controlled way.
for idx in range(1, 32):
    primary, font = PALETTES[(idx - 1) % len(PALETTES)]
    heading_variant = HEADING_VARIANTS[(idx - 1) % len(HEADING_VARIANTS)]
    header_variant = HEADER_VARIANTS[(idx - 1) % len(HEADER_VARIANTS)]
    paper_variant = PAPER_VARIANTS[(idx - 1) % len(PAPER_VARIANTS)]
    pattern = PATTERNS[(idx - 1) % len(PATTERNS)]

    # layout distribution:
    if idx <= 10:
        layout = "Single Column"
    elif idx <= 20:
        layout = "Two Column"
    elif idx <= 26:
        layout = "Sidebar Left"
    else:
        layout = "Sidebar Right"

    # Sidebar styles
    sidebar_bg = None
    sidebar_text = None
    sidebar_accent = None
    if "Sidebar" in layout:
        sidebar_bg = "#0b1220" if idx % 2 == 0 else "#f1f5f9"
        sidebar_text = "#e5e7eb" if sidebar_bg == "#0b1220" else "#0f172a"
        sidebar_accent = primary

    theme = _theme(
        primary,
        font=font,
        heading_variant=heading_variant,
        header_variant=header_variant,
        paper_variant=paper_variant,
        pattern=pattern,
        sidebar_bg=sidebar_bg,
        sidebar_text=sidebar_text,
        sidebar_accent=sidebar_accent,
    )

    # Make each name a bit unique
    nice = [
        "Aurora",
        "Monochrome",
        "Cobalt",
        "Crimson",
        "Sage",
        "Atlas",
        "Slate",
        "Orchid",
        "Teal",
        "Sunset",
        "Nimbus",
        "Nova",
        "Prism",
        "Zen",
        "Obsidian",
        "Iris",
        "Pulse",
        "Vertex",
        "Muse",
        "Horizon",
        "Lumen",
        "Kinetic",
        "Sierra",
        "Cedar",
        "Lagoon",
        "Noir",
        "Amber",
        "Citrine",
        "Matrix",
        "Echo",
        "Summit",
    ]
    name = f"{nice[idx-1]} {idx:02d}"

    # Custom column/ordering per layout to increase variety
    if layout == "Single Column":
        orders = [
            ["header", "summary", "experience", "education", "skills", "projects"],
            ["header", "summary", "skills", "experience", "projects", "education"],
            ["header", "summary", "experience", "projects", "skills", "education"],
            ["header", "summary", "education", "experience", "projects", "skills"],
        ]
        order = orders[(idx - 1) % len(orders)]
        _mk(idx, name, layout, theme, order=order)

    elif layout == "Two Column":
        colsets = [
            (["summary", "skills", "education"], ["header", "experience", "projects"]),
            (["header", "summary", "skills"], ["experience", "projects", "education"]),
            (["summary", "education", "languages"], ["header", "experience", "skills", "projects"]),
            (["skills", "education", "interests"], ["header", "summary", "experience", "projects"]),
        ]
        left, right = colsets[(idx - 1) % len(colsets)]
        _mk(idx, name, layout, theme, left=left, right=right)

    elif layout == "Sidebar Left":
        side_sets = [
            (["header", "skills", "education", "languages"], ["summary", "experience", "projects"]),
            (["header", "contacts", "skills", "education"], ["summary", "experience", "projects"]),
            (["sidebarProfile", "header", "skills", "languages"], ["summary", "experience", "projects", "education"]),
        ]
        sidebar, main = side_sets[(idx - 1) % len(side_sets)]
        _mk(idx, name, layout, theme, sidebar=sidebar, main=main)

    else:  # Sidebar Right
        side_sets = [
            (["header", "skills", "education", "languages"], ["summary", "experience", "projects"]),
            (["header", "contacts", "skills", "education"], ["summary", "experience", "projects"]),
            (["sidebarProfile", "header", "skills", "languages"], ["summary", "experience", "projects", "education"]),
        ]
        sidebar, main = side_sets[(idx - 1) % len(side_sets)]
        _mk(idx, name, layout, theme, sidebar=sidebar, main=main)


MARKETPLACE_TEMPLATES: List[Dict[str, Any]] = _TPLS
