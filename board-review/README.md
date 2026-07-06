# TML / Board Review — Slide 1 update (Apr–Jun'26)

Slide 1 of `TML_Review__CM__AprMayJun_2026.pptx` was restructured so the same deck
serves both the **monthly TML review** and the **quarterly Board review**.

## What changed (slide 1 only; slide 2 untouched)

The single "MoM TREND / PROGRESS" block was split into a **4-column grid**, one row
per project:

| Column | Content |
|--------|---------|
| **PROJECT** | Objective + one-line approach |
| **DELIVERED · APR–JUN'26** | Product stories / features shipped in the quarter (named) |
| **METRICS & TREND (JAN–JUN'26)** | Metric deltas and the 6-month trend chart together, Apr–Jun highlighted |
| **NEXT FOCUS · JUL–AUG** | What's planned for the next two months |

The ledger-automation row (new initiative picked in June) is highlighted in amber.

## Trend charts

`charts/` holds the four trend charts (matplotlib), built from the monthly metrics
table for Jan–Jun'26. Design follows the data-viz method: single axis, colorblind-safe
palette, recessive pre-quarter segment, bold highlighted Apr–Jun segment with end-value
labels. The inventory chart shows the AI-vs-manual crossover.

- `c1_dau` — FO App DAU
- `c2_fulfil` — Placeable fulfilment %
- `c3_inv` — AI vs manual inventory created
- `c4_calls` — Calls initiated via agent

## Reproduce

```
python3 gen_charts.py   # regenerate charts/ from the metrics
python3 build.py        # rebuild slide 1 from source_deck.pptx -> deck_out.pptx
```

## Note on source data

The feature names in DELIVERED and the NEXT FOCUS items are **indicative** —
derived from the existing deck plus the provided metrics. Linear was **not reachable
in this session** (the connector needs authorization), so they were not pulled live
from delivered stories / roadmap. Once Linear is authorized, replace the feature
names with the actual shipped story titles (Apr–Jun) and align NEXT FOCUS with the
planned roadmap (Jul–Aug).
