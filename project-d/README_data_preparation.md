# Project D: Data Preparation README

**Author / role:** [name and role from the work plan]

Project question: *Who drives AI-in-education research in Europe?*

This document describes how the research-paper data was collected and prepared, which files exist, and what limitations apply. The analysis built on these files is described in `README_descriptive_analysis.md`.

**Important:** these datasets are prepared for further analysis. They are not fully validated final results. Read the limitations in Section 5 before using them.

## 1. Which file should I use?

Start with `openalex_eu_candidates.csv` for the main table of candidate papers. All files are in `project-d/data/processed/`.

| File | Contents | When to use it |
|---|---|---|
| `openalex_eu_candidates.csv` | 7,594 candidate papers with EU affiliations: OpenAlex ID, title, year, type, DOI, EU countries | Main paper-level dataset |
| `openalex_relevance_screened.csv` | The same 7,594 papers plus abstract and a preliminary automated relevance flag | Reviewing likely relevant papers and papers that need checking |
| `strict_scopus_provisional.csv` | 3,668 records whose matched Scopus source covers the publication year, with venue and Scopus match fields | Provisional STRICT comparison only; confirm the definition first |
| `all_vs_strict_by_year.csv` | Yearly counts for ALL (candidates) and provisional STRICT | Comparing ALL and STRICT by year |
| `publication_counts_by_country.csv` | Candidate-paper counts by EU country (27 rows) | Country-level summary |
| `paper_institution_affiliations.csv` | Paper-to-institution links, including non-EU institutions (21,236 rows) | Broader affiliation and collaboration work |
| `eu_paper_institution_affiliations.csv` | Paper-to-institution links filtered to EU institutions (13,879 rows) | EU institution collaboration networks |
| `eu_institution_paper_counts.csv` | One row per EU institution with its candidate-paper count (2,489 rows) | Institution ranking |
| `strict_quality_report.csv` | Basic quality checks for the provisional STRICT set | Reporting data quality and limitations |

Other files in the folder (for example `openalex_deduplicated.csv`, `openalex_scopus_matched.csv`, `openalex_scopus_coverage_checked.csv`, `search_rules.csv`, `search_strategy_comparison.csv`, audit samples and `publication_counts_by_year.csv` / `_by_type.csv`) are intermediate or supporting outputs from the preparation steps.

Row counts describe the files at the time this README was written and may change if the preparation notebook is rerun.

## 2. How the data was prepared

**Step 1: Search OpenAlex.** Five search queries were used: "artificial intelligence in education", "AI in education", "intelligent tutoring system", "machine learning" and education, and "generative AI" and education. They returned 75,126 records in total. This is not the number of unique papers, because the same paper can appear in several searches.

**Step 2: Combine and deduplicate.** Results were combined and duplicates removed by OpenAlex paper ID: 67,684 unique records remained (7,442 duplicates removed, 0 missing IDs).

**Step 3: Identify EU-affiliated candidates.** Author affiliation information was used to keep records associated with institutions in EU member states: 7,594 candidate papers. These are candidates, not a confirmed set of relevant AI-in-education papers.

**Step 4: Preliminary relevance screening.** A keyword check on titles and reconstructed abstracts flags records as "Likely relevant" (6,442) or "Needs checking" (1,152). This is a preliminary step that can produce false positives and false negatives. It is not manual validation.

**Step 5: Compare against the Scopus source list.** Publication venues were matched to the downloaded September 2026 Scopus source list by ISSN/eISSN and publication-year coverage. 3,722 candidates had a Scopus source match, and 3,668 had coverage for the publication year. These 3,668 form the provisional STRICT set.

**Step 6: Country and institution tables.** Institution information was extracted from OpenAlex authorship affiliations. Separate files hold paper-institution links, EU-only links, institution counts and country counts.

**Step 7: Basic quality checks.** The STRICT set was checked for duplicate or missing IDs, titles, years and DOIs, and for Scopus match and coverage status. Result for 3,668 rows: 0 duplicate IDs, 0 missing IDs, 1 missing title, 0 missing years, 21 missing DOIs.

## 3. Folder structure

```
project-d/
├── data/
│   ├── raw/
│   │   ├── openalex/     # original OpenAlex search results and test samples
│   │   └── sources/      # downloaded Scopus source list
│   └── processed/        # prepared CSV files listed above
├── README_data_preparation.md
└── README_descriptive_analysis.md
```

Keep raw data unchanged so the preparation steps can be reproduced.

## 4. Load the main dataset in Python

```python
import pandas as pd
from pathlib import Path

project = Path(r"path\to\project-d")   # set to your local project-d folder
df = pd.read_csv(project / "data" / "processed" / "openalex_eu_candidates.csv")
print(len(df), df.columns.tolist())
df.head()
```

## 5. Limitations

- **Candidates are not confirmed relevant.** The 7,594 papers come from search results and EU affiliation, not from manual review.
- **Relevance validation is incomplete.** A random audit sample was created but not fully labelled, so the search strategy has not been fully validated. The keyword screen is weak: for example, *Alzheimer's & Dementia* records appear in the STRICT set and are flagged "Likely relevant".
- **STRICT is provisional.** The 3,668 records use the current ISSN/eISSN matching and coverage logic. Confirm the project's required STRICT definition before treating it as final.
- **2026 is an incomplete year.** Do not compare it directly with full years without noting this.
- **Country counts overlap.** A paper with authors in several EU countries counts for each, so country counts sum to 9,050 and should not be treated as a partition of the 7,594 papers.
- **Institution counts** come from the candidate dataset and may include papers that would not pass final relevance validation.
- **One STRICT record has no title** in the original OpenAlex record. Keep it documented; do not invent a title or remove it without an agreed rule.

## 6. Short explanation for the team

> My part covered data preparation. I collected OpenAlex records with five search queries, deduplicated them (67,684 unique), identified 7,594 EU-affiliated candidate papers, added preliminary relevance screening, matched venues against the Scopus source list to build a provisional STRICT set of 3,668 records, and prepared country and institution tables. Relevance validation is incomplete and the STRICT definition still needs confirmation, so both are documented as limitations.

## 7. Suggested next steps

1. Agree on the final definitions of ALL and STRICT.
2. Decide how to handle the incomplete manual relevance audit.
3. Use the prepared files for the descriptive, institution, country and collaboration analyses.
4. Record any further filtering decisions in the project documentation.
