from pptx import Presentation
from pptx.oxml.ns import qn
from copy import deepcopy

GREEN="26815C"; INK="25303B"

def set_style(r_elem, color_hex, bold, size=780):
    rPr=r_elem.find(qn('a:rPr'))
    if rPr is None:
        rPr=r_elem.makeelement(qn('a:rPr'),{}); r_elem.insert(0,rPr)
    rPr.set('b','1' if bold else '0')
    rPr.set('sz',str(size))
    for sf in rPr.findall(qn('a:solidFill')): rPr.remove(sf)
    sf=rPr.makeelement(qn('a:solidFill'),{})
    clr=sf.makeelement(qn('a:srgbClr'),{}); clr.set('val',color_hex)
    sf.append(clr)
    # solidFill must come after ln but before latin; safe to insert right after b handling
    rPr.insert(0,sf)

def rewrite(shape, bullets):
    tf=shape.text_frame
    paras=[pp._p for pp in tf.paragraphs]
    template=deepcopy(paras[0])
    parent=paras[0].getparent()
    for pe in paras: parent.remove(pe)
    for text,hl in bullets:
        clone=deepcopy(template)
        runs=clone.findall(qn('a:r'))
        first=runs[0]
        t=first.find(qn('a:t'))
        if t is None:
            t=first.makeelement(qn('a:t'),{}); first.append(t)
        t.text=text
        for r in runs[1:]: clone.remove(r)
        set_style(first, GREEN if hl else INK, hl)
        parent.append(clone)

DATA={
 164:[  # Drive FO App to 2,000 DAU
  ("•  My Bids + bid-status alerts; advance-pay banner", False),
  ("•  Full POD details, status & dispute alerts", False),
  ("•  Exact loading address post-win; demand alerts", False),
  ("•  DAU 178 → 252 (+42%); MAU → 1,325; Installs → 1,935", True),
 ],
 169:[  # Improve demand fulfilment
  ("•  Smarter matching: origin + normalised veh-type", False),
  ("•  Split availability lane-wise; enrich suppliers", False),
  ("•  Duplicate-demand guard; agent onboarding", False),
  ("•  Bids 477 → 725 (+52%); fulfilment 17.3 → 24.9%", True),
 ],
 174:[  # Increase inventory
  ("•  Agentic AI inventory calling — multi-lingual", True),
  ("•  GPS potential-inv detection; alt O/D capture", False),
  ("•  WhatsApp fallback + callback; Live Eval Agent", False),
  ("•  AI drives ~65% of inventory (869 of 1,341)", True),
 ],
 179:[  # Cost to serve
  ("•  Automated Vahan verification via ULIP", False),
  ("•  Auto WhatsApp trip-link + loading-memo to LSP", False),
  ("•  System STA auto-calc; adv-pay %; OCR approval", False),
  ("•  ~10 hrs/day CT saved; ~15% cost reduction", True),
 ],
 184:[  # Ledger
  ("•  Ledger design finalised — build-vs-buy decision", True),
  ("•  Phased plan; trip & party-level ledger design", False),
 ],
}

p=Presentation("board_cur.pptx"); s=p.slides[0]
for sh in s.shapes:
    if sh.shape_id in DATA:
        rewrite(sh, DATA[sh.shape_id])
p.save("board_out.pptx")
print("delivery cells updated")
