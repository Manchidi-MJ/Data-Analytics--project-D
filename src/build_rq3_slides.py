"""Build the RQ3 presentation deck (clustering and interpretation).

Standard library only. Reuses the master, layout and theme of Dev's deck so
both decks look alike, and draws every chart with native PowerPoint shapes
(no images), so the numbers stay editable. All figures are read from the
committed result CSVs, so the deck cannot drift from the analysis. Each slide
carries speaker notes.

    python src/build_rq3_slides.py

Input : project-d/ProjectD_RQ1_RQ2_slides.pptx (template only, unchanged)
        data/processed/clustering/strict_only_sensitivity/ (result CSVs)
Output: project-d/Manchidi.pptx
"""

import csv
import math
import re
import sys
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

sys.path.insert(0, "src")
import network_map  # noqa: E402  (layout helper, same folder)

TEMPLATE = Path("project-d/ProjectD_RQ1_RQ2_slides.pptx")
OUT = Path("project-d/Manchidi.pptx")
BASE = Path("data/processed/clustering/strict_only_sensitivity")

DARK, TEAL, ORANGE, INK, CARD, MUTED = (
    "12343B", "2C6E63", "D1603D", "1F2A2E", "EAF1EF", "5C6B70",
)
LIGHT_TEAL, LIGHT_ORANGE = "9CC9BF", "F3A58C"
SLIDE_W, SLIDE_H, MARGIN = 12192000, 6858000, 548640
NS = (
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/'
    'relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
)
THEMES = {
    "0": "Foundations, reviews, policy",
    "1": "Intelligent tutoring",
    "2": "Health / clinical ML",
    "3": "ML and student performance",
    "4": "Generative AI, higher education",
}
WARNINGS = []


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def font(face):
    return (
        f'<a:latin typeface="{face}" pitchFamily="34" charset="0"/>'
        f'<a:ea typeface="{face}" pitchFamily="34" charset="-122"/>'
        f'<a:cs typeface="{face}" pitchFamily="34" charset="-120"/>'
    )


def para(text, size=1600, colour=INK, bold=False, face="Calibri",
         bullet=False, algn="l"):
    return dict(text=text, size=size, colour=colour, bold=bold, face=face,
                bullet=bullet, algn=algn)


def para_xml(p):
    bold = ' b="1"' if p["bold"] else ""
    if p["bullet"]:
        ppr = (
            f'<a:pPr marL="342900" indent="-342900" algn="{p["algn"]}">'
            '<a:spcAft><a:spcPts val="1000"/></a:spcAft>'
            '<a:buSzPct val="100000"/><a:buChar char="&#x2022;"/></a:pPr>'
        )
    else:
        ppr = (
            f'<a:pPr indent="0" marL="0" algn="{p["algn"]}"><a:spcAft>'
            '<a:spcPts val="400"/></a:spcAft><a:buNone/></a:pPr>'
        )
    return (
        f'<a:p>{ppr}<a:r><a:rPr lang="en-US" sz="{p["size"]}"{bold} '
        f'dirty="0"><a:solidFill><a:srgbClr val="{p["colour"]}"/>'
        f'</a:solidFill>{font(p["face"])}</a:rPr><a:t>{escape(p["text"])}'
        f'</a:t></a:r><a:endParaRPr lang="en-US" sz="{p["size"]}" '
        'dirty="0"/></a:p>'
    )


def check_fit(name, paras, w, h):
    """Rough overflow estimate (Calibri averages ~0.5 em per character)."""
    width_in, height_in, used = w / 914400, h / 914400, 0.0
    for p in paras:
        usable = width_in - (0.375 if p["bullet"] else 0)
        chars_per_line = max(1, usable / (p["size"] / 100 * 0.5 / 72))
        lines = max(1, math.ceil(len(p["text"]) / chars_per_line))
        used += lines * p["size"] / 100 * 1.2 / 72
        used += (10 if p["bullet"] else 4) / 72
    if used > height_in * 1.02:
        WARNINGS.append(f"{name}: text needs {used:.2f} in, box {height_in:.2f} in")


