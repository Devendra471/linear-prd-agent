# TML / Board Review — Slide 1 update (Apr–Jun'26)

Slide 1 of `TML_Review__CM__AprMayJun_2026.pptx` was restructured so the same deck
serves both the **monthly TML review** and the **quarterly Board review**.

## What changed (slide 1 only; slide 2 untouched)

The single "MoM TREND / PROGRESS" block was split into a **4-column grid**, one row
per project:

| Column | Content |
|--------|---------|
| **PROJECT** | Objective + one-line approach |
| **DELIVERED · APR–JUN'26** | What shipped in the quarter (outcomes + metric deltas) |
| **TREND (JAN–JUN'26)** | Chart view — 6-month line per headline metric, Apr–Jun highlighted |
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

The DELIVERED and NEXT FOCUS content was carried and reorganized from the existing
deck plus the provided metrics. Linear was **not reachable in this session** (the
connector needs authorization), so the columns were not pulled live from delivered
stories / roadmap. Once Linear is authorized, these two columns can be enriched
directly from the shipped stories (Apr–Jun) and the planned roadmap (Jul–Aug).
