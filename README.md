
Loading older messages…
<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>openalex_id</th>
      <th>title</th>
      <th>year</th>
      <th>institution_id</th>
      <th>institution</th>
      <th>country_code</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>https://openalex.org/W4304943299</td>
      <td>Ethical principles for artificial intelligence...</td>
      <td>2022</td>
      <td>https://openalex.org/I98381234</td>
      <td>University of Oulu</td>
      <td>FI</td>
    </tr>
    <tr>
      <th>5</th>
      <td>https://openalex.org/W3196708219</td>
      <td>Artificial Intelligence in Education</td>
      <td>2021</td>
      <td>https://openalex.org/I71999127</td>
      <td>Universitat de Barcelona</td>
      <td>ES</td>
    </tr>
    <tr>
      <th>7</th>
      <td>https://openalex.org/W3133611467</td>
      <td>Artificial Intelligence in Education</td>
      <td>2021</td>
      <td>https://openalex.org/I7876267</td>
      <td>Open University of the Netherlands</td>
      <td>NL</td>
    </tr>
    <tr>
      <th>9</th>
      <td>https://openalex.org/W4386634686</td>
      <td>Data-Driven Artificial Intelligence in Educati...</td>
      <td>2023</td>
      <td>https://openalex.org/I4210100923</td>
      <td>Munster Technological University</td>
      <td>IE</td>
    </tr>
    <tr>
      <th>20</th>
      <td>https://openalex.org/W2600942494</td>
      <td>Artificial Intelligence in Education</td>
      <td>2020</td>
      <td>https://openalex.org/I82767444</td>
      <td>Universidad de Málaga</td>
      <td>ES</td>
    </tr>
    <tr>
      <th>21</th>
      <td>https://openalex.org/W3145952927</td>
      <td>Artificial Intelligence and Education</td>
      <td>2020</td>
      <td>https://openalex.org/I166825849</td>
      <td>Tampere University</td>
      <td>FI</td>
    </tr>
    <tr>
      <th>22</th>
      <td>https://openalex.org/W3145952927</td>
      <td>Artificial Intelligence and Education</td>
      <td>2020</td>
      <td>https://openalex.org/I111112146</td>
      <td>Tallinn University of Technology</td>
      <td>EE</td>
    </tr>
    <tr>
      <th>23</th>
      <td>https://openalex.org/W3145952927</td>
      <td>Artificial Intelligence and Education</td>
      <td>2020</td>
      <td>https://openalex.org/I155660961</td>
      <td>University of Turku</td>
      <td>FI</td>
    </tr>
    <tr>
      <th>24</th>
      <td>https://openalex.org/W3145952927</td>
      <td>Artificial Intelligence and Education</td>
      <td>2020</td>
      <td>https://openalex.org/I95220073</td>
      <td>University of Lapland</td>
      <td>FI</td>
    </tr>
    <tr>
      <th>29</th>
      <td>https://openalex.org/W4381956096</td>
      <td>Artificial Intelligence in Education</td>
      <td>2023</td>
      <td>https://openalex.org/I178450904</td>
      <td>Universidad Nacional de Educación a Distancia</td>
      <td>ES</td>
    </tr>
  </tbody>
</table>
</div>
…
It looks like you pasted the previous eu_affiliations_df preview again. That's okay! We just need to run the institution summary cell now.

Step 1 — Run this code in a new Jupyter cell
institution_summary = (
    eu_affiliations_df
    .groupby(["institution_id", "institution", "country_code"])
    ["openalex_id"]
    .nunique()
    .reset_index(name="paper_count")
    .sort_values("paper_count", ascending=False)
)

summary_file = (
    project / "data" / "processed"
    / "eu_institution_paper_counts.csv"
)

institution_summary.to_csv(summary_file, index=False)

print("Unique EU institutions:", len(institution_summary))
print("Saved to:", summary_file)

display(institution_summary.head(15))

Step 2 — Check the output
You should see a table with these columns:

institution_id

institution

country_code

paper_count

This counts each paper once per institution, even if the same institution appears multiple times in the paper's authorship records.

