# AI-use log

Declared AI use for Project D. Each member should add their own entries.
Shifa owns this file (guide, Step 9.3).

| Field | Meaning |
|---|---|
| Who | Team member who ran the session |
| Tool / model | Assistant and model, as reported by the tool |
| Task | What it was asked to do |
| What we kept or changed | What the human reviewed, corrected or rejected |

## John (Clustering and interpretation)

| Date | Tool / model | Task | What we kept or changed |
|---|---|---|---|
| 2026-11-14 | Kiro (web agent), model chosen automatically by the service; exact model name not shown | Review repository against the project guide and list gaps | Used the gap list to plan the remaining work |
| 2026-11-14 | Kiro, same | Write `src/cluster_network_crosswalk.py` and `src/network_map.py` (standard library only), generate SVG figures and crosswalk CSVs | Outputs come from committed CSVs. John should re-run both scripts and check the figures render correctly |
| 2026-11-14 | Kiro, same | Draft `docs/INTERPRETATION.md`, `docs/REPORT.md` and slides for RQ3, RQ4 and the conclusions | Numbers for RQ1, RQ2 and RQ4 were read from Dev's and Mabango's files. The text is a draft that John, Dev and Mabango must check and rewrite in their own words |
| 2026-11-14 | Kiro, same | Change `src/` scripts to read project CSVs from the working tree and fix the review-file path | Not re-run: the environment lacked pandas, scikit-learn and the local JSONL file. Run them before submitting |

Effort and cost: one working session. The tool does not report token cost.

## Shifa (Data processing)

_To be filled in by Shifa._

## Dev (Descriptive analysis, slides)

_To be filled in by Dev._

## Mabango (Search validation)

_To be filled in by Mabango._

## Keerthana (Collaboration networks)

_To be filled in by Keerthana._
