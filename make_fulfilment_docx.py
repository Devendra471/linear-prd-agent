#!/usr/bin/env python3
"""Editable .docx version of the Fulfilment Initiatives one-pager (business-team note)."""
from docx import Document
from docx.shared import Pt, Mm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY = "0F2A4A"; GREEN = "2E7D44"; BLUE = "3F72A8"; ORANGE = "9A4E0E"; GREY = "6B7F96"
CARD_BG = "F7FAFC"; GREEN_BG = "F4FAF5"; BACK_BG = "F0FAF2"; BLUE_BG = "EEF3F8"
AMBER_BG = "FFF7F0"; ALT_BG = "F7FAFC"
T_NOW = "E2F3E6"; T_MONTH = "EEF3F8"; T_DEC = "FDEBD7"; T_NEXT = "F1F5F9"

doc = Document()
sec = doc.sections[0]
sec.page_height, sec.page_width = Mm(297), Mm(210)
sec.top_margin = sec.bottom_margin = Mm(9)
sec.left_margin = sec.right_margin = Mm(11)

style = doc.styles["Normal"]
style.font.name = "Calibri"; style.font.size = Pt(8.5)
style.paragraph_format.space_after = Pt(0); style.paragraph_format.space_before = Pt(0)

def shade(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)

def borders(cell, color="DBE3EC", sz=4, edges=("top","bottom","left","right")):
    tcPr = cell._tc.get_or_add_tcPr()
    tb = OxmlElement("w:tcBorders")
    for e in edges:
        el = OxmlElement(f"w:{e}")
        el.set(qn("w:val"), "single"); el.set(qn("w:sz"), str(sz)); el.set(qn("w:color"), color)
        tb.append(el)
    tcPr.append(tb)

def topbar(cell, color, sz=24):
    tcPr = cell._tc.get_or_add_tcPr()
    tb = OxmlElement("w:tcBorders")
    el = OxmlElement("w:top"); el.set(qn("w:val"), "single"); el.set(qn("w:sz"), str(sz)); el.set(qn("w:color"), color)
    tb.append(el)
    for e in ("bottom","left","right"):
        x = OxmlElement(f"w:{e}"); x.set(qn("w:val"), "single"); x.set(qn("w:sz"), "4"); x.set(qn("w:color"), "CDD9E6")
        tb.append(x)
    tcPr.append(tb)

def leftbar(cell, color, fill, sz=24):
    tcPr = cell._tc.get_or_add_tcPr()
    tb = OxmlElement("w:tcBorders")
    el = OxmlElement("w:left"); el.set(qn("w:val"), "single"); el.set(qn("w:sz"), str(sz)); el.set(qn("w:color"), color)
    tb.append(el)
    for e in ("top","bottom","right"):
        x = OxmlElement(f"w:{e}"); x.set(qn("w:val"), "single"); x.set(qn("w:sz"), "4"); x.set(qn("w:color"), color)
        tb.append(x)
    tcPr.append(tb)
    shade(cell, fill)

def no_borders(table):
    pr = table._tbl.tblPr
    b = OxmlElement("w:tblBorders")
    for e in ("top","left","bottom","right","insideH","insideV"):
        el = OxmlElement(f"w:{e}"); el.set(qn("w:val"), "none"); b.append(el)
    pr.append(b)

def runs_into(p, runs, size, align):
    p.alignment = {"l": WD_ALIGN_PARAGRAPH.LEFT, "c": WD_ALIGN_PARAGRAPH.CENTER}[align]
    for text, bold, color, italic in runs:
        parts = text.split("\n")
        for i, part in enumerate(parts):
            if i > 0:
                p = p._parent.add_paragraph()
                p.alignment = {"l": WD_ALIGN_PARAGRAPH.LEFT, "c": WD_ALIGN_PARAGRAPH.CENTER}[align]
                p.paragraph_format.space_before = Pt(0); p.paragraph_format.space_after = Pt(0)
            r = p.add_run(part)
            r.bold = bold; r.italic = italic; r.font.size = Pt(size)
            r.font.color.rgb = RGBColor.from_string(color)
    return p

def cell_runs(cell, runs, align="l", size=8, sb=2, sa=2):
    cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(sb); p.paragraph_format.space_after = Pt(sa)
    runs_into(p, runs, size, align)