Please send me the output from this new cell. Then we'll finish the final file checks and prepare your data handover checklist.

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>institution_id</th>
      <th>institution</th>
      <th>country_code</th>
      <th>paper_count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>349</th>
      <td>https://openalex.org/I175532246</td>
      <td>University of Eastern Finland</td>
      <td>FI</td>
      <td>96</td>
    </tr>
    <tr>
      <th>142</th>
      <td>https://openalex.org/I1294671590</td>
      <td>Centre National de la Recherche Scientifique</td>
      <td>FR</td>
      <td>93</td>
    </tr>
    <tr>
      <th>204</th>
      <td>https://openalex.org/I135140700</td>
      <td>University of Bonn</td>
      <td>DE</td>
      <td>86</td>
    </tr>
    <tr>
      <th>64</th>
      <td>https://openalex.org/I114112103</td>
      <td>Leibniz University Hannover</td>
      <td>DE</td>
      <td>80</td>
    </tr>
    <tr>
      <th>2308</th>
      <td>https://openalex.org/I62916508</td>
      <td>Technical University of Munich</td>
      <td>DE</td>
      <td>78</td>
    </tr>
    <tr>
      <th>2479</th>
      <td>https://openalex.org/I98381234</td>
      <td>University of Oulu</td>
      <td>FI</td>
      <td>74</td>
    </tr>
    <tr>
      <th>2378</th>
      <td>https://openalex.org/I8204097</td>
      <td>Ludwig-Maximilians-Universität München</td>
      <td>DE</td>
      <td>71</td>
    </tr>
    <tr>
      <th>5</th>
      <td>https://openalex.org/I100930933</td>
      <td>University College Dublin</td>
      <td>IE</td>
      <td>67</td>
    </tr>
    <tr>
      <th>383</th>
      <td>https://openalex.org/I184999862</td>
      <td>Universidad de Salamanca</td>
      <td>ES</td>
      <td>66</td>
    </tr>
    <tr>
      <th>2412</th>
      <td>https://openalex.org/I88491126</td>
      <td>Bucharest University of Economic Studies</td>
      <td>RO</td>
      <td>64</td>
    </tr>
    <tr>
      <th>1513</th>
      <td>https://openalex.org/I4210136150</td>
      <td>L3S Research Center</td>
      <td>DE</td>
      <td>64</td>
    </tr>
    <tr>
      <th>2377</th>
      <td>https://openalex.org/I8087733</td>
      <td>University of Tübingen</td>
      <td>DE</td>
      <td>63</td>
    </tr>
    <tr>
      <th>468</th>
      <td>https://openalex.org/I204337017</td>
      <td>Aarhus University</td>
      <td>DK</td>
      <td>61</td>
    </tr>
    <tr>
      <th>347</th>
      <td>https://openalex.org/I174878644</td>
      <td>University of Patras</td>
      <td>GR</td>
      <td>60</td>
    </tr>
    <tr>
      <th>187</th>
      <td>https://openalex.org/I133731052</td>
      <td>University of Helsinki</td>
      <td>FI</td>
      <td>58</td>
    </tr>
  </tbody>
</table>
</div>
…
Excellent! 🎉 Your institution summary is now working, and you've prepared another useful dataset for your team.

Your current top 5 institutions by paper count are:

Institution

Country

Papers

University of Eastern Finland

Finland

96

Centre National de la Recherche Scientifique

France

93

University of Bonn

Germany

86

Leibniz University Hannover

Germany

80

Technical University of Munich

Germany

78

These counts are based on your current candidate dataset, so they're preliminary rather than definitive rankings of AI-in-education research.

Next step — Final data-file check
Let's verify that your main prepared files exist and have sensible row counts before you hand them over.

Run this in a new Jupyter cell:

from pathlib import Path
import pandas as pd

processed_dir = project / "data" / "processed"

files_to_check = [
    "openalex_eu_candidates.csv",
    "openalex_relevance_screened.csv",
    "strict_scopus_provisional.csv",
    "all_vs_strict_by_year.csv",
    "publication_counts_by_country.csv",
    "paper_institution_affiliations.csv",
    "eu_paper_institution_affiliations.csv",
    "eu_institution_paper_counts.csv",
    "strict_quality_report.csv",
]

results = []

for filename in files_to_check:
    path = processed_dir / filename

    if path.exists():
        try:
            df = pd.read_csv(path)
            results.append({
                "file": filename,
                "status": "Found",
                "rows": len(df),
                "columns": len(df.columns)
            })
        except Exception as e:
            results.append({
                "file": filename,
                "status": f"Read error: {e}",
                "rows": None,
                "columns": None
            })
    else:
        results.append({
            "file": filename,
            "status": "Missing",
            "rows": None,
            "columns": None
        })

file_check = pd.DataFrame(results)
display(file_check)

