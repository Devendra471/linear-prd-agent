from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

prs = Presentation("deck.pptx"); s = prs.slides[0]
FONT="Manrope"
INK=RGBColor(0x11,0x18,0x27); SEC=RGBColor(0x5D,0x66,0x75); WHITE=RGBColor(0xFF,0xFF,0xFF)
BORDER=RGBColor(0xD6,0xDE,0xE8)
FILL_W=RGBColor(0xFF,0xFF,0xFF); FILL_G=RGBColor(0xF1,0xFB,0xF5); FILL_A=RGBColor(0xFF,0xF2,0xCC)
H_PROJ=RGBColor(0x1F,0x37,0x63); H_DEL=RGBColor(0x26,0x81,0x5C); H_TREND=RGBColor(0x60,0x43,0xA3); H_NEXT=RGBColor(0xB4,0x53,0x09)
GREEN=RGBColor(0x1C,0x6B,0x2D); RED=RGBColor(0x98,0x00,0x00)

KEEP={100,142,143,150,151}
for sh in list(s.shapes):
    if sh.shape_id not in KEEP: sh._element.getparent().remove(sh._element)

title=[sh for sh in s.shapes if sh.shape_id==100][0]
p0=title.text_frame.paragraphs[0]
p0.runs[0].text="Product & Tech Updates — Carrier Matching"
for r in p0.runs[1:]: r.text=""
if len(title.text_frame.paragraphs)>1 and title.text_frame.paragraphs[1].runs:
    title.text_frame.paragraphs[1].runs[0].text="Apr–Jun'26 Board & Monthly Review  ·  Steady momentum; pedal on inventory & demand fulfilment"

def rrect(x,y,w,h,fill,line=BORDER,radius=0.06):
    sh=s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
    sh.fill.solid(); sh.fill.fore_color.rgb=fill
    if line is None: sh.line.fill.background()
    else: sh.line.color.rgb=line; sh.line.width=Pt(0.75)
    try: sh.adjustments[0]=radius
    except: pass
    sh.shadow.inherit=False; return sh
def textbox(x,y,w,h,paras,anchor=MSO_ANCHOR.MIDDLE,align=PP_ALIGN.LEFT,ml=0.05,mr=0.04):
    tb=s.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf=tb.text_frame; tf.word_wrap=True; tf.vertical_anchor=anchor
    tf.margin_left=Inches(ml); tf.margin_right=Inches(mr); tf.margin_top=Inches(0.01); tf.margin_bottom=Inches(0.01)
    for i,para in enumerate(paras):
        p=tf.paragraphs[0] if i==0 else tf.add_paragraph()
        p.alignment=align; p.space_before=Pt(0); p.space_after=Pt(1.5); p.line_spacing=1.0
        for (txt,bold,size,color) in para:
            r=p.add_run(); r.text=txt; r.font.name=FONT; r.font.bold=bold; r.font.size=Pt(size); r.font.color.rgb=color
    return tb
def header(x,w,text,color):
    rrect(x,0.80,w,0.24,color,line=None,radius=0.18)
    textbox(x,0.80,w,0.24,[[(text,True,8,WHITE)]],anchor=MSO_ANCHOR.MIDDLE,align=PP_ALIGN.CENTER)

C1x,C1w=0.30,1.52
C2x,C2w=1.87,2.30
C3x,C3w=4.22,3.14
C4x,C4w=7.41,2.27
header(C1x,C1w,"PROJECT",H_PROJ)
header(C2x,C2w,"DELIVERED · APR–JUN'26",H_DEL)
header(C3x,C3w,"METRICS & TREND (JAN–JUN'26)",H_TREND)
header(C4x,C4w,"NEXT FOCUS · JUL–AUG",H_NEXT)
rows=[(1.08,0.82,FILL_W),(1.93,0.82,FILL_G),(2.78,0.82,FILL_W),(3.63,0.82,FILL_G),(4.48,0.60,FILL_A)]
B=INK
def bl(txt,bold=False,size=6.5,color=B,mk="• "): return [(mk,False,size,color),(txt,bold,size,color)]

