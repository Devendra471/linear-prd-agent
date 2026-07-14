import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np, os

OUT = "charts"
os.makedirs(OUT, exist_ok=True)

# Deck palette
NAVY   = "#1F3763"
GREEN  = "#26815C"
PURPLE = "#6043A3"
INK    = "#25303B"

# ---- Apr-Jun'26 window only ----
MONTHS = ["Apr", "May", "Jun"]
x = np.arange(3)

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
    ax.set_xticklabels(MONTHS, fontsize=7.5)
    ax.set_yticks([])
    ax.margins(x=0.14)
    return fig, ax

def endlabel(ax, xs, ys, color, fmt="{:,.0f}", dy=6):
    ax.annotate(fmt.format(ys[-1]), (xs[-1], ys[-1]), textcoords="offset points",
                xytext=(3, dy), fontsize=7.6, fontweight="bold", color=color, ha="left")

def save(fig, name):
    fig.savefig(f"{OUT}/{name}.png", dpi=DPI, bbox_inches="tight", pad_inches=0.04,
                transparent=True)
    plt.close(fig)

# ---------- 1. FO App adoption: MAU / DAU (Apr-Jun) ----------
MAU = [1027, 1093, 1325]
DAU = [178, 200, 252]
fig, ax = base_ax()
ax.plot(x, MAU, color=NAVY,   lw=2.0, marker="o", ms=3.4)
ax.plot(x, DAU, color=PURPLE, lw=2.0, marker="o", ms=3.4)
endlabel(ax, x, MAU, NAVY,   dy=4)
endlabel(ax, x, DAU, PURPLE, dy=4)
ax.text(0, 1.14, "MAU", transform=ax.transAxes, color=NAVY, fontsize=7, fontweight="bold")
ax.text(0.22, 1.14, "DAU", transform=ax.transAxes, color=PURPLE, fontsize=7, fontweight="bold")
ax.set_ylim(0, max(MAU)*1.18)
save(fig, "row1_app")

# ---------- 2. Demand fulfilment: Placeable Fulfilled % (Apr-Jun) ----------
PF = [13.7, 11.2, 17.1]
fig, ax = base_ax()
ax.fill_between(x, PF, color=GREEN, alpha=0.12, zorder=1)
ax.plot(x, PF, color=GREEN, lw=2.0, marker="o", ms=3.4, zorder=2)
for xi, yi in zip(x, PF):
    dy = 7 if (yi == max(PF) or xi == 0) else -11
    ax.annotate(f"{yi:.1f}%", (xi, yi), textcoords="offset points",
                xytext=(0, dy), fontsize=7.6, fontweight="bold", color=GREEN, ha="center")
ax.set_ylim(0, max(PF)*1.42)
ax.text(0, 1.14, "Placeable fulfilment %", transform=ax.transAxes,
        color=GREEN, fontsize=7, fontweight="bold")
save(fig, "row2_demand")

# ---------- 3. Inventory: AI vs Manual (Apr-Jun, stacked) ----------
AI  = [728, 1043, 869]
MAN = [1098, 303, 472]
fig, ax = base_ax()
ax.bar(x, MAN, width=0.5, color="#C7CDD6", zorder=1)
ax.bar(x, AI,  width=0.5, bottom=MAN, color=PURPLE, zorder=1)
tot = [a+m for a, m in zip(AI, MAN)]
ax.annotate(f"AI {AI[-1]:,}", (x[-1], tot[-1]), textcoords="offset points",
            xytext=(0, 2), fontsize=7.2, fontweight="bold", color=PURPLE, ha="center")
ax.set_ylim(0, max(tot)*1.2)
ax.text(0, 1.14, "AI agent", transform=ax.transAxes, color=PURPLE, fontsize=7, fontweight="bold")
ax.text(0.34, 1.14, "Manual inventory", transform=ax.transAxes, color="#6B7480", fontsize=7, fontweight="bold")
save(fig, "row3_inventory")

# ---------- 4. Cost to serve: Agent-initiated calls (Apr-Jun) ----------
CALLS = [12131, 16136, 8773]
LBL   = ["12.1k", "16.1k", "8.8k"]
fig, ax = base_ax()
ax.fill_between(x, CALLS, color=GREEN, alpha=0.13, zorder=1)
ax.plot(x, CALLS, color=GREEN, lw=2.0, marker="o", ms=3.4, zorder=2)
for xi, yi, lb in zip(x, CALLS, LBL):
    dy = 6 if yi == max(CALLS) else (-11 if xi != len(x)-1 else -2)
    ha = "center" if xi != len(x)-1 else "left"
    off = (0, dy) if xi != len(x)-1 else (3, dy)
    ax.annotate(lb, (xi, yi), textcoords="offset points",
                xytext=off, fontsize=7.4, fontweight="bold", color=GREEN, ha=ha)
ax.set_ylim(0, max(CALLS)*1.22)
ax.text(0, 1.14, "Agent-initiated calls / month", transform=ax.transAxes,
        color=GREEN, fontsize=7, fontweight="bold")
save(fig, "row4_cost")

# ---------- 5. Ledger automation: new initiative ----------
fig, ax = plt.subplots(figsize=(3.25, 0.96), dpi=DPI)
ax.axis("off")
ax.add_patch(plt.Rectangle((0.03, 0.18), 0.94, 0.64, transform=ax.transAxes,
             fill=True, facecolor="#F1ECF9", edgecolor=PURPLE, lw=1.0))
ax.text(0.5, 0.62, "Kicked off  Jun'26", transform=ax.transAxes, ha="center",
        fontsize=8.6, fontweight="bold", color=PURPLE)
ax.text(0.5, 0.34, "Baseline metrics from Q3", transform=ax.transAxes, ha="center",
        fontsize=7.2, color="#6B7480")
save(fig, "row5_ledger")

print("charts written:", sorted(f for f in os.listdir(OUT) if f.endswith('.png')))