This checks the files without changing them.

After you send me the output, we'll organize the final handover. We'll also identify any files that need a clearer name or a note explaining their limitations. Your STRICT file will remain labelled provisional until its definition is fully verified.

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>file</th>
      <th>status</th>
      <th>rows</th>
      <th>columns</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>openalex_eu_candidates.csv</td>
      <td>Found</td>
      <td>7594</td>
      <td>7</td>
    </tr>
    <tr>
      <th>1</th>
      <td>openalex_relevance_screened.csv</td>
      <td>Found</td>
      <td>7594</td>
      <td>9</td>
    </tr>
    <tr>
      <th>2</th>
      <td>strict_scopus_provisional.csv</td>
      <td>Found</td>
      <td>3668</td>
      <td>17</td>
    </tr>
    <tr>
      <th>3</th>
      <td>all_vs_strict_by_year.csv</td>
      <td>Found</td>
      <td>7</td>
      <td>3</td>
    </tr>
    <tr>
      <th>4</th>
      <td>publication_counts_by_country.csv</td>
      <td>Found</td>
      <td>27</td>
      <td>2</td>
    </tr>
    <tr>
      <th>5</th>
      <td>paper_institution_affiliations.csv</td>
      <td>Found</td>
      <td>21236</td>
      <td>6</td>
    </tr>
    <tr>
      <th>6</th>
      <td>eu_paper_institution_affiliations.csv</td>
      <td>Found</td>
      <td>13879</td>
      <td>6</td>
    </tr>
    <tr>
      <th>7</th>
      <td>eu_institution_paper_counts.csv</td>
      <td>Found</td>
      <td>2489</td>
      <td>4</td>
    </tr>
    <tr>
      <th>8</th>
      <td>strict_quality_report.csv</td>
      <td>Found</td>
      <td>8</td>
      <td>2</td>
    </tr>
  </tbody>
</table>
</div>
…
Great! ✅ All 9 files are present, and your data-preparation outputs are saved. You have completed the main preparation work for Project D.

1. Final file check
Output

Rows

Status

EU candidate papers

7,594

Ready

Relevance-screened papers

7,594

Ready, preliminary screening

Provisional STRICT Scopus dataset

3,668

Saved; matching rules need confirmation

ALL vs. STRICT by year

7

Ready

Country publication counts

27

Ready

All paper–institution affiliations

21,236

Ready

EU paper–institution affiliations

13,879

Ready

EU institution publication counts

2,489

Ready

STRICT quality report

8 checks

Ready

2. What you should do next
Since your responsibility is data preparation, I recommend these final steps rather than starting more analysis.

Keep the original raw data unchanged. It lets you reproduce your preparation process.

Document the limitations.

The relevance screening is preliminary, and the manual audit is incomplete.

The STRICT dataset is provisional until the team confirms the Scopus inclusion rules.

The 2026 publication count covers an incomplete year.

One STRICT record has a missing title; keep it documented rather than inventing a title.

Share the prepared files and a short README with your team. Explain what each file contains and how it was produced.

3. One important recommendation
Do not describe all 7,594 papers as confirmed relevant AI-in-education papers. They are currently EU-affiliated candidate papers, with preliminary relevance screening. Similarly, call the 3,668-paper dataset provisional STRICT until the Scopus matching rules are confirmed.

Your preparation is in a good state. You do not need to redo these steps just because the validation is incomplete.

Would you like me to create a ready-to-use README file for your project folder that documents the datasets, preparation steps, quality checks, and limitations?

okay but what idid i just did whay you said and how i explain to my team
You did more than just check files! 😊 Let me explain in simple words what you actually did, why you did it, and how you can explain it to your team.

You do not need to explain every line of Python code. You need to understand the purpose of each step.

1. What did you actually do?
Your project investigates who drives AI-in-education research in Europe. To answer that question, the team needs a dataset of research papers that can be analysed.

Think of your work as preparing a messy collection of research papers so that the team can use it.

Step 1 — Collected research papers

You gathered papers from OpenAlex using five different search queries related to AI in education, intelligent tutoring systems, machine learning in education, and generative AI in education.

Result: 75,126 records collected across searches.

Step 2 — Removed duplicate records

The same paper could appear in multiple search results. You combined the records and kept one record per OpenAlex paper ID.

Result: 67,684 unique records; 7,442 duplicates removed.

Step 3 — Identified papers with EU affiliations

You used author affiliation information to identify papers associated with institutions in EU countries.

