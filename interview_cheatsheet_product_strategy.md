# Product Strategy — Interview Cheat Sheet
### Initiative: "CM — Scale revenue 3.5× while cutting cost base 40%"
*Goal of this answer: prove long-term thinking + ability to build a yearly roadmap.*

---

## 1. Open with the equation (don't start with projects)

> "This is a **contribution-margin expansion** goal. I decompose it into the levers it actually depends on:"

```
REVENUE  =  Demand (loads)  ×  Fill rate  ×  Take rate
COST     =  Supply-acquisition cost  +  Fulfilment/ops cost  +  Leakage/support cost
```

> "Every project had to move one of those terms. Once it's an equation, the **sequence isn't a preference — it's dictated by which lever unlocks the next.**"

---

## 2. Prioritization principle (say this before the phases)

> **"Work the binding constraint in dependency order: Liquidity → Matching → Fulfilment.**
> Each is worthless without the one before it. You can't optimize matching with no demand,
> and you can't cut fulfilment cost until volume is flowing."

---

## 3. The phase table (the core of the answer)

| # | Phase | Projects | Lever it moves | Why it's here (the *why* matters most) |
|---|-------|----------|----------------|------------------------------------------|
| **1** | **Demand** *(top-up, not focus)* | Light demand top-up | ↑ Demand (loads) | Already ~70% solved. It's a **prerequisite** for everything else, so I guaranteed liquidity but **deliberately did NOT over-invest.** Knowing where *not* to spend is strategy. |
| **2** | **Supply** *(the core)* | • Inventory (truck availability)  • **FO Bidding / price discovery** | ↑ Fill rate (revenue) **and** ↓ Acquisition cost | **Only lever that moves revenue AND cost at once** → best ROI. FO bid must come *after* demand: a bid market only works with liquidity. |
| **3** | **Fulfilment** *(protect the margin)* | • Real-time payment visibility  • Detention auto-escalation  • Ticket deflection | ↓ Fulfilment + leakage/support cost | Comes **last on purpose.** At low volume the savings are tiny, and the process changes once volume scales 3.5×. You fix fulfilment *after* you scale, not before. |

---

## 4. Two moments to slow down on (your differentiators)

1. **"I touched demand but refused to over-invest — knowing where *not* to spend is strategy."**
2. **"Fulfilment is deliberately *last*, because it only pays off at scale — doing it first would optimize a process that's about to change."**

---

## 5. Close (the philosophy)

> "The roadmap isn't a ranked list of features — it's a **dependency chain where each phase unlocks and compounds the next**: demand creates liquidity → supply converts it efficiently and cheaply → fulfilment protects the margin. That's how I turn a 12–18 month financial target into a quarter-by-quarter roadmap. **Long-term thinking is sequencing for dependency and compounding — not shipping the highest-impact thing first.**"

---

## 6. Likely pushbacks + answers

| Interviewer asks | Your answer |
|------------------|-------------|
| "Why not parallelize the phases?" | Dependency + focus. FO bid literally can't function without demand liquidity; parallelizing would waste the supply effort. |
| "How did you prioritize within a phase?" | By which equation term it moves + a weighted score (Volume 40 / Frustration 30 / Ease 20 / Retention 10). |
| "What if you were wrong on sequence?" | Each phase has a measurable gate (e.g. fill rate %, cost-per-trip). I re-check the binding constraint each quarter and re-sequence. |
| "Where's the 40% cost cut come from?" | Mostly Phase 2 FO bidding (acquisition cost) + Phase 3 leakage/support deflection. |

---

### One-line mental model (memorize this)
> **Liquidity → Matching → Fulfilment.**
> Demand = prerequisite I topped up. Supply = core (moves revenue *and* cost). Fulfilment = last (only pays at scale).
