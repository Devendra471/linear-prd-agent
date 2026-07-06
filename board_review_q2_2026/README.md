# Carrier Matching — Q2 (Apr–Jun'26) Board + Monthly TML Review

Updated Slide 1 of `TML_Review (CM) AprMayJun 2026` for dual use: the **quarterly Board
review** and the **monthly TML review**. The slide was restructured from 3 columns into 4:

| Column | Content |
|--------|---------|
| **PROJECT / GOAL** | Initiative + the OKR it ladders to |
| **APR–JUN DELIVERY** | Work shipped & outcomes this quarter (green = headline wins) |
| **TREND (Jan–Jun'26)** | Chart view built from the metrics table (`make_charts.py`) |
| **NEXT FOCUS (Jul–Aug)** | What's planned for the next 2 months |

## Trend charts (chart view)
Built from the Jan–Jun'26 metrics with matplotlib, one mini-chart per project:
- **FO App** — MAU / WAU / DAU adoption lines
- **Demand fulfilment** — Bids placed (bars) + Placeable fulfilment % (line); June rebound
- **Inventory** — AI-agent vs Manual inventory (stacked) — AI now dominant
- **Cost to serve** — Agent-initiated calls/month (scaled to 16k)
- **Ledger** — new initiative, kicked off Jun'26 (baseline from Q3)

## ⚠️ Linear data caveat
Delivery and Next-Focus copy was **carried forward from the existing deck and refreshed
against the Jun'26 metrics**. Linear was **not authorised in this session** (OAuth can't run
non-interactively), so the roadmap / delivered-story detail could not be pulled live. Once
the Linear connector is authorised, refresh the Delivery bullets (delivered stories) and the
Next-Focus bullets (roadmap / planned stories) directly from Linear.

## Reproduce
```
python3 make_charts.py     # regenerates charts/
python3 build_slide.py     # needs the source deck as deck.pptx -> writes deck_out.pptx
```
Numbers live in `make_charts.py` (charts) and `build_slide.py` (`rows`).