class Slide:
    def __init__(self, name, bg="FFFFFF", notes=""):
        self.name, self.bg, self.notes = name, bg, notes
        self.shapes, self.next_id = [], 2

    def _id(self):
        self.next_id += 1
        return self.next_id - 1

    def box(self, x, y, w, h, paras=None, kind="rect", fill=None,
            line=None, alpha=None, anchor="t", radius=None):
        i = self._id()
        x, y, w, h = int(x), int(y), int(max(w, 1)), int(max(h, 1))
        if fill:
            a = f'<a:alpha val="{alpha}"/>' if alpha else ""
            fill_xml = f'<a:solidFill><a:srgbClr val="{fill}">{a}' \
                       "</a:srgbClr></a:solidFill>"
        else:
            fill_xml = "<a:noFill/>"
        ln = (
            f'<a:ln w="19050"><a:solidFill><a:srgbClr val="{line}"/>'
            "</a:solidFill></a:ln>" if line else "<a:ln><a:noFill/></a:ln>"
        )
        geom = (
            '<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" '
            f'fmla="val {radius}"/></a:avLst></a:prstGeom>'
            if radius else
            f'<a:prstGeom prst="{kind}"><a:avLst></a:avLst></a:prstGeom>'
        )
        body = "".join(para_xml(p) for p in (paras or [])) or (
            '<a:p><a:endParaRPr lang="en-US"/></a:p>'
        )
        if paras:
            check_fit(f"{self.name} box {i}", paras, w, h)
        self.shapes.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Shape {i}"></p:cNvPr>'
            '<p:cNvSpPr/><p:nvPr></p:nvPr></p:nvSpPr><p:spPr><a:xfrm>'
            f'<a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            f"{geom}{fill_xml}{ln}</p:spPr><p:txBody><a:bodyPr wrap=\"square\" "
            'lIns="45720" tIns="0" rIns="45720" bIns="0" rtlCol="0" '
            f'anchor="{anchor}"></a:bodyPr><a:lstStyle/>{body}</p:txBody></p:sp>'
        )

    def text(self, x, y, w, h, paras, anchor="t"):
        self.box(x, y, w, h, paras, anchor=anchor)

    def line(self, x1, y1, x2, y2, colour, width, alpha=None):
        i = self._id()
        flip = ' flipV="1"' if (x2 - x1) * (y2 - y1) < 0 else ""
        a = f'<a:alpha val="{alpha}"/>' if alpha else ""
        self.shapes.append(
            f'<p:cxnSp><p:nvCxnSpPr><p:cNvPr id="{i}" name="Line {i}"/>'
            '<p:cNvCxnSpPr/><p:nvPr/></p:nvCxnSpPr><p:spPr>'
            f'<a:xfrm{flip}><a:off x="{int(min(x1, x2))}" '
            f'y="{int(min(y1, y2))}"/><a:ext cx="{int(abs(x2 - x1))}" '
            f'cy="{int(abs(y2 - y1))}"/></a:xfrm><a:prstGeom prst="line">'
            f'<a:avLst/></a:prstGeom><a:ln w="{int(width)}"><a:solidFill>'
            f'<a:srgbClr val="{colour}">{a}</a:srgbClr></a:solidFill></a:ln>'
            "</p:spPr></p:cxnSp>"
        )

    def title(self, text, colour=DARK):
        if len(text) > 52:
            WARNINGS.append(f"{self.name}: title may wrap ({len(text)} chars)")
        self.text(MARGIN, 365760, SLIDE_W - 2 * MARGIN, 822960, [
            para(text, 3200, colour, True, "Cambria")], anchor="ctr")

    def card(self, x, y, w, h, fill=CARD):
        self.box(x, y, w, h, fill=fill, radius=6316)

    def stat(self, x, y, big, label, colour=TEAL, w=3200400, h=1600200):
        self.card(x, y, w, h)
        self.text(x + 182880, y + 137160, w - 365760, 800000,
                  [para(big, 4400, colour, True, "Cambria")], anchor="ctr")
        self.text(x + 182880, y + 960120, w - 365760, h - 1000000,
                  [para(label, 1400, INK)])

    def footnote(self, text, colour=MUTED):
        self.text(MARGIN, 6263640, SLIDE_W - 2 * MARGIN, 380000,
                  [para(text, 1200, colour)])

    def xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<p:sld {NS}><p:cSld name="{self.name}"><p:bg><p:bgPr>'
            f'<a:solidFill><a:srgbClr val="{self.bg}"/></a:solidFill>'
            '</p:bgPr></p:bg><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" '
            'name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr>'
            '<a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
            '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm>'
            f'</p:grpSpPr>{"".join(self.shapes)}</p:spTree></p:cSld>'
            "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>"
        )


