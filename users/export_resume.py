# users/export_resume.py
import io
from typing import Any, Dict, List, Tuple

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib import colors

from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn


# -----------------------
# Safe helpers
# -----------------------
def _as_list(x: Any) -> List[Any]:
    return x if isinstance(x, list) else []

def _as_dict(x: Any) -> Dict[str, Any]:
    return x if isinstance(x, dict) else {}

def _as_str(x: Any) -> str:
    if isinstance(x, str):
        return x
    if x is None:
        return ""
    return str(x)

def _safe_font_name(font_family: Any) -> str:
    ff = _as_str(font_family) or "Calibri"
    first = ff.split(",")[0].strip().replace("'", "").replace('"', "")
    return first or "Calibri"

def _join_list(x: Any) -> str:
    return ", ".join([_as_str(i) for i in _as_list(x) if _as_str(i)])

def _hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    c = (hex_color or "").strip()
    if c.startswith("#"):
        c = c[1:]
    if len(c) == 3:
        c = "".join([x * 2 for x in c])
    if len(c) != 6:
        return (37, 99, 235)
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))

def _theme(schema: Dict[str, Any]) -> Dict[str, Any]:
    s = schema or {}
    t = _as_dict(s.get("theme"))
    return {
        "primary": t.get("primary", "#2563eb"),
        "fontFamily": t.get("fontFamily", "Calibri"),
        "titleSize": t.get("titleSize", 12),
        "bodySize": t.get("bodySize", 10),
        "layout": s.get("layout", "Single Column"),
        "columns": _as_dict(s.get("columns")) or {"left": [], "right": []},
        "order": _as_list(s.get("order")),
        "sections": _as_dict(s.get("sections")),
    }

def _enabled(sections: Dict[str, Any], sec_id: str) -> bool:
    cfg = _as_dict((sections or {}).get(sec_id))
    v = cfg.get("enabled", True)
    return v is not False

def _label(sections: Dict[str, Any], sec_id: str) -> str:
    cfg = _as_dict((sections or {}).get(sec_id))
    return _as_str(cfg.get("label")) or sec_id.upper()

def _data_key(sections: Dict[str, Any], sec_id: str) -> str:
    cfg = _as_dict((sections or {}).get(sec_id))
    return _as_str(cfg.get("dataKey")) or sec_id


