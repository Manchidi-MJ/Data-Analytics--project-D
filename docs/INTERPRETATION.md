# Interpretation (Phase 8)

Research question: *Which European institutions and venues drive research on
AI in education since 2020, and do they form one collaboration community or
several?*

Network numbers in the first paragraph come from Keerthana's main network
on all 7,594 candidates. The rest of this file uses the STRICT
likely-relevant sensitivity population (2,972 papers) unless stated
otherwise. Methods are in
`docs/CLUSTERING_AND_INTERPRETATION.md`. The topic-cluster vs network
comparison is produced by `src/cluster_network_crosswalk.py`.

## Short answer

No single institution or venue drives the field. Output is spread over many
institutions that collaborate mostly inside their own country or region, so
the evidence points to **several collaboration communities, not one**. Those
communities are defined by geography, not by research topic. The same topics
appear in every community.

## RQ3. One community or several? What do the topic clusters add?

**Several communities.** Keerthana's main network links 2,489 EU
institutions with 13,408 links. Louvain finds 17 communities (14 large,
modularity 0.59 against 0.50 for grouping by country), and 38% of link
weight crosses a national border. The French-led community is 90% French,
the German-led 75%, and the Dutch- and Finnish-led ones are mixed. Her
sensitivity runs keep 15 to 17 communities.

My cross-check on the reviewed STRICT set gives the same answer with finer
splits. That co-authorship network has 1,641 EU27
institutions, 7,557 edges and 168 connected components, and 139 institutions
have no EU27 collaborator at all. Louvain finds 46 communities among the
connected institutions (modularity 0.64). Sixteen of them hold 90+ papers
each and the rest are tiny fragments of a few papers.

**Most ties stay inside a community.** 71% of the 7,557 institution ties
(73% of co-authored papers on ties) connect two institutions in the same
community. Louvain is built to maximise this, so the figure shows that the
split is clear, not that it is a natural boundary. See
`docs/figures/collaboration_network_map.svg`.

**The communities are mostly national or regional.** Community 0 is 118 of
140 institutions French. Community 1 is 89 of 129 Italian. Community 4 is 68
of 119 Spanish. Community 7 is 56 of 89 Portuguese. Community 11 is 36 of 60
Greek. Across all communities, about half of the institutions (51%) belong to
the community's largest country. At paper level, 52% of papers fall in the most common country of their
network community (19% would be expected by chance with shuffled labels). The
19% for topic clusters is the same as chance, but the two partitions have
different sizes (5 groups vs 46), so compare them through the NMI below, not
through these percentages. A few communities mix several countries (for example 2, 6, 9 and
12), so country is a strong tendency, not a rule.

