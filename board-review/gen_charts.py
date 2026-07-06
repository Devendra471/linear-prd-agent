"""Generate the four Jan-Jun'26 trend charts for the board-review slide."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
import os
MONTHS=["Jan","Feb","Mar","Apr","May","Jun"]
BLUE="#2a78d6"; ORANGE="#eb6834"; INK="#111827"; SEC="#5D6675"; GRID="#D6DEE8"; BAND="#EEF3FA"
Q=3
os.makedirs("charts",exist_ok=True)
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":6.5,"text.color":INK,"xtick.color":SEC})
def base():
    fig,ax=plt.subplots(figsize=(2.35,0.80),dpi=300)
    fig.patch.set_alpha(0); ax.patch.set_alpha(0)
    for sp in["top","right","left"]:ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GRID); ax.spines["bottom"].set_linewidth(0.8)
    ax.yaxis.set_major_locator(NullLocator())
    ax.set_xticks(range(6)); ax.set_xticklabels(MONTHS,fontsize=5.6)
    ax.tick_params(axis="x",length=0,pad=1.5); ax.margins(x=0.04)
    return fig,ax
def band(ax): ax.axvspan(Q-0.35,5.35,color=BAND,zorder=0)
def finish(fig,n):
    fig.subplots_adjust(left=0.02,right=0.84,top=0.985,bottom=0.20)
    fig.savefig(f"charts/{n}.png",transparent=True,dpi=300); plt.close(fig)
def single(n,vals,fmt,color=BLUE):
    fig,ax=base(); ymin=min(vals);ymax=max(vals);pad=(ymax-ymin)*0.28 or 1
    ax.set_ylim(ymin-pad*0.4,ymax+pad); band(ax)
    ax.plot(range(6),vals,color=color,lw=1.2,alpha=0.32,zorder=2)
    ax.plot(range(Q,6),vals[Q:],color=color,lw=2.0,zorder=3)
    ax.scatter(range(Q,6),vals[Q:],s=13,color=color,zorder=4,edgecolor="white",linewidth=0.6)
    ax.annotate(fmt(vals[-1]),(5,vals[-1]),xytext=(4,0),textcoords="offset points",
        fontsize=7.2,fontweight="bold",color=INK,va="center",ha="left",annotation_clip=False)
    finish(fig,n)
def dual(n,a,b,la,lb,ca=BLUE,cb=ORANGE):
    fig,ax=base(); allv=a+b;ymin=min(allv);ymax=max(allv);pad=(ymax-ymin)*0.20 or 1
    ax.set_ylim(ymin-pad,ymax+pad*1.6); band(ax)
    for vals,c in[(a,ca),(b,cb)]:
        ax.plot(range(6),vals,color=c,lw=1.1,alpha=0.32,zorder=2)
        ax.plot(range(Q,6),vals[Q:],color=c,lw=2.0,zorder=3)
        ax.scatter([5],[vals[-1]],s=13,color=c,zorder=4,edgecolor="white",linewidth=0.6)
    ax.annotate(la,(5,a[-1]),xytext=(4,0),textcoords="offset points",fontsize=6.2,fontweight="bold",color=ca,va="center",ha="left",annotation_clip=False)
    ax.annotate(lb,(5,b[-1]),xytext=(4,0),textcoords="offset points",fontsize=6.2,fontweight="bold",color=cb,va="center",ha="left",annotation_clip=False)
    finish(fig,n)
# Metrics: Jan..Jun 2026
single("c1_dau",[107,160,166,178,200,252],lambda v:f"{v}")
single("c2_fulfil",[57.7,33.6,18.7,31.0,29.3,43.5],lambda v:f"{v:.0f}%")
dual("c3_inv",[15,151,276,728,1043,869],[2206,2010,1604,1098,303,472],"AI 869","Man 472")
single("c4_calls",[121,1181,3009,12131,16136,8773],lambda v:f"{v/1000:.1f}k")
print("charts generated")