Result: 7,594 EU-affiliated candidate papers.

Step 4 — Prepared relevance screening

You created a preliminary screening dataset using title and abstract keyword checks to help distinguish likely relevant papers from records that need checking.

Result: 7,594 records with screening information. This is not a fully validated final dataset.

Step 5 — Compared with the Scopus source list

You matched publication venues using ISSN identifiers and checked whether the source's coverage included the paper's publication year.

Result: 3,668 records in a provisional STRICT dataset. The team still needs to confirm the exact inclusion rules.

Step 6 — Prepared institution and country data

You extracted institutional affiliations and created tables counting papers by institution and EU country. These will help the team study which institutions and countries contribute to the research.

Result: 2,489 institution-level summary rows and supporting affiliation tables.

Step 7 — Checked data quality

You checked whether important files existed and inspected basic quality issues, including duplicate IDs, missing titles, missing DOIs, and Scopus coverage status.

Result: your nine main output files are present.

2. What should you tell your team?
You can send this message. It explains your contribution honestly without claiming that the entire research analysis is finished.

Hi team, I have completed the main data-preparation steps for my part of Project D.

I collected the OpenAlex records using five search queries, combined the results, and removed duplicates. The combined dataset contains 67,684 unique records.

I then identified 7,594 candidate papers with EU affiliations and created a preliminary relevance-screening dataset. I also matched the EU candidates against the Scopus source list using ISSNs and publication-year coverage, producing a provisional STRICT dataset of 3,668 records.

Additionally, I prepared country-level publication counts, paper–institution affiliation tables, institution-level paper counts, and a basic data-quality report. The processed files are saved in the project’s data/processed folder.

A few limitations remain: relevance validation is incomplete, the STRICT inclusion rules should be confirmed with the team, and the 2026 publication counts represent an incomplete year. I have kept the STRICT dataset labelled provisional for now.

Please let me know if we should adjust the STRICT definition or the screening criteria before using these datasets for the final analysis.

3. If your professor or teammate asks, “What exactly was your contribution?”
You can answer in one sentence:

“My contribution was data acquisition and preparation: I collected and deduplicated OpenAlex records, identified EU-affiliated candidates, prepared preliminary relevance screening, matched publication venues against the Scopus source list, extracted institution and country information, and checked the resulting datasets for basic quality issues.”

4. What is still your responsibility?
Your main data-preparation outputs exist, but there are two things to be transparent about:

Relevance validation: You have not completed the manual review of the random sample, so you cannot yet claim that the search strategy has been fully validated.

STRICT definition: Your 3,668 records are provisional until the team confirms the exact Scopus inclusion rules.

You do not have to complete your teammates' clustering, collaboration-network analysis, or final interpretation just to explain your contribution. Those are separate analytical tasks unless your team assigns them to you.

My advice: Send the team message above and share the data/processed files. That gives everyone a clear account of what you prepared and what still needs agreement.

but what is my data  which one is my data? to use?
Your actual data is the CSV files inside data/processed in your Project D folder. You don't need to use all nine files for every task. Each file has a different purpose.

1. Which data should you use?
Here is your guide to the most important files.

1. openalex_eu_candidates.csv

Main dataset
7,594 rows · 7 columns

This is your main table of candidate research papers with EU affiliations. It contains titles, years, publication types, DOIs and EU country information.

Use it when: your team needs the basic paper dataset for further filtering and analysis.

2. openalex_relevance_screened.csv

7,594 rows · 9 columns

This is the same candidate collection with additional preliminary relevance-screening information.

Use it when: your team wants to examine which records are likely relevant and which need checking. Don't treat the screening as fully validated.

3. strict_scopus_provisional.csv

3,668 rows · 17 columns

This contains candidate papers whose matched Scopus source coverage includes the publication year, according to your current rules.

Use it when: comparing the broader collection with the provisional Scopus-indexed collection. Confirm the project’s STRICT definition with your team first.

4. eu_institution_paper_counts.csv

2,489 rows · 4 columns

A summary of the number of candidate papers associated with each EU institution.

Use it when: identifying institutions that publish many papers in your collected dataset.

5. eu_paper_institution_affiliations.csv

13,879 rows · 6 columns

Links individual papers to their EU institutions.

Use it when: building institution collaboration networks or examining which institutions appear together on papers.

2. What about the other files?
File

Purpose

all_vs_strict_by_year.csv

Compare ALL and provisional STRICT paper counts by year