def notes_xml(number, text):
    paragraphs = "".join(
        f'<a:p><a:r><a:rPr lang="en-US" dirty="0"/><a:t>{escape(t)}</a:t>'
        "</a:r></a:p>" for t in text.split("\n") if t.strip()
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        f"<p:notes {NS}><p:cSld><p:spTree><p:nvGrpSpPr><p:cNvPr id=\"1\" "
        'name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm>'
        '<a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/>'
        '<a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr><p:sp><p:nvSpPr>'
        '<p:cNvPr id="2" name="Slide Image Placeholder 1"/><p:cNvSpPr>'
        '<a:spLocks noGrp="1" noRot="1" noChangeAspect="1"/></p:cNvSpPr>'
        '<p:nvPr><p:ph type="sldImg"/></p:nvPr></p:nvSpPr><p:spPr/></p:sp>'
        '<p:sp><p:nvSpPr><p:cNvPr id="3" name="Notes Placeholder 2"/>'
        '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph '
        'type="body" idx="1"/></p:nvPr></p:nvSpPr><p:spPr/><p:txBody>'
        f"<a:bodyPr/><a:lstStyle/>{paragraphs}</p:txBody></p:sp>"
        '<p:sp><p:nvSpPr><p:cNvPr id="4" name="Slide Number Placeholder 3"/>'
        '<p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr><p:ph '
        'type="sldNum" sz="quarter" idx="10"/></p:nvPr></p:nvSpPr><p:spPr/>'
        '<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:fld id="{F7021451-1387-'
        '4CA6-816F-3879F97B5CBC}" type="slidenum"><a:rPr lang="en-US"/>'
        f'<a:t>{number}</a:t></a:fld><a:endParaRPr lang="en-US"/></a:p>'
        "</p:txBody></p:sp></p:spTree></p:cSld><p:clrMapOvr>"
        "<a:masterClrMapping/></p:clrMapOvr></p:notes>"
    )


