"""Community-level map of the institutional collaboration network (Step 5.3).

Standard library only. Reads the institution network written by
collaboration_analysis.py and draws one node per Louvain community.
Node size follows the number of institutions, colour follows the community's
leading country, and edge width follows the number of co-authored papers
between the two communities. Also writes network_edge_mix.csv with the share
of co-authorship ties that stay inside a community.
"""

import csv
import math
import random
from collections import Counter, defaultdict
from pathlib import Path

COLLAB = Path(
    "data/processed/clustering/strict_only_sensitivity/collaboration"
)
OUT_FIG = Path("docs/figures/collaboration_network_map.svg")
OUT_CSV = COLLAB / "network_edge_mix.csv"
MIN_INSTITUTIONS = 40  # communities shown on the map
W, H = 980, 760

PALETTE = {
    "FR": "#1f77b4", "IT": "#2ca02c", "NL": "#ff7f0e", "DE": "#7f7f7f",
    "ES": "#d62728", "PT": "#17becf", "DK": "#9467bd", "RO": "#8c564b",
    "GR": "#e377c2", "IE": "#bcbd22", "HU": "#393b79", "CY": "#ad494a",
    "PL": "#637939", "FI": "#3182bd",
}


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def layout(nodes, weights, seed=7, iterations=400):
    """Fruchterman-Reingold layout with a fixed seed."""
    rng = random.Random(seed)
    pos = {n: [rng.random(), rng.random()] for n in nodes}
    k = math.sqrt(1.0 / len(nodes))
    temp = 0.1
    for _ in range(iterations):
        disp = {n: [0.0, 0.0] for n in nodes}
        for a in nodes:
            for b in nodes:
                if a == b:
                    continue
                dx = pos[a][0] - pos[b][0]
                dy = pos[a][1] - pos[b][1]
                d = math.hypot(dx, dy) or 1e-6
                f = k * k / d
                disp[a][0] += dx / d * f
                disp[a][1] += dy / d * f
        for (a, b), w in weights.items():
            dx = pos[a][0] - pos[b][0]
            dy = pos[a][1] - pos[b][1]
            d = math.hypot(dx, dy) or 1e-6
            f = d * d / k * math.log1p(w) / 3
            for n, sign in ((a, -1), (b, 1)):
                disp[n][0] += sign * dx / d * f
                disp[n][1] += sign * dy / d * f
        for n in nodes:
            d = math.hypot(*disp[n]) or 1e-6
            step = min(d, temp)
            pos[n][0] += disp[n][0] / d * step
            pos[n][1] += disp[n][1] / d * step
        temp *= 0.99
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    return {
        n: (
            70 + (p[0] - min(xs)) / ((max(xs) - min(xs)) or 1) * (W - 140),
            90 + (p[1] - min(ys)) / ((max(ys) - min(ys)) or 1) * (H - 190),
        )
        for n, p in pos.items()
    }


def main():
    communities = {
        r["community_id"]: r
        for r in read_csv(COLLAB / "institution_communities.csv")
    }
    edges = read_csv(COLLAB / "institution_edges.csv")

    # share of ties (and co-authored papers) inside a community
    inside = sum(1 for e in edges if e["same_community"] == "True")
    inside_w = sum(
        int(e["coauthored_papers"]) for e in edges
        if e["same_community"] == "True"
    )
    total_w = sum(int(e["coauthored_papers"]) for e in edges)
    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["measure", "value"])
        writer.writerow(["institution_ties", len(edges)])
        writer.writerow(["ties_inside_a_community", inside])
        writer.writerow(["share_ties_inside", round(inside / len(edges), 4)])
        writer.writerow(["coauthored_papers_on_ties", total_w])
        writer.writerow(
            ["share_coauthored_papers_inside", round(inside_w / total_w, 4)]
        )

    shown = [
        c for c, r in communities.items()
        if int(r["institution_count"]) >= MIN_INSTITUTIONS
    ]
    weights = defaultdict(int)
    for e in edges:
        a, b = e["community_1"], e["community_2"]
        if a != b and a in shown and b in shown:
            weights[tuple(sorted((a, b)))] += int(e["coauthored_papers"])
    pos = layout(shown, weights)

    top_country = {
        c: communities[c]["countries"].split(";")[0].split(":")[0].strip()
        for c in shown
    }
    wmax = max(weights.values())
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" '
        f'viewBox="0 0 {W} {H}" font-family="Helvetica, Arial, sans-serif">'
        f'<rect width="{W}" height="{H}" fill="white"/>',
        '<text x="20" y="30" font-size="18" font-weight="bold" fill="#222">'
        "Collaboration communities of EU27 institutions</text>",
        '<text x="20" y="52" font-size="12" fill="#555">One node per '
        f"Louvain community with {MIN_INSTITUTIONS}+ institutions "
        f"({len(shown)} of {len(communities)}). Size = institutions, colour = "
        "leading country, line width = co-authored papers between "
        "communities.</text>",
    ]
    for (a, b), w in sorted(weights.items(), key=lambda x: x[1]):
        (x1, y1), (x2, y2) = pos[a], pos[b]
        parts.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="#888" stroke-opacity="0.45" '
            f'stroke-width="{0.5 + 7 * w / wmax:.2f}"/>'
        )
    for c in shown:
        x, y = pos[c]
        r = 8 + 1.9 * math.sqrt(int(communities[c]["institution_count"]))
        colour = PALETTE.get(top_country[c], "#aaaaaa")
        parts.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{colour}" '
            f'fill-opacity="0.85" stroke="white" stroke-width="2"/>'
        )
        parts.append(
            f'<text x="{x:.1f}" y="{y + 4:.1f}" font-size="11" '
            f'text-anchor="middle" fill="white" font-weight="bold">'
            f"{top_country[c]}</text>"
        )
        parts.append(
            f'<text x="{x:.1f}" y="{y + r + 13:.1f}" font-size="10" '
            f'text-anchor="middle" fill="#333">C{c} '
            f'({communities[c]["institution_count"]})</text>'
        )
    share = inside / len(edges) * 100
    parts.append(
        f'<text x="20" y="{H - 20}" font-size="12" fill="#333">'
        f"{share:.0f}% of the {len(edges):,} institution ties stay inside "
        f"one community ({inside_w / total_w * 100:.0f}% of co-authored "
        "papers). Layout: Fruchterman-Reingold, fixed seed.</text></svg>"
    )
    OUT_FIG.parent.mkdir(parents=True, exist_ok=True)
    OUT_FIG.write_text("".join(parts), encoding="utf-8")
    print(f"ties inside community: {share:.1f}%  ({inside_w}/{total_w} papers)")
    print("shown:", len(shown), Counter(top_country.values()))


if __name__ == "__main__":
    main()
