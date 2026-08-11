from pptx import Presentation
from pptx.oxml.ns import qn
from copy import deepcopy

p=Presentation("july.pptx"); s=p.slides[0]

def para_set_text(p_elem, text):
    runs=p_elem.findall(qn('a:r'))
    first=runs[0]
    t=first.find(qn('a:t'))
    if t is None:
        t=first.makeelement(qn('a:t'),{}); first.append(t)
    t.text=text
    for r in runs[1:]:
        p_elem.remove(r)

def rewrite(shape_id, bullets):
    for sh in s.shapes:
        if sh.shape_id==shape_id:
            tf=sh.text_frame
            paras=[pp._p for pp in tf.paragraphs]
            template=deepcopy(paras[0])          # keep formatting of 1st paragraph
            parent=paras[0].getparent()
            for pe in paras:                     # remove all existing paragraphs
                parent.remove(pe)
            for b in bullets:
                clone=deepcopy(template)
                para_set_text(clone, b)
                parent.append(clone)
            return
    raise SystemExit("shape %s not found"%shape_id)

def set_header(shape_id, txt):
    for sh in s.shapes:
        if sh.shape_id==shape_id:
            para_set_text(sh.text_frame.paragraphs[0]._p, txt); return

# ---- headers ----
set_header(64, "JUN–JUL PROGRESS")
set_header(65, "TREND  (May–Jul'26)")

# ---- swap charts (May-Jul) ----
repl={92:'charts/j_row1.png',91:'charts/j_row2.png',78:'charts/j_row3.png',87:'charts/j_row5.png'}
for sh in list(s.shapes):
    if sh.shape_id in repl:
        L,T,W,H=sh.left,sh.top,sh.width,sh.height
        el=sh._element; el.getparent().remove(el)
        s.shapes.add_picture(repl[sh.shape_id],L,T,W,H)

# ---- Progress (Jun->Jul, delivered) ----
rewrite(69,[
 "•  POD details + payment status & timelines in app",
 "•  Proactive POD dispute/deduction alerts + re-upload",
 "•  DAU 271 → 298 (+10%); MAU 1,377 → 1,573 (+14%)",
])
rewrite(73,[
 "•  Near-match logic + match quality on demand list",
 "•  Supplier availability: lane-specific vs unavailable",
 "•  Agents onboarded (Clerk) for lane assignment",
])
rewrite(77,[
 "•  Automated AI calling for live & potential inventory (multi-lang)",
 "•  WhatsApp fallback + callback; cooldown filtering",
 "•  AI drives ~65% of inventory",
])
rewrite(82,[
 "•  Automated advance payments for Gold/Silver FOs (validation → approval → auto-release)",
 "•  WhatsApp-disconnect auto-reminders for CRM users",
 "•  Vahan verification & journey updates in LSP WhatsApp",
])
rewrite(86,[
 "•  Immutable trip-level ledger — Net Payable/Receivable (live)",
 "•  FO/LSP wallets + overpayment settlement; automated TDS",
 "•  Ledger Phase-1 foundation (journal + payouts) live",
])

# ---- Next Focus (planned / in build) ----
rewrite(70,[
 "›  Drive towards 500 DAU",
 "›  Reach PSA directly for placement (in build)",
 "›  Trip payment statement + in-app advance",
])
rewrite(74,[
 "›  Agent → lane auto-assignment (shipped)",
 "›  Prioritise demand list; Demand-Bot context (in build)",
 "›  Push network-lane fulfilment → 20%",
])
rewrite(79,[
 "›  Inventory creation on network lanes → 1,500/mo",
 "›  Improve inventory quality & conversion",
])
rewrite(83,[
 "›  Automate SIM-consent, pre-transit (in build)",
 "›  FO doc collection via App; transit-delay detection",
 "›  Auto-create Pylon tickets from LSP WhatsApp (POC)",
])
rewrite(88,[
 "›  Trip Statement — 3-yr ledger tab in FO App (in build)",
 "›  TDS rate + self-serve TDS declaration in FO App",
 "›  LSP exposure limit; wallet auto-reconciliation",
])

p.save("july_out.pptx")
print("saved july_out.pptx (Linear-refreshed)")