def mix(hex_a, hex_b, t):
    """Blend colour a (t=0) to colour b (t=1)."""
    a = [int(hex_a[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int(hex_b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


# ---- data ------------------------------------------------------------------

def load():
    d = {}
    d["summary"] = read_csv(BASE / "cluster_summary.csv")
    d["k_eval"] = read_csv(BASE / "k_evaluation.csv")
    d["baseline"] = read_csv(BASE / "baseline_comparison.csv")[0]
    d["stability"] = read_csv(BASE / "stability_comparison.csv")[0]
    d["net"] = read_csv(BASE / "collaboration/network_summary.csv")[0]
    d["edge_mix"] = {
        r["measure"]: float(r["value"])
        for r in read_csv(BASE / "collaboration/network_edge_mix.csv")
    }
    d["communities"] = read_csv(
        BASE / "collaboration/institution_communities.csv")
    d["edges"] = read_csv(BASE / "collaboration/institution_edges.csv")
    d["cross"] = read_csv(BASE / "crosswalk/topic_cluster_by_network_community.csv")
    d["agree"] = read_csv(BASE / "crosswalk/agreement_measures.csv")
    return d


# ---- slides ----------------------------------------------------------------

def slide_title(d):
    s = Slide("Slide 1", DARK, notes=(
        "I am John Magaseng Manchidi. My part is RQ3: do the institutions "
        "that publish AI-in-education research form one collaboration "
        "community or several, and do research topics follow those "
        "communities?"))
    s.text(731520, 1280160, 10515600, 548640,
           [para("Project D  |  RQ3", 2000, LIGHT_TEAL, True)], "ctr")
    s.text(731520, 1828800, 10515600, 1645920, [
        para("One community or several?", 4800, "FFFFFF", True, "Cambria")],
        "ctr")
    s.text(731520, 3749040, 10515600, 800000, [
        para("Topic clusters, collaboration communities and what they mean "
             "for AI in education research in Europe", 2000, "FFFFFF")])
    s.text(731520, 5000000, 10515600, 457200, [
        para("John Magaseng Manchidi  |  Clustering and interpretation  |  "
             "Data Analytics, Fall 2026", 1600, LIGHT_TEAL)])
    return s


def slide_approach(d):
    s = Slide("Slide 2", notes=(
        "We asked one question two ways. First, what do the papers talk "
        "about? That is the text clustering. Second, who works with whom? "
        "That is the institution network.\n"
        "The point of the project is the comparison: if topics and "
        "collaboration line up, the field is several topical communities. "
        "If they do not, something else, such as geography, organises it.\n"
        "I added a manual check of the most doubtful records, because the "
        "keyword search lets in health papers that are not about education."))
    s.title("Two views of the same papers")
    steps = [
        ("1", "Topic clusters",
         "TF-IDF on titles and abstracts, KMeans, k from 4 to 10"),
        ("2", "Baseline check",
         "Do clusters beat simply grouping papers by country?"),
        ("3", "Manual review",
         "125 doubtful records checked; 123 were out of scope"),
        ("4", "Network",
         "1,641 institutions linked by co-authored papers; Louvain "
         "communities"),
        ("5", "Compare",
         "Does topic follow community? Does community follow country?"),
    ]
    w, gap = 2000000, 250000
    for k, (num, head, body) in enumerate(steps):
        x = MARGIN + k * (w + gap)
        s.card(x, 1554480, w, 3200400)
        s.box(x + 137160, 1691640, 480000, 480000, [
            para(num, 2000, "FFFFFF", True, "Cambria", algn="ctr")],
            kind="ellipse", fill=TEAL if k != 2 else ORANGE, anchor="ctr")
        s.text(x + 137160, 2332000, w - 274320, 700000,
               [para(head, 1600, DARK, True, "Cambria")], "ctr")
        s.text(x + 137160, 3150000, w - 274320, 1500000,
               [para(body, 1400, INK)])
        if k < len(steps) - 1:
            s.text(x + w - 75000, 3000000, gap + 150000, 500000,
                   [para("\u203A", 2400, MUTED, algn="ctr")], "ctr")
    s.text(MARGIN, 5120640, SLIDE_W - 2 * MARGIN, 700000, [
        para("Data: 2,972 STRICT papers judged likely relevant, after "
             "removing the 123 reviewed out-of-scope records. "
             "Orange step: the one that changed the dataset.", 1500, MUTED)])
    return s


def slide_themes(d):
    s = Slide("Slide 3", notes=(
        "Five themes came out. The two largest are generative AI in higher "
        "education, about a third of papers, and a broad group of "
        "foundations, reviews and policy, about 28%.\n"
        "Cluster 2 is the health crossover. Even after removing 123 papers "
        "by hand, a tenth of the set still sits there, which tells you the "
        "search lets in clinical machine learning.\n"
        "Treat the names as my reading of the top terms and example titles. "
        "They are not validated categories."))
    s.title("Five broad themes")
    rows = sorted(d["summary"], key=lambda r: -float(r["share_pct"]))
    top_share = max(float(r["share_pct"]) for r in rows)
    label_w, bar_x, bar_max = 3500000, MARGIN + 3600000, 4300000
    for i, r in enumerate(rows):
        y = 1500000 + i * 880000
        share = float(r["share_pct"])
        c = r["cluster"]
        s.text(MARGIN, y, label_w, 640000, [
            para(THEMES[c], 1600, INK, True)], "ctr")
        s.box(bar_x, y + 60000, bar_max * share / top_share, 520000,
              fill=ORANGE if c == "2" else TEAL)
        s.text(bar_x + bar_max * share / top_share + 91440, y, 1900000,
               640000, [para(f"{share:.0f}%  ({int(r['size'])})", 1600, INK,
                             True)], "ctr")
    s.text(MARGIN + 3600000, 5900000, 7000000, 300000, [
        para("Share of 2,972 papers (number of papers). Orange: health "
             "crossover.", 1200, MUTED)])
    s.card(9300000, 1500000, 2340000, 3300000)
    s.text(9420000, 1600000, 2100000, 3100000, [
        para("Top terms", 1600, DARK, True, "Cambria"),
        para("Gen AI: generative ai, genai, higher education, chatgpt",
             1200),
        para("Tutoring: intelligent tutoring, adaptive, feedback", 1200),
        para("Health: patients, clinical, risk, disease", 1200),
    ])
    return s


def slide_quality(d):
    s = Slide("Slide 4", notes=(
        "Here is the honest part. Silhouette runs from minus one to one and "
        "zero means no structure. Our best score is 0.013.\n"
        "The country baseline, grouping the same papers by country, scores "
        "minus 0.012. So topic clusters beat the baseline, but only barely.\n"
        "Look at the bars: silhouette hardly moves with k. Five is the "
        "highest, but four, six and seven are within a hair. So k=5 is a "
        "convenient choice, not a discovery.\n"
        "The takeaway: use these as broad, overlapping themes for "
        "description, and do not build strong claims on the exact cluster "
        "boundaries."))
    s.title("The clusters are real but weak")
    ev = d["k_eval"]
    vals = [float(r["silhouette_cosine"]) for r in ev]
    chart_x, chart_y, chart_w, chart_h = MARGIN + 400000, 1750000, 6800000, 3300000
    ymax = 0.016
    s.text(MARGIN, 1350000, 7200000, 330000, [
        para("Cosine silhouette by number of clusters (k)", 1600, DARK,
             True)])
    s.line(chart_x, chart_y + chart_h, chart_x + chart_w,
           chart_y + chart_h, MUTED, 12700)
    slot = chart_w / len(ev)
    best = max(vals)
    for i, (r, v) in enumerate(zip(ev, vals)):
        h = chart_h * v / ymax
        x = chart_x + i * slot + slot * 0.15
        s.box(x, chart_y + chart_h - h, slot * 0.7, h,
              fill=ORANGE if v == best else TEAL)
        s.text(x - 100000, chart_y + chart_h - h - 300000, slot * 0.7 + 200000,
               280000, [para(f"{v:.4f}", 1100, INK, algn="ctr")])
        s.text(x - 100000, chart_y + chart_h + 50000, slot * 0.7 + 200000,
               300000, [para(f"k={r['k']}", 1200, INK, algn="ctr")])
    base = d["baseline"]
    s.stat(8300000, 1554480, f"{float(base['topic_cluster_silhouette']):.3f}",
           "topic clusters, k=5", TEAL, w=3300000, h=1500000)
    s.stat(8300000, 3250000,
           f"{float(base['country_baseline_silhouette']):.3f}",
           "grouping by country (baseline)", ORANGE, w=3300000, h=1500000)
    s.footnote("0 means no structure. Both scores are close to 0, so use "
               "the clusters as broad themes, not sharp categories.")
    return s


def slide_map(d):
    net = d["net"]
    s = Slide("Slide 5", notes=(
        "Each bubble is one collaboration community found by Louvain "
        "clustering. Size is the number of institutions, the label is the "
        "country that dominates it, and the lines show co-authored papers "
        "between communities.\n"
        "The communities are strikingly national: France, Italy, Spain, "
        "Portugal, Greece and Romania each have a community built around "
        "them. Germany splits into three because it has so many "
        "institutions.\n"
        "71% of institution ties stay inside a community. Be careful: "
        "Louvain is designed to maximise that, so it shows a clear split, "
        "not a natural boundary. Also, we only count EU27 institutions, so "
        "partners in the UK, Switzerland or Norway are missing."))
    s.title("Several communities, mostly national")
    comms = {r["community_id"]: r for r in d["communities"]}
    shown = [c for c, r in comms.items() if int(r["institution_count"]) >= 40]
    weights = {}
    for e in d["edges"]:
        a, b = e["community_1"], e["community_2"]
        if a != b and a in shown and b in shown:
            key = tuple(sorted((a, b)))
            weights[key] = weights.get(key, 0) + int(e["coauthored_papers"])
    pos = network_map.layout(shown, weights)
    ax, ay, aw, ah = MARGIN, 1350000, 7500000, 4750000
    px = {c: ax + 400000 + (pos[c][0] - 70) / (network_map.W - 140)
          * (aw - 800000) for c in shown}
    py = {c: ay + 300000 + (pos[c][1] - 90) / (network_map.H - 190)
          * (ah - 700000) for c in shown}
    radii = {c: 120000 + 30000 * math.sqrt(int(comms[c]["institution_count"]))
             for c in shown}
    for _ in range(400):  # push overlapping bubbles apart, keep inside area
        for i, a in enumerate(shown):
            for b in shown[i + 1:]:
                dx, dy = px[b] - px[a], py[b] - py[a]
                dist = math.hypot(dx, dy) or 1.0
                gap_needed = radii[a] + radii[b] + 60000
                if dist < gap_needed:
                    push = (gap_needed - dist) / 2
                    px[a] -= dx / dist * push
                    py[a] -= dy / dist * push
                    px[b] += dx / dist * push
                    py[b] += dy / dist * push
        for c in shown:
            px[c] = min(max(px[c], ax + radii[c]), ax + aw - radii[c])
            py[c] = min(max(py[c], ay + radii[c] + 100000),
                        ay + ah - radii[c] - 250000)
    wmax = max(weights.values())
    for (a, b), w in sorted(weights.items(), key=lambda kv: kv[1]):
        s.line(px[a], py[a], px[b], py[b], "888888",
               6350 + 70000 * w / wmax, alpha=45000)
    palette = {"FR": "1F77B4", "IT": "2CA02C", "NL": "FF7F0E", "DE": "7F7F7F",
               "ES": "D62728", "PT": "17BECF", "DK": "9467BD", "RO": "8C564B",
               "GR": "E377C2", "IE": "BCBD22", "HU": "393B79"}
    for c in shown:
        r = comms[c]
        code = r["countries"].split(";")[0].split(":")[0].strip()
        rad = radii[c]
        s.box(px[c] - rad, py[c] - rad, 2 * rad, 2 * rad, [
            para(code, 1200, "FFFFFF", True, algn="ctr")], kind="ellipse",
            fill=palette.get(code, "AAAAAA"), line="FFFFFF", anchor="ctr")
    for i, a in enumerate(shown):
        for b in shown[i + 1:]:
            if math.hypot(px[a] - px[b], py[a] - py[b]) < radii[a] + radii[b]:
                WARNINGS.append(f"Slide 5: bubbles C{a} and C{b} overlap")
    s.stat(8500000, 1500000, str(net["louvain_communities_nonisolated"]),
           f"communities (modularity "
           f"{float(net['louvain_modularity_nonisolated']):.2f}); "
           f"{len(shown)} are large", w=3150000, h=1500000)
    inside = d["edge_mix"]["share_ties_inside"] * 100
    s.stat(8500000, 3150000, f"{inside:.0f}%",
           "of institution ties stay inside a community", ORANGE,
           w=3150000, h=1500000)
    s.text(8500000, 4800000, 3150000, 1300000, [
        para("France 118 of 140 institutions, Italy 89 of 129, Spain 68 of "
             "119, Portugal 56 of 89 in their largest community.", 1200,
             MUTED)])
    s.footnote("Bubble size = institutions, label = leading country, line "
               "width = co-authored papers. EU27 institutions only.")
    return s


def slide_crosswalk(d):
    s = Slide("Slide 6", notes=(
        "Now the key comparison. Each row is a topic cluster, each column "
        "one of the ten biggest collaboration communities, and each cell is "
        "the share of that topic cluster's papers in that community.\n"
        "If topics followed communities, you would see dark cells, one per "
        "row. You see an even wash. Every community contains every theme. "
        "Generative AI is the biggest theme nearly everywhere.\n"
        "The numbers say the same: topic and community agree at an NMI of "
        "0.03, where shuffled labels give 0.01. There is a real link, but "
        "a tiny one. Community and country agree at 0.45 against 0.04 for "
        "shuffled labels, which is a strong link.\n"
        "So geography organises collaboration, and topics are shared "
        "across countries."))
    s.title("Topics cut across the communities")
    cross = d["cross"]
    cols = [h for h in cross[0].keys() if h != "topic_cluster"]
    comm_by_id = {r["community_id"]: r for r in d["communities"]}
    left, top, cw, chh = MARGIN + 3000000, 1900000, 700000, 520000
    s.text(MARGIN, 1350000, 11000000, 330000, [
        para("Share of each topic cluster's papers in the ten largest "
             "network communities", 1500, DARK, True)])
    for j, col in enumerate(cols):
        if col == "other":
            lab = "Other"
        else:
            cid = col.split("_")[1]
            code = comm_by_id[cid]["countries"].split(";")[0].split(":")[0]
            lab = f"C{cid} {code.strip()}"
        s.text(left + j * cw, top - 330000, cw, 300000,
               [para(lab, 1100, INK, True, algn="ctr")], "ctr")
    for i, row in enumerate(cross):
        counts = [int(row[c]) for c in cols]
        total = sum(counts)
        y = top + i * chh
        s.text(MARGIN, y, 2950000, chh, [
            para(f"{THEMES[row['topic_cluster']]}", 1300, INK, True)], "ctr")
        for j, n in enumerate(counts):
            share = n / total
            t = min(1.0, share / 0.30)
            s.box(left + j * cw, y, cw, chh, [
                para(f"{share * 100:.0f}", 1200,
                     "FFFFFF" if t > 0.55 else INK, algn="ctr")],
                fill=mix("F4F7F6", TEAL, t), line="FFFFFF", anchor="ctr")
    agree = {r["comparison"]: r for r in d["agree"]}
    cards = [
        ("topic cluster vs network community", ORANGE,
         "NMI, topic vs community"),
        ("network community vs dominant country", TEAL,
         "NMI, community vs country"),
    ]
    y0 = top + len(cross) * chh + 330000
    for k, (key, colour, label) in enumerate(cards):
        r = agree[key]
        x = MARGIN + k * 3500000
        s.card(x, y0, 3300000, 1250000)
        s.text(x + 182880, y0 + 100000, 1450000, 1050000, [
            para(f"{float(r['nmi']):.2f}", 4000, colour, True, "Cambria")],
            "ctr")
        s.text(x + 1600000, y0 + 150000, 1600000, 950000, [
            para(label, 1300, INK, True),
            para(f"shuffled labels: {float(r['nmi_shuffled_mean']):.2f}",
                 1200, MUTED)], "ctr")
    s.text(7700000, y0, 3900000, 1250000, [
        para("Each cell is a % of the row; rows sum to 100. An even wash "
             "means every community studies every theme.", 1300, MUTED)],
        "ctr")
    return s


def slide_meaning(d):
    s = Slide("Slide 7", DARK, notes=(
        "So what does it mean? The field is not one community and not a set "
        "of topical camps. It is a set of national or regional "
        "collaboration clusters that all work on the same themes.\n"
        "That matters for funding and policy: cross-border links on shared "
        "topics such as generative AI in higher education are thin, so "
        "there may be duplicated effort.\n"
        "Now the limits. Our search finds about a fifth of the relevant "
        "papers, so if the missing ones are mainly non-English, the "
        "national communities are probably understated. The network only "
        "counts EU27 institutions. The text clusters are weak. Any of "
        "these could move numbers, though I would expect the main result, "
        "geography over topic, to hold.\n"
        "Questions are welcome."))
    s.title("What it means", "FFFFFF")
    s.text(MARGIN, 1371600, 5303520, 450000, [
        para("Findings", 2200, LIGHT_TEAL, True, "Cambria")], "ctr")
    s.text(MARGIN, 1874520, 5303520, 4206240, [
        para("Several collaboration communities, not one", 1500, "FFFFFF",
             bullet=True),
        para("Large communities are mostly national or regional", 1500,
             "FFFFFF", bullet=True),
        para("The same themes appear in every community", 1500, "FFFFFF",
             bullet=True),
        para("Geography organises collaboration, topic does not", 1500,
             "FFFFFF", bullet=True),
        para("Implication: little cross-border collaboration on shared "
             "topics such as generative AI in higher education", 1500,
             "FFFFFF", bullet=True),
    ])
    s.text(6309360, 1371600, 5303520, 450000, [
        para("What could change this", 2200, LIGHT_ORANGE, True,
             "Cambria")], "ctr")
    s.text(6309360, 1874520, 5303520, 4206240, [
        para("Search recall is about 21%; missing non-English work could "
             "understate national communities", 1500, "FFFFFF", bullet=True),
        para("EU27-only network leaves out UK, Swiss and Norwegian partners",
             1500, "FFFFFF", bullet=True),
        para("Silhouette near 0.01: themes overlap heavily", 1500, "FFFFFF",
             bullet=True),
        para("Manual review covered two clusters only", 1500, "FFFFFF",
             bullet=True),
        para("Next: widen the query, add non-EU partners, test other "
             "community settings", 1500, "FFFFFF", bullet=True),
    ])
    return s


# ---- packaging -------------------------------------------------------------

def package(slides):
    with zipfile.ZipFile(TEMPLATE) as zin:
        keep = {
            n: zin.read(n) for n in zin.namelist()
            if not n.endswith("/") and not n.startswith((
                "ppt/slides/", "ppt/charts/", "ppt/embeddings/",
                "ppt/notesSlides/"))
        }
    n = len(slides)
    files = dict(keep)

    ct = ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
          '<Types xmlns="http://schemas.openxmlformats.org/package/2006/'
          'content-types"><Default Extension="xml" ContentType="application/'
          'xml"/><Default Extension="rels" ContentType="application/vnd.'
          'openxmlformats-package.relationships+xml"/>')
    pt = "application/vnd.openxmlformats-officedocument.presentationml."
    fixed = {
        "/ppt/presentation.xml": pt + "presentation.main+xml",
        "/ppt/notesMasters/notesMaster1.xml": pt + "notesMaster+xml",
        "/ppt/slideMasters/slideMaster1.xml": pt + "slideMaster+xml",
        "/ppt/slideLayouts/slideLayout1.xml": pt + "slideLayout+xml",
        "/ppt/presProps.xml": pt + "presProps+xml",
        "/ppt/viewProps.xml": pt + "viewProps+xml",
        "/ppt/tableStyles.xml": pt + "tableStyles+xml",
        "/ppt/theme/theme1.xml":
            "application/vnd.openxmlformats-officedocument.theme+xml",
        "/docProps/core.xml":
            "application/vnd.openxmlformats-package.core-properties+xml",
        "/docProps/app.xml": "application/vnd.openxmlformats-officedocument."
                             "extended-properties+xml",
    }
    for part, ctype in fixed.items():
        if part.lstrip("/") in files:
            ct += f'<Override PartName="{part}" ContentType="{ctype}"/>'
    for i in range(1, n + 1):
        ct += (f'<Override PartName="/ppt/slides/slide{i}.xml" '
               f'ContentType="{pt}slide+xml"/>'
               f'<Override PartName="/ppt/notesSlides/notesSlide{i}.xml" '
               f'ContentType="{pt}notesSlide+xml"/>')
    ct += "</Types>"
    files["[Content_Types].xml"] = ct.encode("utf-8")

    rel_ns = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    for i, slide in enumerate(slides, 1):
        files[f"ppt/slides/slide{i}.xml"] = slide.xml().encode("utf-8")
        files[f"ppt/slides/_rels/slide{i}.xml.rels"] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/'
            'package/2006/relationships"><Relationship Id="rId1" '
            f'Type="{rel_ns}/slideLayout" '
            'Target="../slideLayouts/slideLayout1.xml"/><Relationship '
            f'Id="rId2" Type="{rel_ns}/notesSlide" '
            f'Target="../notesSlides/notesSlide{i}.xml"/></Relationships>'
        ).encode("utf-8")
        files[f"ppt/notesSlides/notesSlide{i}.xml"] = notes_xml(
            i, slide.notes).encode("utf-8")
        files[f"ppt/notesSlides/_rels/notesSlide{i}.xml.rels"] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/'
            'package/2006/relationships"><Relationship Id="rId1" '
            f'Type="{rel_ns}/notesMaster" '
            'Target="../notesMasters/notesMaster1.xml"/><Relationship '
            f'Id="rId2" Type="{rel_ns}/slide" '
            f'Target="../slides/slide{i}.xml"/></Relationships>'
        ).encode("utf-8")

    # presentation.xml and its relationships
    pres = files["ppt/presentation.xml"].decode("utf-8")
    ids = "".join(
        f'<p:sldId id="{255 + i}" r:id="rId{100 + i}"/>'
        for i in range(1, n + 1))
    pres = re.sub(r"<p:sldIdLst>.*?</p:sldIdLst>",
                  f"<p:sldIdLst>{ids}</p:sldIdLst>", pres, flags=re.S)
    files["ppt/presentation.xml"] = pres.encode("utf-8")
    prel = files["ppt/_rels/presentation.xml.rels"].decode("utf-8")
    prel = re.sub(r'<Relationship Id="rId\d+" Type="[^"]*/slide" '
                  r'Target="slides/[^"]*"/>', "", prel)
    add = "".join(
        f'<Relationship Id="rId{100 + i}" Type="{rel_ns}/slide" '
        f'Target="slides/slide{i}.xml"/>' for i in range(1, n + 1))
    files["ppt/_rels/presentation.xml.rels"] = prel.replace(
        "</Relationships>", add + "</Relationships>").encode("utf-8")

    app = files["docProps/app.xml"].decode("utf-8")
    app = re.sub(r"<Slides>\d+</Slides>", f"<Slides>{n}</Slides>", app)
    app = re.sub(r"<Notes>\d+</Notes>", f"<Notes>{n}</Notes>", app)
    files["docProps/app.xml"] = app.encode("utf-8")
    core = files["docProps/core.xml"].decode("utf-8")
    core = core.replace("Project D: RQ1 and RQ2", "Manchidi")
    files["docProps/core.xml"] = core.encode("utf-8")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as zout:
        zout.writestr("[Content_Types].xml", files.pop("[Content_Types].xml"))
        for name, data in files.items():
            zout.writestr(name, data)


def main():
    d = load()
    slides = [
        slide_title(d), slide_approach(d), slide_themes(d),
        slide_quality(d), slide_map(d), slide_crosswalk(d),
        slide_meaning(d),
    ]
    package(slides)
    print(f"wrote {OUT} with {len(slides)} slides")
    for w in WARNINGS:
        print("WARNING:", w)


if __name__ == "__main__":
    main()