publication_counts_by_country.csv

Summarise candidate paper counts by EU country

paper_institution_affiliations.csv

Institution affiliations from the broader candidate collection, including non-EU institutions

strict_quality_report.csv

Basic quality checks for the provisional STRICT dataset

3. Which one should you open first?
Start with openalex_eu_candidates.csv. It is your main paper-level dataset. Open it in Excel or load it in Python.

For example, in your Jupyter notebook:

import pandas as pd
from pathlib import Path

file_path = project / "data" / "processed" / "openalex_eu_candidates.csv"
df = pd.read_csv(file_path)

print("Number of papers:", len(df))
print("Columns:", df.columns.tolist())

display(df.head())

This lets you see the actual rows and columns you collected.

Important: Your data is not just one file. It is a small collection of related datasets: one contains papers, another adds screening information, another represents the provisional Scopus subset, and others summarise countries and institutions.

If your team asks, “Which dataset should we analyse?”, say: “The main dataset is openalex_eu_candidates.csv; openalex_relevance_screened.csv adds preliminary screening, and strict_scopus_provisional.csv is the provisional Scopus subset.”

can u cretae readme to undratsand

I created a README for your Project D that explains what your data is, which CSV file to use, how you prepared it, and how to explain your contribution to your team.

Download README_data_preparation.md

What you'll find inside
A simple explanation of all 9 processed CSV files.

Your data-preparation steps, from OpenAlex collection to deduplication and EU affiliation filtering.

The meaning of your 7,594 candidate papers and 3,668 provisional STRICT records.

Data-quality checks and limitations.

Python code to open your main dataset.

A short explanation you can share with your team.

What to do next
Download the README.

Place it in your project-d folder, alongside your project files.

Open it in VS Code.

Share it with your team along with the data/processed folder.

Remember: Your main dataset is openalex_eu_candidates.csv. Start there when you want to see the actual research-paper records. The README explains when to use the other files.


README_data_preparation.md
Document
Project D — Data Preparation README
1. What is this folder?
This folder contains prepared research-paper data for Project D:

“Who drives AI-in-education research in Europe?”

The goal of this part of the project is to collect candidate research papers, remove duplicates, identify papers with EU affiliations, prepare preliminary relevance screening, compare publication venues with the Scopus source list, and prepare country/institution tables for later analysis.

Important: These datasets are prepared for further analysis. They are not all fully validated final results. Please read the limitations in Section 5 before using them.

2. Which file should I use?
Start with openalex_eu_candidates.csv if you need the main table of candidate papers.

File	What it contains	When to use it
openalex_eu_candidates.csv	7,594 candidate papers with EU affiliations; includes OpenAlex ID, title, year, type, DOI and EU country information	Main paper-level dataset for further filtering and analysis
openalex_relevance_screened.csv	The same 7,594 candidate papers with extra preliminary relevance-screening fields	To review likely relevant papers and papers that need checking
strict_scopus_provisional.csv	3,668 records whose matched Scopus source coverage includes the paper's publication year under the current matching rules	Provisional STRICT comparison only; confirm the project definition first
all_vs_strict_by_year.csv	Counts by year for the broad candidate dataset and provisional STRICT dataset	To compare yearly counts
publication_counts_by_country.csv	Candidate-paper counts by EU country	To summarise country-level representation
paper_institution_affiliations.csv	Paper-to-institution affiliation links, including institutions outside the EU	For broader affiliation and collaboration work
eu_paper_institution_affiliations.csv	Paper-to-institution links filtered to EU-27 institutions	For EU institution collaboration/network work
eu_institution_paper_counts.csv	One summary row per EU institution with its candidate-paper count	To identify institutions with many candidate papers
strict_quality_report.csv	Basic quality-check results for the provisional STRICT dataset	To report data-quality checks and limitations
The row counts above describe the files at the time this README was created. If you rerun the data-preparation notebook, counts may change.

3. How the data was prepared
Step 1 — Search OpenAlex
Five search queries were used to collect records about:

“artificial intelligence in education”
“AI in education”
“intelligent tutoring system”
“machine learning” and education
“generative AI” and education
The searches returned 75,126 records across the five searches. Because the same paper can appear in multiple searches, this was not the number of unique papers.

Step 2 — Combine and deduplicate
The search results were combined and duplicate records were removed using OpenAlex paper IDs.