content=[
 dict(obj="Drive FO App to 2,000 DAU", sub="Better load experience & payment visibility",
   feats=[bl("Load discovery & experience revamp"),bl("In-app payment visibility"),bl("Bid & trip status surfacing")],
   metrics=[[("DAU 178→",False,6.5,B),("252",True,6.5,GREEN),(" (+42%)",False,6.5,B)],
            [("Installs 1,449→1,935",False,6.5,B)],[("MAU 1,027→1,325",False,6.5,B)]],
   chart="charts/c1_dau.png",
   nxt=[bl("Payment status timeline in FO App (POD→UTR)"),bl("Push DAU toward 2,000"),bl("Lift WAU (582→747), cut uninstalls")]),
 dict(obj="Improve demand fulfilment to 50%", sub="Matching, bid ranges & real-time visibility",
   feats=[bl("Suggested bid ranges"),bl("Real-time matching visibility"),bl("FO–demand matching tuning")],
   metrics=[[("Placeable fulfil 31→",False,6.5,B),("43.5%",True,6.5,GREEN)],
            [("Bids 670→725",False,6.5,B)],[("Unique FOs 211→267",False,6.5,B)]],
   chart="charts/c2_fulfil.png",
   nxt=[bl("Sustain 50% placeable-fulfilment target"),bl("Bid ranges & matching visibility"),bl("Rebuild bid consistency across lanes")]),
 dict(obj="Increase inventory 50% (1,500/mo)", sub="Via automated agentic calling",
   feats=[bl("Agentic calling for inventory (AI bot)"),bl("Call → inventory automation"),bl("Manual-ops reduction")],
   metrics=[[("AI inv 728→",False,6.5,B),("1,043",True,6.5,GREEN)],
            [("Manual 1,098→",False,6.5,B),("472",True,6.5,RED)],[("Agent calls → 16k",False,6.5,B)]],
   chart="charts/c3_inv.png",
   nxt=[bl("Inventory quality: best-time-to-call, power-lane, FO filtering"),bl("Lift placeable conversion (23.9→11.4%)"),bl("Grow net inventory to 1,500/mo")]),
 dict(obj="Cost to serve reduction 70%", sub="Automate ops processes",
   feats=[bl("Automated Vahan verification (LSP WhatsApp)"),bl("Automated journey/transit updates")],
   metrics=[[("~10 hrs/day CT effort saved",False,6.5,B)],[("~15% CT resource-cost cut",False,6.5,B)],
            [("Agent calls 12k→16k (peak)",False,6.5,B)]],
   chart="charts/c4_calls.png",
   nxt=[bl("FO doc collection via app incentives"),bl("AI City-Team for SIM-consent automation"),bl("Transit-delay detection")]),
 dict(obj="Ledger automation for compliance", sub="Trip & party-level ledger · NEW (Jun)",
   feats=[bl("Trip & party-level ledger — kickoff")],
   metrics=None, chart=None,
   nxt=[bl("Build trip-level & party-level ledgers"),bl("Wallet-based auto-reconciliation across trips")]),
]
for (y,h,fill),c in zip(rows,content):
    rrect(C1x,y,C1w,h,fill); rrect(C2x,y,C2w,h,fill); rrect(C3x,y,C3w,h,fill); rrect(C4x,y,C4w,h,fill)
    textbox(C1x,y,C1w,h,[[(c["obj"],True,8,INK)],[(c["sub"],False,6.3,SEC)]])
    textbox(C2x,y,C2w,h,c["feats"])
    # combined metrics + trend
    if c["chart"]:
        iw=1.72; ih=iw*0.34; ix=C3x+0.05; iy=y+(h-ih)/2
        s.shapes.add_picture(c["chart"],Inches(ix),Inches(iy),Inches(iw),Inches(ih))
        textbox(C3x+1.82,y,C3w-1.86,h,c["metrics"],ml=0.03,mr=0.03)
    else:
        rrect(C3x+C3w/2-0.55,y+h/2-0.13,1.10,0.26,RGBColor(0xED,0xE7,0xF7),line=None,radius=0.5)
        textbox(C3x+C3w/2-0.55,y+h/2-0.13,1.10,0.26,[[("New · Jun'26",True,7,H_TREND)]],align=PP_ALIGN.CENTER)
    textbox(C4x,y,C4w,h,c["nxt"])
textbox(0.30,5.28,7.6,0.20,[[("Trend from monthly metrics (Jan–Jun'26); Apr–Jun highlighted. Feature names indicative — confirm against Linear delivered stories / roadmap.",False,5.5,SEC)]])
prs.save("deck_out.pptx"); print("saved")
