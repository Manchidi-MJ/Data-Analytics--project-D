"""Compare topic clusters with institutional network communities (RQ3).

Standard library only, so it runs without the pandas/matplotlib stack.

Inputs (all produced by the earlier clustering/collaboration scripts):
  - data/processed/clustering/strict_only_sensitivity/cluster_assignments.csv
  - data/processed/clustering/strict_only_sensitivity/cluster_summary.csv
  - data/processed/clustering/strict_only_sensitivity/baseline_comparison.csv
  - data/processed/clustering/strict_only_sensitivity/collaboration/
        institution_nodes.csv, institution_communities.csv
  - project-d/data/processed/eu_paper_institution_affiliations.csv

Method: each paper is assigned the plurality network community among its
EU27 institutions that sit in the non-isolated network (ties go to the
community with the lower id). Agreement between topic cluster and network
community is then measured with a contingency table, Cramer's V, normalised
mutual information (NMI) and the adjusted Rand index (ARI). The same
measures are computed for topic cluster vs dominant country and network
community vs dominant country, to show what each partition tracks.

Outputs: CSV tables in .../strict_only_sensitivity/crosswalk/ and SVG figures
in docs/figures/.
"""

import csv
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path("data/processed/clustering/strict_only_sensitivity")
COLLAB = BASE / "collaboration"
AFFIL = Path("project-d/data/processed/eu_paper_institution_affiliations.csv")
OUT = BASE / "crosswalk"
FIG = Path("docs/figures")
TOP_COMMUNITIES = 10
PERMUTATIONS = 200
SEED = 1


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, header, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


def short_id(value):
    return value.rstrip("/").rsplit("/", 1)[-1]


# ---- agreement measures ---------------------------------------------------

def contingency(a, b):
    table = Counter(zip(a, b))
    return table, Counter(a), Counter(b)


def comb2(n):
    return n * (n - 1) / 2


def ari(a, b):
    table, ra, rb = contingency(a, b)
    n = len(a)
    index = sum(comb2(v) for v in table.values())
    sa = sum(comb2(v) for v in ra.values())
    sb = sum(comb2(v) for v in rb.values())
    expected = sa * sb / comb2(n)
    maximum = (sa + sb) / 2
    return (index - expected) / (maximum - expected)


def entropy(counts, n):
    return -sum(c / n * math.log(c / n) for c in counts.values() if c)


def nmi(a, b):
    table, ra, rb = contingency(a, b)
    n = len(a)
    mi = sum(
        c / n * math.log(c * n / (ra[i] * rb[j]))
        for (i, j), c in table.items()
    )
    denom = (entropy(ra, n) + entropy(rb, n)) / 2
    return mi / denom if denom else 0.0


def cramers_v(a, b):
    table, ra, rb = contingency(a, b)
    n = len(a)
    chi2 = 0.0
    for i in ra:
        for j in rb:
            expected = ra[i] * rb[j] / n
            chi2 += (table.get((i, j), 0) - expected) ** 2 / expected
    k = min(len(ra), len(rb)) - 1
    return math.sqrt(chi2 / (n * k)) if k else 0.0


def shuffled_mean(a, b, func, rng):
    """Mean of func(a, b shuffled) over PERMUTATIONS random shuffles.

    Gives the agreement expected by chance for these partition sizes.
    """
    total = 0.0
    for _ in range(PERMUTATIONS):
        b2 = b[:]
        rng.shuffle(b2)
        total += func(a, b2)
    return total / PERMUTATIONS


def purity(a, b):
    """Share of items in the modal b-label of each a-group."""
    groups = defaultdict(Counter)
    for x, y in zip(a, b):
        groups[x][y] += 1
    return sum(max(c.values()) for c in groups.values()) / len(a)


# ---- data assembly --------------------------------------------------------

def assign_communities(papers, node_community, affiliations):
    by_paper = defaultdict(list)
    for row in affiliations:
        by_paper[row["openalex_id"]].append(short_id(row["institution_id"]))
    result = {}
    for paper in papers:
        votes = Counter()
        has_institution = False
        for inst in set(by_paper.get(paper["openalex_id"], [])):
            has_institution = True
            if inst in node_community:
                votes[node_community[inst]] += 1
        if votes:
            top = max(votes.values())
            result[paper["openalex_id"]] = min(
                c for c, v in votes.items() if v == top
            )
        else:
            result[paper["openalex_id"]] = (
                "isolates_only" if has_institution else "no_institution"
            )
    return result


# ---- SVG helpers ----------------------------------------------------------

def svg_open(w, h):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" font-family="Helvetica, Arial, sans-serif">'
        f'<rect width="{w}" height="{h}" fill="white"/>'
    )