**Topic does not follow the network.** After placing each paper in a
community (2,772 of 2,972 papers could be placed; the other 200 only have
isolated institutions), agreement between topic cluster and network
community is close to zero (NMI 0.027, ARI 0.004). Shuffling the community
labels gives an NMI of 0.014, so the link is real but tiny. It is the same for
topic cluster vs country (NMI 0.028 against 0.009 shuffled). Network
community vs country is much higher (NMI 0.45 against 0.04 shuffled). See
`docs/figures/topic_cluster_vs_network_community.svg`: every community
contains all five topic groups. Proportions do vary (health papers are 24% of
community 2 and 6% of community 4, Cramer's V 0.17), but there is no
community built around one topic.
Generative AI / higher education (cluster 4) is the largest topic in most
communities, and broad foundations/reviews (cluster 0) leads in several
others (for example 1, 2, 11).

What this means: people collaborate with nearby partners, but they do not
specialise by topic. Generative AI in higher education, learning analytics
and tutoring systems are each being studied in France, Spain, Germany and
Greece at once, by groups that rarely co-author across borders. A country
view would say "Spain does generative AI and Finland does tutoring". The data
does not support that. Knowing a paper's topic tells you almost nothing about
which community or country produced it.

**Clustering vs country baseline.** Topic clusters score a cosine silhouette
of 0.013 against -0.012 for grouping by country. That is a small edge over
the baseline, but both values are near zero, so the clusters are weak,
overlapping groupings. The silhouette also barely changes with k (0.0087 at
k=10 to 0.0126 at k=5), so k=5 is a convenient choice, not a clearly better
one. Use them as descriptive themes, not as validated
categories. (Figures: `docs/figures/silhouette_topic_vs_country.svg`.)

## RQ1. Who dominates, and has it shifted since 2020?

**No dominant institution.** The most productive institution, the University
of Eastern Finland, appears in 46 of 2,972 papers (1.5%), followed by the
University of Oulu (41) and the Technical University of Munich (36). Nordic,
German and Iberian universities lead. CNRS and Inserm lead France, whose
output is spread over a large number of institutions.

**Venues are also spread out.** *Education Sciences* (81 papers),
*Frontiers in Education* (73) and *Applied Sciences* (66) lead, and the top
five venues together hold well under a fifth of the papers (about 11%,
329 of 2,972). Most outlets publish a handful of papers.

**Shift over time.** The field grew very fast: in the strict-sensitivity set
there are 438 papers in 2020-2022 and 2,248 in 2024-2026 (2026 is an
incomplete year). In 2020-2022 no institution had more than 13 papers (University
College Dublin, University of Eastern Finland, Inserm). In 2024-2026 the
leaders are Oulu (36), Eastern Finland (30), TU Munich (30), Complutense
Madrid (29), Nicosia (25) and CNRS (25). Eastern Finland stays near the top
throughout, and the other leaders change. Treat the early ranking with
caution because the counts are small.

## RQ2. How much does ALL vs STRICT change the picture?

STRICT keeps 3,668 of 7,594 candidates (48%). Its share of ALL is highest in
2021-2022 (56%) and falls to 46% in 2026, so recent growth is partly in
venues outside the Scopus list. Institution rankings change in
places: the University of Bonn (86 papers in ALL) and
Leibniz University Hannover (80) are in the ALL top ten but not among the top
eight STRICT-sensitivity institutions.

STRICT is not automatically cleaner. *Alzheimer's & Dementia* (43 records) is
the seventh venue in the provisional STRICT table, because the keyword screen
lets clinical machine-learning papers through and Scopus lists the journal.
My manual review of 125 records in the two health-heavy clusters found 123
out of scope, which is why the sensitivity analysis excludes them. Scopus
membership is a quality filter for the venue, not a relevance filter for the
paper.

## RQ4. What does the keyword search miss?

- Precision is about 80% (95% CI 70.6-86.7%) on a 100-paper audit, so
  roughly one capture in five is not really AI in education. The main error
  types are AI papers with no education link and health or patient
  education.
- Recall is about 21% (95% CI 15.9-27.2%) against 200 EU papers tagged
  AI-in-education by OpenAlex. English papers were found at 28%,
  non-English at 11%.
- The search misses papers that use terms such as ChatGPT, chatbot, LLM or
  GenAI without the phrases in the query.
- 26.5-37.4% of works lost their country, depending on which of the five
  searches is used (22-35% by year for the AI-in-education search), so
  country-based results rest on incomplete affiliation data.

## What would change the conclusion

- **Recall of about 21% is the biggest threat.** If the missing papers are
  mostly non-English, the national communities and the leaders in countries
  such as Spain, Poland and Germany could be understated. Our "several
  communities" result would likely hold, but the ranking could change.
- **Country-level fragmentation could be partly an artefact.** Louvain tends
  to split large sparse graphs, and a graph built from EU27 institutions
  only ignores collaboration with the UK, Switzerland, Norway and the US.
  Adding those partners could merge some communities. Check this with a
  broader Europe scope.
- **Text clusters are weak (silhouette about 0.01).** A different
  representation, such as OpenAlex concepts or sentence embeddings, could
  separate topics better. The finding that topics and network communities do
  not line up is therefore moderately robust, not certain.
- **Scope of "AI in education".** If AI-assisted patient education counts,
  part of the excluded health cluster comes back and the topic map changes.
- **The manual review was targeted.** It covered only two clusters, so other
  false positives remain. The exclusion share must not be quoted as an
  overall error rate.