# -----------------------
# DOCX (Editable Word)
# -----------------------
def build_docx_bytes(resume_data: Dict[str, Any], schema: Dict[str, Any]) -> bytes:
    """
    Editable DOCX export that preserves layout reliably:
    - fixed margins
    - fixed table widths, autofit disabled
    - fixed column widths for Two Column / Sidebar
    - strong sidebar shading using w:shd XML
    - heading bottom border (stable)
    """
    from docx.shared import Pt, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.shared import Cm

    t = _theme(schema)
    theme = _as_dict((schema or {}).get("theme"))
    layout = _as_str(t.get("layout")) or "Single Column"
    cols = _as_dict(t.get("columns"))
    order = _as_list(t.get("order"))
    sections_cfg = _as_dict(t.get("sections"))

    primary_hex = _as_str(theme.get("primary") or t.get("primary") or "#2563eb")
    sidebar_bg_hex = _as_str(theme.get("sidebarBg") or "#0b1220")
    sidebar_text_hex = _as_str(theme.get("sidebarText") or theme.get("sidebarTextColor") or "#e5e7eb")
    sidebar_accent_hex = _as_str(theme.get("sidebarAccent") or primary_hex)

    doc = Document()

    # ✅ Fixed page margins
    sec = doc.sections[0]
    sec.top_margin = Cm(1.3)
    sec.bottom_margin = Cm(1.3)
    sec.left_margin = Cm(1.3)
    sec.right_margin = Cm(1.3)

    # ✅ Default font
    safe_font = _safe_font_name(t.get("fontFamily"))
    normal = doc.styles["Normal"]
    normal.font.name = safe_font
    try:
        normal._element.rPr.rFonts.set(qn("w:eastAsia"), safe_font)  # type: ignore[attr-defined]
    except Exception:
        pass
    normal.font.size = Pt(int((t.get("bodySize") or 10) + 1))

    def rgb(hexv: str) -> RGBColor:
        r, g, b = _hex_to_rgb(hexv)
        return RGBColor(r, g, b)

    PRIMARY = rgb(primary_hex)
    SIDEBAR_TEXT = rgb(sidebar_text_hex)
    SIDEBAR_ACCENT = rgb(sidebar_accent_hex)

    def set_cell_shading(cell, hex_color: str):
        """Reliable cell shading using w:shd"""
        fill = hex_color.strip().lstrip("#")
        tcPr = cell._tc.get_or_add_tcPr()
        shd = tcPr.find(qn("w:shd"))
        if shd is None:
            shd = OxmlElement("w:shd")
            tcPr.append(shd)
        shd.set(qn("w:val"), "clear")
        shd.set(qn("w:color"), "auto")
        shd.set(qn("w:fill"), fill)

    def set_cell_width(cell, inches: float):
        cell.width = Inches(inches)

    def disable_table_autofit(table):
        table.autofit = False
        try:
            tblPr = table._tbl.tblPr
            tblW = tblPr.tblW
            tblW.type = "dxa"
        except Exception:
            pass

    def heading(container, text: str, *, in_sidebar: bool):
        p = container.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(_as_str(text).upper())
        run.bold = True
        run.font.size = Pt(11)
        run.font.color.rgb = SIDEBAR_ACCENT if in_sidebar else PRIMARY

        # ✅ Stable bottom border line
        pPr = p._p.get_or_add_pPr()
        pBdr = pPr.find(qn("w:pBdr"))
        if pBdr is None:
            pBdr = OxmlElement("w:pBdr")
            pPr.append(pBdr)
        bottom = OxmlElement("w:bottom")
        bottom.set(qn("w:val"), "single")
        bottom.set(qn("w:sz"), "6")
        bottom.set(qn("w:space"), "1")
        bottom.set(qn("w:color"), (sidebar_accent_hex if in_sidebar else primary_hex).lstrip("#"))
        pBdr.append(bottom)

        return p

    def text(container, txt: Any, *, in_sidebar: bool = False, bold: bool = False, italic: bool = False):
        p = container.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        run = p.add_run(_as_str(txt))
        run.bold = bold
        run.italic = italic
        if in_sidebar:
            run.font.color.rgb = SIDEBAR_TEXT
        return p

    def bullets(container, arr: Any, *, in_sidebar: bool = False):
        for b in _as_list(arr):
            s = _as_str(b)
            if not s:
                continue
            p = container.add_paragraph(s, style="List Bullet")
            if in_sidebar:
                for r in p.runs:
                    r.font.color.rgb = SIDEBAR_TEXT
            p.paragraph_format.space_after = Pt(0)

    def render_section(container, sec_id: str, *, in_sidebar: bool):
        if not _enabled(sections_cfg, sec_id):
            return

        cfg = _as_dict(sections_cfg.get(sec_id))
        typ = _as_str(cfg.get("type"))
        dk = _data_key(sections_cfg, sec_id)
        lab = _label(sections_cfg, sec_id)
        val = resume_data.get(dk)

        if sec_id == "sidebarProfile":
            heading(container, "PROFILE", in_sidebar=True)
            text(container, "PHOTO", in_sidebar=True, bold=True)
            return

        if sec_id == "header":
            h = _as_dict(resume_data.get("header"))
            p = container.add_paragraph()
            p.paragraph_format.space_after = Pt(2)
            r = p.add_run(_as_str(h.get("fullName")))
            r.bold = True
            r.font.size = Pt(20)
            r.font.color.rgb = SIDEBAR_ACCENT if in_sidebar else PRIMARY

            p2 = container.add_paragraph()
            p2.paragraph_format.space_after = Pt(8)
            r2 = p2.add_run(_as_str(h.get("jobTitle")))
            r2.bold = True
            r2.font.size = Pt(11)
            if in_sidebar:
                r2.font.color.rgb = SIDEBAR_TEXT
            return

        if sec_id == "contacts":
            h = _as_dict(resume_data.get("header"))
            heading(container, lab, in_sidebar=in_sidebar)
            for line in [
                f"Email: {_as_str(h.get('email'))}",
                f"Phone: {_as_str(h.get('phone'))}",
                f"Location: {_as_str(h.get('location'))}",
                f"LinkedIn: {_as_str(h.get('linkedin'))}",
                f"Website: {_as_str(h.get('website'))}",
            ]:
                if ":" in line and line.split(":", 1)[1].strip():
                    text(container, line, in_sidebar=in_sidebar)
            return

        # normal section
        heading(container, lab, in_sidebar=in_sidebar)

        if typ == "text":
            text(container, val, in_sidebar=in_sidebar)
            return

        if typ in ("list", "languages"):
            bullets(container, val, in_sidebar=in_sidebar)
            return

        if typ == "skills":
            s = _as_dict(val)
            text(container, "Programming: " + _join_list(s.get("programming")), in_sidebar=in_sidebar)
            text(container, "Frameworks: " + _join_list(s.get("frameworks")), in_sidebar=in_sidebar)
            text(container, "Tools: " + _join_list(s.get("tools")), in_sidebar=in_sidebar)
            return

        if typ == "timeline":
            items = _as_list(val)
            for x in items:
                d = _as_dict(x)
                title = _as_str(d.get("title") or d.get("school") or d.get("name"))
                sub = _as_str(d.get("company") or d.get("degree") or d.get("location"))
                date = ""
                if d.get("from") or d.get("to"):
                    date = f"{_as_str(d.get('from'))} - {_as_str(d.get('to'))}".strip(" -")

                text(container, title, in_sidebar=in_sidebar, bold=True)
                if sub:
                    text(container, sub, in_sidebar=in_sidebar)
                if date:
                    text(container, date, in_sidebar=in_sidebar, italic=True)
                bullets(container, d.get("bullets"), in_sidebar=in_sidebar)
                if d.get("desc"):
                    text(container, d.get("desc"), in_sidebar=in_sidebar)
                container.add_paragraph("")  # spacer
            return

        # fallback
        text(container, val, in_sidebar=in_sidebar)

    # ---------------- Layout render ----------------
    if layout == "Two Column":
        # fixed widths (A4 usable ~ 6.7 in with margins; split 40/60)
        table = doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        disable_table_autofit(table)

        left = table.rows[0].cells[0]
        right = table.rows[0].cells[1]
        set_cell_width(left, 2.7)
        set_cell_width(right, 4.0)

        left_ids = _as_list(cols.get("left")) or ["summary", "skills", "education", "certifications", "languages"]
        right_ids = _as_list(cols.get("right")) or ["header", "contacts", "experience", "projects", "achievements"]

        for sid in left_ids:
            render_section(left, _as_str(sid), in_sidebar=False)
        for sid in right_ids:
            render_section(right, _as_str(sid), in_sidebar=False)

    elif layout in ("Sidebar Left", "Sidebar Right"):
        table = doc.add_table(rows=1, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        disable_table_autofit(table)

        c0 = table.rows[0].cells[0]
        c1 = table.rows[0].cells[1]

        # fixed widths 35/65
        set_cell_width(c0, 2.4)
        set_cell_width(c1, 4.3)

        if layout == "Sidebar Left":
            sidebar = c0
            main = c1
            sidebar_ids = _as_list(cols.get("left")) or ["sidebarProfile", "header", "contacts", "skills", "languages", "certifications"]
            main_ids = _as_list(cols.get("right")) or ["summary", "experience", "projects", "education", "achievements"]
        else:
            main = c0
            sidebar = c1
            main_ids = _as_list(cols.get("left")) or ["summary", "experience", "projects", "education", "achievements"]
            sidebar_ids = _as_list(cols.get("right")) or ["sidebarProfile", "header", "contacts", "skills", "languages", "certifications"]

        # shading always
        set_cell_shading(sidebar, sidebar_bg_hex or "#0b1220")

        for sid in sidebar_ids:
            render_section(sidebar, _as_str(sid), in_sidebar=True)
        for sid in main_ids:
            render_section(main, _as_str(sid), in_sidebar=False)

    else:
        ids = order or ["header", "contacts", "summary", "experience", "education", "skills", "projects", "achievements", "certifications", "languages"]
        for sid in ids:
            render_section(doc, _as_str(sid), in_sidebar=False)

    f = io.BytesIO()
    doc.save(f)
    return f.getvalue()

# -----------------------
# PDF (Selectable text)
# -----------------------
def build_pdf_bytes(resume_data: Dict[str, Any], schema: Dict[str, Any]) -> bytes:
    t = _theme(schema)
    primary_hex = _as_str(t["primary"]) or "#2563eb"
    pr = colors.Color(*[x / 255 for x in _hex_to_rgb(primary_hex)])

    layout = _as_str(t.get("layout")) or "Single Column"
    cols = _as_dict(t.get("columns"))
    order = _as_list(t.get("order"))
    sections_cfg = _as_dict(t.get("sections"))

    theme = _as_dict((schema or {}).get("theme"))
    pattern = theme.get("pattern")
    paper_variant = theme.get("paperVariant") or "plain"
    sidebar_bg = theme.get("sidebarBg")
    sidebar_text = theme.get("sidebarText") or theme.get("sidebarTextColor") or "#ffffff"
    sidebar_accent = theme.get("sidebarAccent") or primary_hex

    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    W, H = A4
    margin = 14 * mm  # tighter like template
    x0, y0 = margin, H - margin
    usable_w = W - 2 * margin

    body_font = "Helvetica"
    bold_font = "Helvetica-Bold"

    font_size = 9.5
    line_height = 12

    def draw_grid_bg():
        if pattern != "grid":
            return
        c.setStrokeColor(colors.Color(0, 0, 0, alpha=0.06))
        step = 12
        y = 0
        while y < H:
            c.line(0, y, W, y)
            y += step
        x = 0
        while x < W:
            c.line(x, 0, x, H)
            x += step

    def draw_paper_variant():
        if paper_variant == "borderTop":
            c.setFillColor(pr)
            c.rect(0, H - 10, W, 10, fill=1, stroke=0)
        elif paper_variant == "borderLeft":
            c.setFillColor(pr)
            c.rect(0, 0, 10, H, fill=1, stroke=0)

    def ensure_page(y: float) -> float:
        if y < margin + 40:
            c.showPage()
            draw_grid_bg()
            draw_paper_variant()
            return H - margin
        return y

    def wrap_text(txt: str, max_w: float) -> List[str]:
        words = (txt or "").split()
        lines = []
        line = ""
        for w in words:
            test = (line + " " + w).strip()
            if c.stringWidth(test, body_font, font_size) > max_w:
                if line:
                    lines.append(line)
                line = w
            else:
                line = test
        if line:
            lines.append(line)
        return lines

    def draw_heading(title: str, x: float, y: float, max_w: float) -> float:
        c.setFont(bold_font, 10.5)
        c.setFillColor(pr)
        c.drawString(x, y, title.upper())
        y -= 10

        # underline like template
        c.setStrokeColor(pr)
        c.setLineWidth(1)
        c.line(x, y, x + max_w, y)
        y -= 10
        return y

    def draw_paragraph(txt: Any, x: float, y: float, max_w: float, color=colors.black) -> float:
        c.setFont(body_font, font_size)
        c.setFillColor(color)
        for line in wrap_text(_as_str(txt), max_w):
            y = ensure_page(y)
            c.drawString(x, y, line)
            y -= line_height
        return y

    def draw_bullets(items: Any, x: float, y: float, max_w: float) -> float:
        arr = _as_list(items)
        c.setFont(body_font, font_size)
        c.setFillColor(colors.black)
        for it in arr:
            s = _as_str(it)
            if not s:
                continue
            lines = wrap_text(s, max_w - 10)
            for j, line in enumerate(lines):
                y = ensure_page(y)
                prefix = "• " if j == 0 else "  "
                c.drawString(x, y, prefix + line)
                y -= line_height
        return y

    def section_value(sec_id: str):
        cfg = _as_dict(sections_cfg.get(sec_id))
        dk = _data_key(sections_cfg, sec_id)
        return cfg, dk, resume_data.get(dk)

    def render_header(x: float, y: float, max_w: float) -> float:
        h = _as_dict(resume_data.get("header"))
        c.setFont(bold_font, 18)
        c.setFillColor(pr)
        c.drawString(x, y, _as_str(h.get("fullName")))
        y -= 22

        c.setFont(bold_font, 11)
        c.setFillColor(colors.black)
        c.drawString(x, y, _as_str(h.get("jobTitle")))
        y -= 18
        return y

    def render_contacts(x: float, y: float, max_w: float, in_sidebar=False) -> float:
        h = _as_dict(resume_data.get("header"))
        items = [
            ("Email", h.get("email")),
            ("Phone", h.get("phone")),
            ("Location", h.get("location")),
            ("LinkedIn", h.get("linkedin")),
            ("Website", h.get("website")),
        ]
        col = colors.white if in_sidebar else colors.black
        y = draw_heading(_label(sections_cfg, "contacts"), x, y, max_w)
        for k, v in items:
            if not _as_str(v):
                continue
            y = ensure_page(y)
            c.setFont(bold_font, font_size)
            c.setFillColor(col)
            c.drawString(x, y, f"{k}:")
            c.setFont(body_font, font_size)
            c.drawString(x + 42, y, _as_str(v))
            y -= line_height
        y -= 6
        return y

    def render_section(sec_id: str, x: float, y: float, max_w: float, in_sidebar=False) -> float:
        if not _enabled(sections_cfg, sec_id):
            return y

        if sec_id == "header":
            return render_header(x, y, max_w)

        if sec_id == "contacts":
            return render_contacts(x, y, max_w, in_sidebar=in_sidebar)

        cfg, dk, val = section_value(sec_id)
        typ = _as_str(cfg.get("type"))
        title = _label(sections_cfg, sec_id)

        # heading
        if in_sidebar:
            # sidebar heading in accent
            c.setFont(bold_font, 10.5)
            c.setFillColor(colors.Color(*[x/255 for x in _hex_to_rgb(sidebar_accent)]))
            c.drawString(x, y, title.upper())
            y -= 10
            c.setStrokeColor(colors.Color(*[x/255 for x in _hex_to_rgb(sidebar_accent)]))
            c.line(x, y, x + max_w, y)
            y -= 10
        else:
            y = draw_heading(title, x, y, max_w)

        text_col = colors.white if in_sidebar else colors.black

        if typ == "text":
            y = draw_paragraph(val if isinstance(val, str) else "", x, y, max_w, color=text_col)
            y -= 6
            return y

        if typ in ("list", "languages"):
            y = draw_bullets(val, x, y, max_w)
            y -= 6
            return y

        if typ == "skills":
            s = _as_dict(val)
            y = draw_paragraph("Programming: " + _join_list(s.get("programming")), x, y, max_w, color=text_col)
            y = draw_paragraph("Frameworks: " + _join_list(s.get("frameworks")), x, y, max_w, color=text_col)
            y = draw_paragraph("Tools: " + _join_list(s.get("tools")), x, y, max_w, color=text_col)
            y -= 6
            return y

        if typ == "timeline":
            arr = _as_list(val)
            for xitem in arr:
                d = _as_dict(xitem)
                y = ensure_page(y)
                title_line = _as_str(d.get("title") or d.get("school") or d.get("name"))
                sub = _as_str(d.get("company") or d.get("degree") or d.get("location"))
                date = ""
                if d.get("from") or d.get("to"):
                    date = f"{_as_str(d.get('from'))} - {_as_str(d.get('to'))}".strip(" -")

                c.setFont(bold_font, font_size)
                c.setFillColor(text_col)
                c.drawString(x, y, title_line)
                y -= line_height

                if sub:
                    y = draw_paragraph(sub, x, y, max_w, color=text_col)
                if date:
                    c.setFont("Helvetica-Oblique", 8.5)
                    c.setFillColor(text_col)
                    c.drawString(x, y, date)
                    y -= 11

                y = draw_bullets(d.get("bullets"), x, y, max_w)
                if d.get("desc"):
                    y = draw_paragraph(d.get("desc"), x, y, max_w, color=text_col)
                y -= 8
            return y

        # fallback
        y = draw_paragraph(val, x, y, max_w, color=text_col)
        y -= 6
        return y

    # ---- Page init
    draw_grid_bg()
    draw_paper_variant()

    if layout == "Sidebar Right" or layout == "Sidebar Left":
        side_w = usable_w * 0.35
        main_w = usable_w * 0.65
        gap = 10

        if layout == "Sidebar Left":
            side_x = x0
            main_x = x0 + side_w + gap
        else:
            main_x = x0
            side_x = x0 + main_w + gap

        # draw sidebar background
        sb = colors.Color(*[x/255 for x in _hex_to_rgb(_as_str(sidebar_bg or "#0b1220"))])
        c.setFillColor(sb)
        c.setStrokeColor(colors.transparent)
        c.roundRect(side_x - 4, margin - 4, side_w + 8, H - 2*margin + 8, 16, fill=1, stroke=0)

        # text colors for sidebar
        c.setFillColor(colors.white)

        # Render columns
        left_ids = _as_list(cols.get("left"))
        right_ids = _as_list(cols.get("right"))

        sidebar_ids = left_ids if layout == "Sidebar Left" else right_ids
        main_ids = right_ids if layout == "Sidebar Left" else left_ids

        y_main = y0
        for sid in (main_ids or ["header","summary","experience","projects","education","achievements"]):
            y_main = render_section(_as_str(sid), main_x, y_main, main_w - 6, in_sidebar=False)
            y_main = ensure_page(y_main)

        y_side = y0
        # sidebar: prefer profile + header + contacts + skills...
        for sid in (sidebar_ids or ["sidebarProfile","header","contacts","skills","languages","certifications"]):
            if sid == "sidebarProfile":
                # sidebarProfile is photo placeholder in PDF (circle)
                # (real photo not embedded in PDF currently)
                y_side = ensure_page(y_side)
                c.setFillColor(colors.white)
                c.circle(side_x + (side_w/2), y_side - 45, 35, fill=0, stroke=1)
                c.setFont(bold_font, 10)
                c.setFillColor(colors.white)
                c.drawCentredString(side_x + (side_w/2), y_side - 45, "PHOTO")
                y_side -= 95
                continue

            y_side = render_section(_as_str(sid), side_x + 8, y_side, side_w - 16, in_sidebar=True)
            y_side = ensure_page(y_side)

    elif layout == "Two Column":
        left_w = usable_w * 0.40
        right_w = usable_w * 0.60
        gap = 10
        left_x = x0
        right_x = x0 + left_w + gap

        left_ids = _as_list(cols.get("left")) or ["summary","skills","education","certifications","languages"]
        right_ids = _as_list(cols.get("right")) or ["header","contacts","experience","projects","achievements"]

        y_left = y0
        for sid in left_ids:
            y_left = render_section(_as_str(sid), left_x, y_left, left_w - 6, in_sidebar=False)
            y_left = ensure_page(y_left)

        y_right = y0
        for sid in right_ids:
            y_right = render_section(_as_str(sid), right_x, y_right, right_w - 6, in_sidebar=False)
            y_right = ensure_page(y_right)

    else:
        ids = order or ["header","contacts","summary","experience","projects","education","skills","achievements","certifications","languages"]
        y = y0
        for sid in ids:
            y = render_section(_as_str(sid), x0, y, usable_w, in_sidebar=False)
            y = ensure_page(y)

    c.save()
    return buf.getvalue()
