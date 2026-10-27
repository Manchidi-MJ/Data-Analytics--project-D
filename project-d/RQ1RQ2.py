from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

# ---- 1. Set your project folder ----
PROJECT = Path(r"C:\Users\Aftab bloch\Documents\project\Data-Analytics--project-D\project-d")
P = PROJECT / "data" / "processed"
OUT = P / "deliverables"
OUT.mkdir(exist_ok=True)

# ---- 2. Load data ----
inst = pd.read_csv(P / "eu_institution_paper_counts.csv")
ctry = pd.read_csv(P / "publication_counts_by_country.csv")
year = pd.read_csv(P / "all_vs_strict_by_year.csv")
strict = pd.read_csv(P / "strict_scopus_provisional.csv")
screened = pd.read_csv(P / "openalex_relevance_screened.csv")
aff = pd.read_csv(P / "eu_paper_institution_affiliations.csv")

N_ALL, N_STRICT = int(year.ALL_candidates.sum()), int(year.STRICT_provisional.sum())

# ---- 3. RQ1: institutions, countries, venues ----
top_inst = inst.sort_values("paper_count", ascending=False).head(10)
top_ctry = ctry.sort_values("paper_count", ascending=False).head(10)

# Venue names exist only in the STRICT file, so venue results describe STRICT only
venues_all = strict.venue.value_counts()
top_venues = venues_all.head(10).rename_axis("venue").reset_index(name="records")
top_journals = (strict[strict.openalex_source_type == "journal"].venue.value_counts()
                .head(10).rename_axis("venue").reset_index(name="records"))

# Sensitivity check: only papers flagged "Likely relevant"
likely_ids = set(screened.loc[screened.automated_relevance_flag == "Likely relevant", "openalex_id"])
top_inst_likely = (aff[aff.openalex_id.isin(likely_ids)]
                   .groupby(["institution", "country_code"]).openalex_id.nunique()
                   .sort_values(ascending=False).head(10).reset_index(name="paper_count"))

# ---- 4. RQ2: yearly trend and STRICT share ----
year = year.sort_values("year").copy()
year["strict_share_pct"] = (year.STRICT_provisional / year.ALL_candidates * 100).round(1)
year["all_growth_pct"] = (year.ALL_candidates.pct_change() * 100).round(1)

# ---- 5. Show and save tables ----
tables = {"top_institutions": top_inst, "top_countries": top_ctry,
          "top_venues_strict": top_venues, "top_journals_strict": top_journals,
          "top_institutions_likely_relevant": top_inst_likely,
          "yearly_all_vs_strict": year}
for name, d in tables.items():
    d.to_csv(OUT / f"{name}.csv", index=False)
    print(f"\n== {name} ==")
    display(d)

# ---- 6. Figures ----
def barh(df, x, y, title, fn):
    fig, ax = plt.subplots(figsize=(10, 6))
    d = df.iloc[::-1]
    ax.barh(d[y], d[x], color="#2C6E63")
    ax.set(title=title, xlabel="Papers")
    for i, v in enumerate(d[x]):
        ax.text(v, i, f" {v}", va="center", fontsize=9)
    fig.tight_layout()
    fig.savefig(OUT / fn, dpi=200)
    plt.show()

barh(top_inst, "paper_count", "institution", "Top 10 EU institutions (candidate papers)", "fig_institutions.png")
barh(top_ctry, "paper_count", "country", "Top 10 EU countries (full counting)", "fig_countries.png")
barh(top_journals, "records", "venue", "Top 10 journals in provisional STRICT set", "fig_journals.png")

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(year.year, year.ALL_candidates, marker="o", label="ALL candidates", color="#2C6E63")
ax.plot(year.year, year.STRICT_provisional, marker="s", label="STRICT (provisional)", color="#D1603D")
ax.axvline(2026, ls="--", color="gray")
ax.text(2026, ax.get_ylim()[1] * .95, "2026 partial", ha="right", color="gray")
ax.set(title="Yearly publications: ALL vs STRICT", xlabel="Year", ylabel="Papers")
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "fig_yearly.png", dpi=200)
plt.show()

fig, ax = plt.subplots(figsize=(10, 4))
ax.bar(year.year.astype(str), year.strict_share_pct, color="#D1603D")
ax.set(title="Share of ALL records kept in STRICT", ylabel="%")
fig.tight_layout()
fig.savefig(OUT / "fig_strict_share.png", dpi=200)
plt.show()

# ---- 7. Key facts ----
print(f"\nALL={N_ALL:,}  STRICT={N_STRICT:,}  retained={N_STRICT/N_ALL:.1%}")
print(f"Country counts sum to {ctry.paper_count.sum():,} (more than {N_ALL:,} papers, so full counting)")
print(f"Institutions: {len(inst):,}; median papers = {inst.paper_count.median():.0f}; with 10+ papers: {(inst.paper_count>=10).sum()}")
print(f"STRICT venues: {venues_all.size:,}; top-10 share = {venues_all.head(10).sum()/len(strict):.1%}")
print("\nRelevance flags:")
print(screened.automated_relevance_flag.value_counts().to_string())
print("\nSaved tables and figures to:", OUT)