def heading(num, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(7); p.paragraph_format.space_after = Pt(3)
    r = p.add_run(f" {num} ")
    r.bold = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor.from_string("FFFFFF")
    rPr = r._element.get_or_add_rPr()
    shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), NAVY); rPr.append(shd)
    r2 = p.add_run("  " + text)
    r2.bold = True; r2.font.size = Pt(10.5); r2.font.color.rgb = RGBColor.from_string(NAVY)
    pb = OxmlElement("w:pBdr"); btm = OxmlElement("w:bottom")
    btm.set(qn("w:val"), "single"); btm.set(qn("w:sz"), "8"); btm.set(qn("w:color"), "E2E8F0")
    pb.append(btm); p._p.get_or_add_pPr().append(pb)

def callout(border_color, fill, runs_blocks, title=None, title_color=None):
    t = doc.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    no_borders(t)
    c = t.rows[0].cells[0]; c.width = Mm(188)
    shade(c, fill); leftbar(c, border_color, fill, sz=28)
    first = True
    if title:
        p = c.paragraphs[0]; p.paragraph_format.space_before = Pt(4); p.paragraph_format.space_after = Pt(2)
        r = p.add_run(title); r.bold = True; r.font.size = Pt(9); r.font.color.rgb = RGBColor.from_string(title_color)
        first = False
    for block in runs_blocks:
        if first:
            p = c.paragraphs[0]; first = False
        else:
            p = c.add_paragraph()
        p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(3)
        runs_into(p, block, 8.4, "l")
    return t

# ---------- TITLE BAR ----------
t = doc.add_table(rows=1, cols=1); no_borders(t)
c = t.rows[0].cells[0]; c.width = Mm(188); shade(c, NAVY)
cell_runs(c, [("Fulfilment Initiatives — What We Can Start Now", True, "FFFFFF", False)], size=15, sb=5, sa=0)
p = c.add_paragraph(); p.paragraph_format.space_after = Pt(5)
r = p.add_run("Note for the business team   •   Sequencing the three founder-led initiatives around current bandwidth   •   June 2026")
r.font.size = Pt(8.2); r.font.color.rgb = RGBColor.from_string("BCD3EC")

# ---------- BOTTOM LINE ----------
callout(NAVY, BLUE_BG, [[
    ("Bottom line. ", True, NAVY, False),
    ("For the next ~1 month, product & tech bandwidth is committed to ", False, "1E293B", False),
    ("Ledger and CT automation", True, NAVY, False),
    (", so the three fulfilment initiatives can’t take full engineering effort yet. We can still ", False, "1E293B", False),
    ("start the Onboarding Agent now", True, NAVY, False),
    (" — its content/video track needs HR and Product, not engineering. But none of the three initiatives will pay off until ", False, "1E293B", False),
    ("placement actually runs inside the CRM", True, NAVY, False),
    (", which today it largely does not. That alignment is the one thing we need from business first.", False, "1E293B", False),
]])

# ---------- SECTION 1: cards ----------
heading("1", "The three founder-led initiatives — and their shared backbone")
cards = [
    ("Onboarding Agent", "Cut time-to-productive for new Fulfilment Agents (14 days → Day 2) using bite-size videos and a live call co-pilot."),
    ("AI Fulfilment Agent", "An AI caller that places loads end-to-end on selected lanes — covering month-end peaks, night shifts and FA absences."),
    ("FO Movement Signal", "Use FASTag + GPS to see where each FO’s trucks actually run, and match demand to those real lanes."),
]
t = doc.add_table(rows=1, cols=3); t.alignment = WD_TABLE_ALIGNMENT.CENTER; no_borders(t)
for j, (h, b) in enumerate(cards):
    c = t.rows[0].cells[j]; c.width = Mm(62); shade(c, CARD_BG); topbar(c, BLUE)
    cell_runs(c, [(h + "\n", True, NAVY, False), (b, False, "334155", False)], size=8, sb=3, sa=3)
