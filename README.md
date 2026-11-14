# Project D — Who Drives AI-in-Education Research in Europe?

**Data Analytics · MDE-CO-02 · Fall 2026 · Constructor University**

## Research question (one sentence)

> **Which European institutions and venues drive research on AI in education since 2020, and do they form one collaboration community or several?**

## Team & roles

| Person | Role | Covers |
|---|---|---|
| Shifa Kayumbhai Bhari | Data Processing & Reproducibility | OpenAlex pull, cleaning, ISSN joins, ALL/STRICT layers, repo, README |
| Dev Charan | Descriptive Analysis | RQ1, RQ2 |
| Mabango Nyikuri | Search Validation & Limitations | RQ4 |
| Panchumarthi Keerthana | Collaboration Networks | RQ3 |
| Magaseng John Manchidi | Clustering & Interpretation | RQ3 |

## Research questions
1. Which institutions and venues dominate, and has that shifted since 2020?
2. How much does the picture change between the ALL layer and the Scopus-only STRICT layer?
3. What clusters exist — by topic, by collaboration, or simply by country?
4. What does the keyword search miss, and how would we know?

## Data sources
- **OpenAlex API** — free, no key. Works 2020+ with ≥1 EU-affiliated co-author, matching the AI-in-education query.
- **SCImago SJR** + **Scopus source list** — downloaded by hand, committed to `data/external/`, joined on ISSN.

Two layers: **ALL** (everything from OpenAlex) and **STRICT** (Scopus-listed sources only).

## Repository layout
```
├── data/{raw,external,processed}/   # raw pulls / hand-fetched lists / ALL+STRICT
├── notebooks/                       # counts, exploration, analysis
├── src/                             # pipeline code
└── docs/                            # guide, checklist, data dictionary, AI-use log
```

## Scope
> Default: **EU-27** (editable). Team to confirm EU-27 vs broader Europe (incl. UK/NO/CH).

## How to set up (Phase 0)
```bash
git clone https://github.com/shif10/Data-Analytics--project-D.git
cd Data-Analytics--project-D
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

See `docs/STEP_BY_STEP_GUIDE.md` for the full walkthrough.

Data-preparation notes and ALL/STRICT layer details: see `project-d/README_data_preparation.md`.

## Clustering and interpretation (RQ3)

- `docs/CLUSTERING_AND_INTERPRETATION.md`: method, topic clusters, manual review, sensitivity analysis, network comparison.
- `docs/INTERPRETATION.md`: answers to the four research questions and what would change the conclusion.
- `docs/figures/`: SVG figures.
- Scripts: `src/cluster_analysis_screened.py`, `src/cluster_analysis_strict_sensitivity.py`, `src/collaboration_analysis.py`, `src/cluster_network_crosswalk.py`.

Headline finding: collaboration forms several largely national or regional communities, and topic clusters cut across them.
