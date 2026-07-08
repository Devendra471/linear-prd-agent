import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
import numpy as np, os

OUT = "charts"
os.makedirs(OUT, exist_ok=True)

# Deck palette
NAVY   = "#1F3763"
GREEN  = "#26815C"
PURPLE = "#6043A3"
AMBER  = "#C77D0A"
GREY   = "#9AA3AF"
INK    = "#25303B"

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
x = np.arange(6)

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 8.5,
    "axes.edgecolor": "#C9CFD6",
    "axes.linewidth": 0.8,
    "text.color": INK,
    "axes.labelcolor": INK,
    "xtick.color": "#6B7480",
    "ytick.color": "#6B7480",
})

FIGSIZE = (3.25, 0.96)
DPI = 300

def base_ax():
    fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color("#C9CFD6")
    ax.tick_params(length=0, pad=1.5)
    ax.set_xticks(x)
    ax.set_xticklabels([m[0] for m in MONTHS], fontsize=7.5)
    ax.set_yticks([])
    ax.margins(x=0.06)
    return fig, ax

def endlabel(ax, xs, ys, color, fmt="{:,.0f}", dy=6, first=False):
    ax.annotate(fmt.format(ys[-1]), (xs[-1], ys[-1]), textcoords="offset points",
                xytext=(2, dy), fontsize=7.6, fontweight="bold", color=color, ha="left")
    if first:
        ax.annotate(fmt.format(ys[0]), (xs[0], ys[0]), textcoords="offset points",
                    xytext=(-1, dy), fontsize=7.0, color=color, ha="right")

def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png", dpi=DPI, bbox_inches="tight", pad_inches=0.04,
                transparent=True)
    plt.close(fig)

# ---------- 1. FO App adoption: MAU / DAU ----------
DAU = [107,160,166,178,200,252]
MAU = [717,847,990,1027,1093,1325]
fig, ax = base_ax()
ax.plot(x, MAU, color=NAVY,  lw=1.9, marker="o", ms=2.6)
ax.plot(x, DAU, color=PURPLE,lw=1.9, marker="o", ms=2.6)
endlabel(ax, x, MAU, NAVY,  dy=4)
endlabel(ax, x, DAU, PURPLE,dy=6)
ax.text(0, 1.14, "MAU", transform=ax.transAxes, color=NAVY, fontsize=7, fontweight="bold")
ax.text(0.22, 1.14, "DAU", transform=ax.transAxes, color=PURPLE, fontsize=7, fontweight="bold")
ax.set_ylim(0, max(MAU)*1.18)
save(fig, "row1_app")

# ---------- 2. Demand fulfilment: Bids (bars) + Placeable Fulfilled % (line) ----------
BIDS = [206,332,510,670,477,725]
PF   = [37.8,22.4,11.2,19.4,17.3,24.9]
fig, ax = base_ax()
ax.bar(x, BIDS, width=0.62, color="#D8DEE9", zorder=1)
ax.bar(x[-1], BIDS[-1], width=0.62, color=NAVY, zorder=1)
ax.annotate(f"{BIDS[-1]:,}", (x[-1], BIDS[-1]), textcoords="offset points",
            xytext=(0, 2), fontsize=7.4, fontweight="bold", color=NAVY, ha="center")
ax2 = ax.twinx()
ax2.plot(x, PF, color=GREEN, lw=1.9, marker="o", ms=2.6, zorder=3)
for sp in ("top","right","left"): ax2.spines[sp].set_visible(False)
ax2.set_yticks([]); ax2.tick_params(length=0)
ax2.annotate(f"{PF[-1]:.0f}%", (x[-1], PF[-1]), textcoords="offset points",
             xytext=(3, -2), fontsize=7.6, fontweight="bold", color=GREEN, ha="left")
ax2.set_ylim(0, max(PF)*1.35)
ax.set_ylim(0, max(BIDS)*1.25)
ax.text(0, 1.14, "Bids placed", transform=ax.transAxes, color=NAVY, fontsize=7, fontweight="bold")
ax.text(0.52, 1.14, "Placeable fulfilment %", transform=ax.transAxes, color=GREEN, fontsize=7, fontweight="bold")
save(fig, "row2_demand")

# ---------- 3. Inventory: AI vs Manual (stacked bars) + conversion % ----------
AI  = [15,151,276,728,1043,869]
MAN = [2206,2010,1604,1098,303,472]
fig, ax = base_ax()
ax.bar(x, MAN, width=0.64, color="#C7CDD6", label="Manual", zorder=1)
ax.bar(x, AI,  width=0.64, bottom=MAN, color=PURPLE, label="AI agent", zorder=1)
tot = [a+m for a,m in zip(AI,MAN)]
ax.annotate(f"AI {AI[-1]:,}", (x[-1], tot[-1]), textcoords="offset points",
            xytext=(0, 2), fontsize=7.2, fontweight="bold", color=PURPLE, ha="center")
ax.set_ylim(0, max(tot)*1.2)
ax.text(0, 1.14, "AI agent", transform=ax.transAxes, color=PURPLE, fontsize=7, fontweight="bold")
ax.text(0.34, 1.14, "Manual inventory", transform=ax.transAxes, color="#6B7480", fontsize=7, fontweight="bold")
save(fig, "row3_inventory")

# ---------- 4. Cost to serve: Agent calls scaled ----------
CALLS = [121,1181,3009,12131,16136,8773]
fig, ax = base_ax()
ax.fill_between(x, CALLS, color=GREEN, alpha=0.14, zorder=1)
ax.plot(x, CALLS, color=GREEN, lw=2.0, marker="o", ms=2.6, zorder=2)
ax.annotate("16.1k", (4, CALLS[4]), textcoords="offset points",
            xytext=(0, 4), fontsize=7.2, fontweight="bold", color=GREEN, ha="center")
ax.annotate("8.8k", (5, CALLS[5]), textcoords="offset points",
            xytext=(3, -2), fontsize=7.4, fontweight="bold", color=GREEN, ha="left")
ax.set_ylim(0, max(CALLS)*1.2)
ax.text(0, 1.14, "Agent-initiated calls / month", transform=ax.transAxes, color=GREEN, fontsize=7, fontweight="bold")
save(fig, "row4_cost")

# ---------- 5. Ledger automation: new initiative ----------
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
ax.axis("off")
ax.add_patch(plt.Rectangle((0.03,0.18),0.94,0.64, transform=ax.transAxes,
             fill=True, facecolor="#F1ECF9", edgecolor=PURPLE, lw=1.0))
ax.text(0.5,0.62,"Kicked off  Jun'26", transform=ax.transAxes, ha="center",
        fontsize=8.6, fontweight="bold", color=PURPLE)
ax.text(0.5,0.34,"Baseline metrics from Q3", transform=ax.transAxes, ha="center",
        fontsize=7.2, color="#6B7480")
save(fig, "row5_ledger")

print("charts written:", sorted(os.listdir(OUT)))