callout(GREEN, BACK_BG, [[
    ("Shared backbone: ", True, "1F5C31", False),
    ("all three depend on ", False, "1E293B", False),
    ("system-driven calling", True, "1F5C31", False),
    (" (calls placed from CRM, auto-recorded and tagged) and a ", False, "1E293B", False),
    ("library of top-agent call recordings", True, "1F5C31", False),
    (". We are already running calling for inventory and consent flows — that live experience directly feeds the fulfilment agent.", False, "1E293B", False),
]])

# ---------- SECTION 2: start now ----------
heading("2", "Start now — Onboarding Agent content track (no/low tech)")
parts = [
    ("1", "HR docs → bite-size videos", "Convert the onboarding material HR already has into short, mobile-first videos and micro-docs."),
    ("2", "Top-agent calls → clips", "Curate recordings from our best Fulfilment Agents into short clips by scenario — e.g. how to negotiate rate with fleet owners."),
    ("3", "Product how-to videos", "Short walkthroughs of the CRM placement flow, packaged alongside the negotiation clips."),
]
t = doc.add_table(rows=1, cols=3); t.alignment = WD_TABLE_ALIGNMENT.CENTER; no_borders(t)
for j, (n, h, b) in enumerate(parts):
    c = t.rows[0].cells[j]; c.width = Mm(62); shade(c, GREEN_BG); borders(c, "BFDEC5", sz=6)
    p = c.paragraphs[0]; p.paragraph_format.space_before = Pt(3); p.paragraph_format.space_after = Pt(2)
    rn = p.add_run(f" {n} "); rn.bold = True; rn.font.size = Pt(8); rn.font.color.rgb = RGBColor.from_string("FFFFFF")
    rPr = rn._element.get_or_add_rPr(); shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), GREEN); rPr.append(shd)
    rh = p.add_run("  " + h); rh.bold = True; rh.font.size = Pt(8.4); rh.font.color.rgb = RGBColor.from_string("1F5C31")
    p2 = c.add_paragraph(); p2.paragraph_format.space_after = Pt(3)
    r2 = p2.add_run(b); r2.font.size = Pt(8); r2.font.color.rgb = RGBColor.from_string("334155")
p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(3); p.paragraph_format.space_after = Pt(2)
r = p.add_run("Owners: "); r.bold = True; r.font.size = Pt(8); r.font.color.rgb = RGBColor.from_string("475569")
r = p.add_run("HR + Ravi + Product, working in parallel — "); r.font.size = Pt(8); r.font.color.rgb = RGBColor.from_string("475569")
r = p.add_run("no engineering dependency."); r.bold = True; r.font.size = Pt(8); r.font.color.rgb = RGBColor.from_string("475569")

# ---------- SECTION 3: phasing ----------
heading("3", "Then, as product bandwidth opens up — the phased path")
phases = [
    ("Phase 1\nNow", GREEN, [("Onboarding content & videos", True), (" (the three parts above). Doable immediately, in parallel, without engineering.", False)]),
    ("Phase 2\nWith product", BLUE, [("Embed the flows into the CRM", True), (" so new joiners watch the curated recordings in-product — and build the ", False), ("Evolve agent", True), (" that listens to live call recordings, scores them, and gives agents specific feedback on what to improve.", False)]),
    ("Phase 3\nAfter Ledger", GREY, [("AI Fulfilment Agent", True), (" placing loads end-to-end on selected lanes — once the calling infrastructure and CRM adoption are solid.", False)]),
]
t = doc.add_table(rows=len(phases), cols=2); t.alignment = WD_TABLE_ALIGNMENT.CENTER
for i, (label, color, body) in enumerate(phases):
    c0, c1 = t.rows[i].cells
    c0.width = Mm(30); c1.width = Mm(158)
    borders(c0); borders(c1); shade(c0, color)
    if i % 2 == 1: shade(c1, ALT_BG)
    c0.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    cell_runs(c0, [(label, True, "FFFFFF", False)], align="c", size=8, sb=3, sa=3)
    cell_runs(c1, [(txt, b, "1E293B", False) for txt, b in body], size=8, sb=3, sa=3)