def text(x, y, s, size=12, anchor="start", weight="normal", fill="#222"):
    s = s.replace("&", "&amp;").replace("<", "&lt;")
    return (
        f'<text x="{x}" y="{y}" font-size="{size}" text-anchor="{anchor}" '
        f'font-weight="{weight}" fill="{fill}">{s}</text>'
    )


def heat_colour(share):
    # white -> dark blue
    level = max(0.0, min(1.0, share))
    r = int(255 - level * (255 - 31))
    g = int(255 - level * (255 - 78))
    b = int(255 - level * (255 - 121))
    return f"rgb({r},{g},{b})"


def heatmap_svg(path, title, row_labels, col_labels, matrix, note):
    cell_w, cell_h = 62, 34
    left, top = 300, 90
    w = left + cell_w * len(col_labels) + 30
    h = top + cell_h * len(row_labels) + 70
    parts = [svg_open(w, h), text(20, 28, title, 16, weight="bold")]
    parts.append(text(20, 48, note, 11, fill="#555"))
    for j, label in enumerate(col_labels):
        parts.append(
            text(left + j * cell_w + cell_w / 2, top - 10, label, 11, "middle")
        )
    for i, label in enumerate(row_labels):
        y = top + i * cell_h
        parts.append(text(left - 10, y + cell_h / 2 + 4, label, 11, "end"))
        for j, value in enumerate(matrix[i]):
            x = left + j * cell_w
            colour = heat_colour(value / 0.8)
            parts.append(
                f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" '
                f'fill="{colour}" stroke="white"/>'
            )
            ink = "white" if value > 0.4 else "#222"
            parts.append(
                text(x + cell_w / 2, y + cell_h / 2 + 4,
                     f"{value * 100:.0f}%", 11, "middle", fill=ink)
            )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(parts), encoding="utf-8")


def bar_svg(path, title, labels, values, note, fmt="{:.3f}", colours=None):
    w, h = 760, 90 + 46 * len(labels) + 30
    left, bar_max = 330, 330
    lo = min(0.0, min(values))
    hi = max(values) * 1.15 if max(values) > 0 else 1.0
    span = hi - lo
    zero_x = left + (0 - lo) / span * bar_max
    parts = [svg_open(w, h), text(20, 28, title, 16, weight="bold")]
    parts.append(text(20, 48, note, 11, fill="#555"))
    for i, (label, value) in enumerate(zip(labels, values)):
        y = 80 + i * 46
        x0 = left + (min(0, value) - lo) / span * bar_max
        width = abs(value) / span * bar_max
        colour = (colours or ["#1f4e79"] * len(labels))[i]
        parts.append(text(left - 10, y + 22, label, 12, "end"))
        parts.append(
            f'<rect x="{x0:.1f}" y="{y}" width="{width:.1f}" height="30" '
            f'fill="{colour}"/>'
        )
        parts.append(
            text(max(x0 + width, zero_x) + 8, y + 21, fmt.format(value), 12)
        )
    parts.append(
        f'<line x1="{zero_x:.1f}" y1="70" x2="{zero_x:.1f}" y2="{h - 20}" '
        f'stroke="#888"/>'
    )
    parts.append("</svg>")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(parts), encoding="utf-8")


# ---- main -----------------------------------------------------------------