Records collected across searches: 75,126
Unique records after deduplication: 67,684
Duplicate records removed: 7,442
Records with missing OpenAlex IDs in the deduplicated result: 0
Step 3 — Identify EU-affiliated candidates
Author affiliation information was used to identify records associated with institutions in EU member states.

EU-affiliated candidate papers: 7,594
These are candidate papers, not a fully confirmed set of relevant AI-in-education papers.

Step 4 — Prepare preliminary relevance screening
A screening file was created using available titles and reconstructed abstracts/keyword checks to help flag likely relevant records and records that need checking.

This is a preliminary screening step. It can produce false positives and false negatives and should not be described as full manual validation.

Step 5 — Compare against the Scopus source list
Publication venues were matched against the downloaded September 2026 Scopus source list using ISSN/eISSN identifiers and publication-year coverage.

EU-affiliated candidates: 7,594
Candidates with a Scopus source match: 3,722
Provisional STRICT records with a matched source whose coverage includes the publication year: 3,668
The STRICT dataset is labelled provisional because the team must confirm the exact inclusion rules required by the project. Source matching and coverage checks do not by themselves guarantee that every record meets the final project definition.

Step 6 — Prepare country and institution tables
Institution information was extracted from OpenAlex authorship affiliations. Separate files were created for paper–institution links, EU-only paper–institution links, institution-level counts, and country counts. These can support later descriptive analysis and collaboration-network analysis.

Step 7 — Perform basic quality checks
The provisional STRICT dataset was checked for duplicate/missing OpenAlex IDs, missing titles, missing years, missing DOIs, and Scopus-match/coverage status.

The quality report found:

3,668 rows
0 duplicate OpenAlex IDs
0 missing OpenAlex IDs
1 missing title
0 missing years
21 missing DOIs
A missing DOI does not automatically mean a record is invalid if it has a valid OpenAlex ID. The record with a missing title should be documented rather than assigned an invented title.

4. Folder structure
The relevant files are expected in these locations:

project-d/
├── data/
│   ├── raw/
│   │   ├── openalex/       # Original OpenAlex search results and combined raw data
│   │   └── sources/        # Downloaded Scopus source list
│   └── processed/          # Prepared CSV files listed above
└── README_data_preparation.md
Keep raw data unchanged where possible so the preparation steps can be reproduced. Processed files are outputs intended for review and analysis.

5. Limitations and cautions
Candidate papers are not all confirmed relevant. The 7,594-paper collection is based on search results and EU affiliations. Keyword screening is preliminary.
Manual relevance audit is incomplete. A random sample was created, but not all sampled records were labelled. Therefore, do not claim that the search strategy has been fully validated.
STRICT is provisional. The 3,668 records use the current ISSN/eISSN matching and source-coverage logic. Confirm the project's required STRICT definition with the team before treating it as final.
The year 2026 is incomplete. Avoid comparing 2026 directly with full publication years without noting this.
Country counts can overlap. A paper with affiliations in multiple EU countries can contribute to multiple country counts. Country counts therefore should not be summed as if each paper belonged to exactly one country.
Institution counts are candidate-dataset counts. They may include papers that have not yet passed final relevance validation.
One STRICT record has no title in the original OpenAlex record. Keep it documented; do not invent a title or automatically remove it without an agreed rule.
6. Example: load the main dataset in Python
Run this in the project notebook, where project is already set to the project folder:

import pandas as pd

file_path = project / "data" / "processed" / "openalex_eu_candidates.csv"
df = pd.read_csv(file_path)

print("Number of rows:", len(df))
print("Columns:", df.columns.tolist())
display(df.head())
If the project variable is not defined, set it to your project directory first:

from pathlib import Path

project = Path(r"C:\Users\Aftab bloch\Documents\project\Data-Analytics--project-D\project-d")
7. Short explanation for the team
“My part focused on data preparation. I collected OpenAlex records using five search queries, deduplicated the results, identified EU-affiliated candidate papers, created preliminary relevance-screening fields, matched publication venues against the Scopus source list, and prepared country and institution affiliation tables. The main candidate dataset has 7,594 records, and the provisional STRICT dataset has 3,668 records. Relevance validation is incomplete and the STRICT definition still needs confirmation, so I have documented those limitations.”

8. Suggested next steps for the team
Agree on the final definition of the ALL and STRICT datasets.
Decide how to handle the incomplete manual relevance audit.
Use the prepared datasets for the assigned descriptive, institution, country, and collaboration analyses.
Record any further filtering decisions in the project documentation.


15⋮⋮⋮⋮