# ---------- SECTION 4: alignment ----------
heading("4", "The one alignment we need from business first")
callout("D97A2B", AMBER_BG, [
    [("Today, CRM adoption for placement is ", False, "1E293B", False),
     ("low", True, ORANGE, False),
     (" — a large share of placements still happen ", False, "1E293B", False),
     ("outside the system", True, ORANGE, False),
     (". When placement happens off-system, the supply and bids we collect go unused, and ", False, "1E293B", False),
     ("none of these three initiatives can scale", True, ORANGE, False),
     (", no matter how good the tooling is.", False, "1E293B", False)],
    [("Ask: ", True, ORANGE, False),
     ("business to commit to (1) running every placement through the CRM, and (2) acting on every demand from the demand aggregator inside the system. This is the foundation everything else builds on.", False, "1E293B", False)],
], title="Placement must run inside the CRM", title_color=ORANGE)

# ---------- SECTION 5: actionables ----------
heading("5", "Actionables")
rows = [
    ("Continue Ledger + CT automation; limited fulfilment-tech bandwidth this month", "Product / Tech", False, "This month", T_MONTH, NAVY),
    ("Onboarding content track — convert HR docs into bite-size videos", "HR + Ravi + Product", False, "Start now", T_NOW, "1F5C31"),
    ("Curate top-agent call recordings into scenario clips", "Fulfilment leads — [confirm]", True, "Start now", T_NOW, "1F5C31"),
    ("Product how-to / FO-negotiation videos", "Product + Ravi", False, "Start now", T_NOW, "1F5C31"),
    ("Business alignment — placement runs in CRM; act on all aggregator demand", "Business heads — [confirm]", True, "Decision needed", T_DEC, ORANGE),
    ("Scope calling-infrastructure gaps (Phase 0/2 prerequisite)", "Product", False, "Next", T_NEXT, "475569"),
    ("Evolve agent & AI Fulfilment Agent build", "[post-Ledger / CT — TBD]", True, "Later", T_NEXT, "475569"),
]
t = doc.add_table(rows=len(rows) + 1, cols=3); t.alignment = WD_TABLE_ALIGNMENT.CENTER
widths = [Mm(86), Mm(64), Mm(38)]
hdr = t.rows[0]
for j, txt in enumerate(["Action", "Owner", "When"]):
    c = hdr.cells[j]; c.width = widths[j]; shade(c, NAVY); borders(c)
    cell_runs(c, [(txt, True, "FFFFFF", False)], size=8.1, sb=2, sa=2)
for i, (action, owner, owner_ph, when, when_bg, when_col) in enumerate(rows):
    row = t.rows[i + 1]
    for j in range(3): row.cells[j].width = widths[j]; borders(row.cells[j])
    if i % 2 == 1:
        shade(row.cells[0], ALT_BG); shade(row.cells[1], ALT_BG)
    # action (bold the alignment row)
    a_bold = action.startswith("Business alignment")
    if a_bold:
        cell_runs(row.cells[0], [("Business alignment", True, "1E293B", False),
                                 (" — placement runs in CRM; act on all aggregator demand", False, "1E293B", False)], size=8, sb=2, sa=2)
    else:
        cell_runs(row.cells[0], [(action, False, "1E293B", False)], size=8, sb=2, sa=2)
    cell_runs(row.cells[1], [(owner, False, "94A3B8" if owner_ph else "1E293B", owner_ph)], size=8, sb=2, sa=2)
    cw = row.cells[2]
    cw.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
    p = cw.paragraphs[0]; p.paragraph_format.space_before = Pt(2); p.paragraph_format.space_after = Pt(2)
    rt = p.add_run(" " + when + " "); rt.bold = True; rt.font.size = Pt(7.4); rt.font.color.rgb = RGBColor.from_string(when_col)
    rPr = rt._element.get_or_add_rPr(); shd = OxmlElement("w:shd"); shd.set(qn("w:val"), "clear"); shd.set(qn("w:fill"), when_bg); rPr.append(shd)

# footnote
p = doc.add_paragraph(); p.paragraph_format.space_before = Pt(5)
r = p.add_run("Placeholders marked [confirm] / [TBD] need owners and dates filled in. “CT automation” refers to the in-flight compliance-automation workstream — confirm the exact name before sharing.")
r.italic = True; r.font.size = Pt(7.6); r.font.color.rgb = RGBColor.from_string("64748B")

doc.save("Fulfilment_Initiatives.docx")
print("saved")
