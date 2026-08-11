import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

NAVY="#1F3763"; GREEN="#26815C"; PURPLE="#6043A3"; INK="#25303B"; GREY="#6B7480"

MONTHS=["May","Jun","Jul"]; x=np.arange(3)
plt.rcParams.update({"font.family":"DejaVu Sans","axes.edgecolor":"#C9CFD6",
    "axes.linewidth":0.8,"text.color":INK,"xtick.color":GREY,"ytick.color":GREY})

# target picture boxes (EMU) -> aspect  (keep same layout positions)
BOX={"r1":(1765309,738000),"r2":(1652701,712008),"r3":(2196200,648000),"r5":(2060375,648000)}
def newfig(key,h=1.45):
    w=h*BOX[key][0]/BOX[key][1]
    fig,ax=plt.subplots(figsize=(w,h),dpi=300)
    return fig,ax
def clean(ax):
    for sp in ("top","right","left"): ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#C9CFD6")
    ax.tick_params(length=0,pad=2); ax.set_xticks(x); ax.set_xticklabels(MONTHS,fontsize=9)
    ax.set_yticks([]); ax.margins(x=0.11)
def save(fig,name,top=0.82,bottom=0.20,left=0.035,right=0.985):
    fig.subplots_adjust(left=left,right=right,top=top,bottom=bottom)
    fig.savefig(f"charts/{name}.png",dpi=300,transparent=True); plt.close(fig)

# ---- row1: MAU + DAU (Apr-Jul) ----
MAU=[1093,1377,1573]; DAU=[200,271,298]
fig,ax=newfig("r1"); clean(ax)
ax.plot(x,MAU,color=NAVY,lw=2.0,marker="o",ms=3.6)
ax.plot(x,DAU,color=PURPLE,lw=2.0,marker="o",ms=3.6)
ax.annotate(f"{MAU[-1]:,}",(x[-1],MAU[-1]),textcoords="offset points",xytext=(0,5),
            fontsize=8.5,fontweight="bold",color=NAVY,ha="center")
ax.annotate(f"{DAU[-1]:,}",(x[-1],DAU[-1]),textcoords="offset points",xytext=(0,5),
            fontsize=8.5,fontweight="bold",color=PURPLE,ha="center")
ax.text(0,1.12,"MAU",transform=ax.transAxes,color=NAVY,fontsize=8,fontweight="bold")
ax.text(0.24,1.12,"DAU",transform=ax.transAxes,color=PURPLE,fontsize=8,fontweight="bold")
ax.set_ylim(0,max(MAU)*1.20)
save(fig,"j_row1")

# ---- row2: fulfilment % (network lane) Apr-Jul ----
PF=[11.2,17.1,18.0]
fig,ax=newfig("r2"); clean(ax)
ax.fill_between(x,PF,color=GREEN,alpha=0.12)
ax.plot(x,PF,color=GREEN,lw=2.1,marker="o",ms=3.8)
for xi,yi in zip(x,PF):
    dy=8 if (yi==max(PF) or xi==0) else -13
    ax.annotate(f"{yi:.1f}%",(xi,yi),textcoords="offset points",xytext=(0,dy),
                fontsize=8.4,fontweight="bold",color=GREEN,ha="center")
ax.set_ylim(0,max(PF)*1.45)
ax.text(0,1.12,"Fulfilment %",transform=ax.transAxes,color=GREEN,fontsize=8,fontweight="bold")
save(fig,"j_row2")

# ---- row3: AI vs Manual inventory (stacked) Apr-Jul ----
AI=[1043,869,687]; MAN=[304,449,972]
fig,ax=newfig("r3"); clean(ax)
ax.bar(x,MAN,width=0.46,color="#C7CDD6")
ax.bar(x,AI,width=0.46,bottom=MAN,color=PURPLE)
tot=[a+m for a,m in zip(AI,MAN)]
ax.annotate(f"AI {AI[-1]:,}",(x[-1],tot[-1]),textcoords="offset points",xytext=(0,2),
            fontsize=8.0,fontweight="bold",color=PURPLE,ha="center")
ax.set_ylim(0,max(tot)*1.22)
ax.text(0,1.11,"AI agent",transform=ax.transAxes,color=PURPLE,fontsize=8,fontweight="bold")
ax.text(0.30,1.11,"Manual inventory",transform=ax.transAxes,color=GREY,fontsize=8,fontweight="bold")
save(fig,"j_row3")

# ---- row5: ledger status badge ----
fig,ax=newfig("r5")
ax.axis("off")
ax.add_patch(plt.Rectangle((0.02,0.16),0.96,0.68,transform=ax.transAxes,
             fill=True,facecolor="#F1ECF9",edgecolor=PURPLE,lw=1.1))
ax.text(0.5,0.60,"Phase-1 live  ·  Jul'26",transform=ax.transAxes,ha="center",
        fontsize=10.5,fontweight="bold",color=PURPLE)
ax.text(0.5,0.30,"Immutable ledger + wallets + TDS",transform=ax.transAxes,ha="center",
        fontsize=8,color=GREY)
save(fig,"j_row5",top=0.98,bottom=0.02)

print("done")