def main():
    papers = read_csv(BASE / "cluster_assignments.csv")
    summary = {r["cluster"]: r for r in read_csv(BASE / "cluster_summary.csv")}
    nodes = read_csv(COLLAB / "institution_nodes.csv")
    communities = {
        r["community_id"]: r
        for r in read_csv(COLLAB / "institution_communities.csv")
    }
    baseline = read_csv(BASE / "baseline_comparison.csv")[0]
    node_community = {
        r["institution_id"]: r["community_id"]
        for r in nodes
        if r["is_isolate"] == "False"
    }
    paper_comm = assign_communities(
        papers, node_community, read_csv(AFFIL)
    )

    status = Counter(
        v if not v.isdigit() else "in_network" for v in paper_comm.values()
    )
    write_csv(
        OUT / "paper_community_assignment_status.csv",
        ["status", "papers"],
        sorted(status.items()),
    )

    # papers that can be placed in a network community
    linked = [p for p in papers if paper_comm[p["openalex_id"]].isdigit()]
    topic = [p["topic_cluster"] for p in linked]
    comm = [paper_comm[p["openalex_id"]] for p in linked]
    country = [p["dominant_eu_country"] or "NA" for p in linked]

    rng = random.Random(SEED)
    measures = []
    for name, x, y in [
        ("topic cluster vs network community", topic, comm),
        ("topic cluster vs dominant country", topic, country),
        ("network community vs dominant country", comm, country),
    ]:
        measures.append(
            (name, len(linked), round(nmi(x, y), 4),
             round(shuffled_mean(x, y, nmi, rng), 4),
             round(ari(x, y), 4), round(cramers_v(x, y), 4))
        )
    write_csv(
        OUT / "agreement_measures.csv",
        ["comparison", "papers", "nmi", "nmi_shuffled_mean", "ari",
         "cramers_v"],
        measures,
    )
    write_csv(
        OUT / "purity.csv",
        ["partition", "grouped_by", "share_of_papers_in_modal_country"],
        [
            ("topic cluster", "dominant country",
             round(purity(topic, country), 4)),
            ("network community", "dominant country",
             round(purity(comm, country), 4)),
        ],  # not comparable: 5 groups vs 46, so read with the NMI baseline
    )

    # contingency table: topic cluster x top communities (+ other)
    comm_sizes = Counter(comm)
    top = [c for c, _ in comm_sizes.most_common(TOP_COMMUNITIES)]
    clusters = sorted(summary, key=int)
    rows, matrix_share = [], []
    for cl in clusters:
        in_cl = [paper_comm[p["openalex_id"]] for p in linked
                 if p["topic_cluster"] == cl]
        counts = Counter(in_cl)
        other = sum(v for k, v in counts.items() if k not in top)
        rows.append([cl] + [counts.get(c, 0) for c in top] + [other])
        total = len(in_cl)
        matrix_share.append(
            [counts.get(c, 0) / total for c in top] + [other / total]
        )
    write_csv(
        OUT / "topic_cluster_by_network_community.csv",
        ["topic_cluster"] + [f"community_{c}" for c in top] + ["other"],
        rows,
    )

    # per-community profile: size, top countries, dominant topic cluster
    profile = []
    for c in sorted(communities, key=int):
        members = [p for p in linked if paper_comm[p["openalex_id"]] == c]
        if not members:
            continue
        topics = Counter(p["topic_cluster"] for p in members)
        top_topic, top_n = topics.most_common(1)[0]
        profile.append((
            c, len(members), communities[c]["countries"].split(";")[0].split(":")[0].strip(),
            top_topic, round(top_n / len(members), 3),
        ))
    write_csv(
        OUT / "community_profile.csv",
        ["community", "papers", "leading_country", "most_common_topic_cluster",
         "share_in_that_topic_cluster"],
        profile,
    )

    # ---- figures
    short = {
        "0": "Foundations, reviews, policy",
        "1": "Intelligent tutoring",
        "2": "Health / clinical ML",
        "3": "ML and student performance",
        "4": "Generative AI, higher ed",
    }
    row_labels = [f"{cl}: {short.get(cl, summary[cl]['top_terms'][:28])}"
                  for cl in clusters]
    col_labels = [
        f"C{c} ({communities[c]['countries'].split(':')[0]})" for c in top
    ] + ["Other"]
    heatmap_svg(
        FIG / "topic_cluster_vs_network_community.svg",
        "Where each topic cluster's papers sit in the collaboration network",
        row_labels, col_labels, matrix_share,
        f"Row share of papers, {len(linked)} papers placed in a network "
        f"community. Columns: the {TOP_COMMUNITIES} largest communities "
        "(leading country in brackets).",
    )

    sizes = [int(summary[cl]["size"]) for cl in clusters]
    bar_svg(
        FIG / "topic_cluster_sizes.svg",
        "Topic cluster sizes (STRICT sensitivity, k=5)",
        row_labels, [float(s) for s in sizes],
        "Number of papers per cluster.", fmt="{:.0f}",
    )

    topic_sil = float(baseline["topic_cluster_silhouette"])
    country_sil = float(baseline["country_baseline_silhouette"])
    bar_svg(
        FIG / "silhouette_topic_vs_country.svg",
        "Cosine silhouette: topic clusters vs country baseline",
        ["Topic clusters (k=5)", "Country baseline"],
        [topic_sil, country_sil],
        "Higher is better; 0 means no separation. Both are weak.",
        colours=["#1f4e79", "#b85c38"],
    )

    bar_svg(
        FIG / "agreement_nmi.svg",
        "What each partition tracks (normalised mutual information)",
        [m[0] for m in measures], [m[2] for m in measures],
        "0 = unrelated, 1 = identical. Chance level (shuffled labels) is 0.01-0.04.",
    )

    print(f"papers linked to a network community: {len(linked)} "
          f"of {len(papers)}")
    for name, n, nm, nm0, ar, cv in measures:
        print(f"{name}: NMI={nm} (shuffled {nm0}) ARI={ar} V={cv}")
    print("status:", dict(status))


if __name__ == "__main__":
    main()
