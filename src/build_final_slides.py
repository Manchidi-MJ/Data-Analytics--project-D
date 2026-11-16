"""Build the team's final presentation deck (10 minutes).

Standard library only.

    python src/build_final_slides.py

Order (11 slides, about one minute each):
  1  Title                              Dev's slide 1, subtitle updated
  2  Data and who did what              Dev's slide 2
  3  RQ1 institutions                   Dev's slide 3
  4  RQ2 growth                         Dev's slide 6
  5  RQ2 ALL vs STRICT                  Dev's slide 7
  6  RQ3 collaboration network          Keerthana's map and numbers
  7  RQ3 topic themes                   John
  8  RQ3 cluster quality vs baseline    John
  9  RQ3 topics across communities      John
  10 RQ4 what the search misses         Mabango's numbers
  11 Answers, limits, next steps        team

Dev's slides 4, 5 and 8 (countries, venues, ranking stability) are left out
for time; their content is in docs/REPORT.md. Dev's slides keep his charts.

Inputs : project-d/ProjectD_RQ1_RQ2_slides.pptx (unchanged)
         project-d/data/raw/network_*.csv, fig_network_map.png (Keerthana)
         data/processed/clustering/strict_only_sensitivity/ (John)
Output : project-d/ProjectD_final_slides.pptx
"""

import csv
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, "src")
import build_rq3_slides as rq3  # noqa: E402

SRC = Path("project-d/ProjectD_RQ1_RQ2_slides.pptx")
DST = Path("project-d/ProjectD_final_slides.pptx")
NET = Path("project-d/data/raw")
MAP_PNG = NET / "fig_network_map.png"

KEEP = [1, 2, 3, 6, 7]          # Dev's slides, in this order
DROP = [4, 5, 8, 9]             # slide 9 is replaced by the new closing slide
REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PML = "application/vnd.openxmlformats-officedocument.presentationml."


def read_csv(path):
    with open(path, newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def picture(slide, rid, x, y, w, h):
    i = slide._id()
    slide.shapes.append(
        f'<p:pic><p:nvPicPr><p:cNvPr id="{i}" name="Picture {i}"/>'
        '<p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr><p:nvPr/>'
        f'</p:nvPicPr><p:blipFill><a:blip r:embed="{rid}"/><a:stretch>'
        '<a:fillRect/></a:stretch></p:blipFill><p:spPr><a:xfrm>'
        f'<a:off x="{int(x)}" y="{int(y)}"/><a:ext cx="{int(w)}" '
        f'cy="{int(h)}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/>'
        "</a:prstGeom></p:spPr></p:pic>"
    )


def slide_network():
    main = read_csv(NET / "network_sensitivity.csv")[0]
    comms = read_csv(NET / "network_communities.csv")
    pairs = read_csv(NET / "network_country_pairs.csv")[:3]
    by_country = {}
    for c in comms:
        by_country.setdefault(c["top_country"], c)
    s = rq3.Slide("Network", notes=(
        "This is Keerthana's network. Each dot is an EU institution, and a "
        "line means the two institutions share at least one paper. Colours "
        "are Louvain communities.\n"
        f"Louvain finds {main['communities']} communities, "
        f"{main['big_communities']} of them large. Grouping institutions by "
        f"country gives modularity {float(main['modularity_country']):.2f}; "
        f"the communities reach {float(main['modularity']):.2f}, so they "
        "describe collaboration better than country alone.\n"
        "The communities are still strongly national: the French one is 90% "
        "French. But it is not purely national, because "
        f"{float(main['cross_country_share']) * 100:.0f}% of link weight "
        "crosses a border.\n"
        "CNRS is the main hub. Note that CNRS and Inserm are umbrella "
        "organisations, which inflates their centrality."))
    s.title("RQ3: Several communities, mostly national")
    img_h = 4700000
    img_w = img_h * 2600 / 2000
    picture(s, "rIdMap", rq3.MARGIN, 1300000, img_w, img_h)
    x = rq3.MARGIN + img_w + 250000
    w = rq3.SLIDE_W - rq3.MARGIN - x
    s.stat(x, 1300000, main["communities"],
           f"Louvain communities ({main['big_communities']} large) among "
           f"{int(main['nodes']):,} institutions", w=w, h=1500000)
    s.stat(x, 2950000, f"{float(main['modularity']):.2f}",
           f"modularity, vs {float(main['modularity_country']):.2f} for "
           "grouping by country", rq3.ORANGE, w=w, h=1500000)
    fr = by_country["FR"]
    pair_txt = ", ".join(
        f"{p['country_a']}-{p['country_b']} ({p['joint_papers']})"
        for p in pairs)
    s.text(x, 4600000, w, 1600000, [
        rq3.para(f"French-led community: {float(fr['purity']) * 100:.0f}% "
                 "French", 1300, rq3.INK, bullet=True),
        rq3.para(f"{float(main['cross_country_share']) * 100:.0f}% of link "
                 "weight crosses a border", 1300, rq3.INK, bullet=True),
        rq3.para(f"Top pairs: {pair_txt}", 1300, rq3.INK, bullet=True),
    ])
    s.footnote("Network: Keerthana, all 7,594 candidates. A cross-check on "
               "the 2,972 reviewed STRICT papers (John) gives the same "
               "pattern with finer splits.")
    return s


def slide_rq4():
    s = rq3.Slide("RQ4", notes=(
        "Mabango checked how good our search is. Precision is about 80%: "
        "one paper in five we collect is not really AI in education, "
        "mostly AI papers with no education link and patient education.\n"
        "Recall is the bigger problem. Against 200 papers that OpenAlex "
        "itself tags as AI in education, we found only 21%. Non-English "
        "papers are found at 11%.\n"
        "So our rankings are provisional, and countries that publish in "
        "their own language are probably under-counted."))
    s.title("RQ4: Our search misses most relevant work")
    s.text(rq3.MARGIN, 1463040, 7315200, 4389120, [
        rq3.para(t, 1600, rq3.INK, bullet=True) for t in (
            "Precision about 80% (95% CI 70.6-86.7%) on a 100-paper audit",
            "False positives: AI with no education link, patient education",
            "Recall about 21% (95% CI 15.9-27.2%) against 200 OpenAlex "
            "AI-in-education papers",
            "English papers found at 28%, non-English at 11%",
            "Misses use terms such as ChatGPT, chatbot, LLM and GenAI",
            "26-37% of works lost their country, by search",
        )])
    s.stat(8412480, 1554480, "80%", "precision (over-capture 20%)")
    s.stat(8412480, 3566160, "21%", "recall (under-capture 79%)",
           rq3.ORANGE)
    s.footnote("Search validation: Mabango. Recall is measured against a "
               "benchmark sample, not a complete list.")
    return s


def slide_close():
    s = rq3.Slide("Close", rq3.DARK, notes=(
        "To answer our question: no single institution or venue drives AI "
        "in education research in Europe. The field forms several "
        "collaboration communities, mostly national or regional, and the "
        "same research themes appear in all of them.\n"
        "The main limit is recall. With about a fifth of relevant papers "
        "found, rankings could change, especially for non-English work.\n"
        "Next we would widen the query, add UK, Swiss and Norwegian "
        "partners, and test other community settings. Thank you; we are "
        "happy to take questions."))
    s.title("Answers, limits and next steps", "FFFFFF")
    for x, head, colour, items in (
        (rq3.MARGIN, "What drives the field?", rq3.LIGHT_TEAL, (
            "No single institution or venue dominates (top institution: 1.3% "
            "of papers)",
            "Output grew more than sixfold from 2020 to 2025",
            "Several collaboration communities, mostly national or regional",
            "Topics cut across those communities",
            "Scopus listing filters venues, not relevance",
        )),
        (6309360, "Limits and next steps", rq3.LIGHT_ORANGE, (
            "Recall about 21%: rankings are provisional, non-English work "
            "under-counted",
            "EU27-only network may overstate national splits",
            "Text clusters are weak (silhouette about 0.01)",
            "2026 is a partial year; STRICT is provisional",
            "Next: widen the query, add UK, CH and NO, test other community "
            "settings",
        )),
    ):
        s.text(x, 1371600, 5303520, 450000, [
            rq3.para(head, 2200, colour, True, "Cambria")], "ctr")
        s.text(x, 1874520, 5303520, 4206240, [
            rq3.para(t, 1400, "FFFFFF", bullet=True) for t in items])
    return s


def main():
    with zipfile.ZipFile(SRC) as zin:
        files = {n: zin.read(n) for n in zin.namelist() if not n.endswith("/")}

    # drop Dev's unused slides with their notes, charts and embedded sheets
    for n in DROP:
        rels = files.pop(f"ppt/slides/_rels/slide{n}.xml.rels").decode()
        for chart in re.findall(r'Target="(?:\.\.|/ppt)/charts/(chart\d+)\.xml"', rels):
            crel = files.pop(f"ppt/charts/_rels/{chart}.xml.rels").decode()
            for emb in re.findall(r'Target="(?:\.\.|/ppt)/embeddings/([^"]+)"', crel):
                files.pop(f"ppt/embeddings/{emb}")
            files.pop(f"ppt/charts/{chart}.xml")
        files.pop(f"ppt/slides/slide{n}.xml")
        files.pop(f"ppt/notesSlides/notesSlide{n}.xml")
        files.pop(f"ppt/notesSlides/_rels/notesSlide{n}.xml.rels")

    s1 = files["ppt/slides/slide1.xml"].decode("utf-8")
    old = re.search(r"Descriptive analysis: RQ1[^<]*", s1).group(0)
    s1 = s1.replace(old, "RQ1-RQ2 who leads and growth  |  RQ3 communities "
                         "and topics  |  RQ4 search validation")
    files["ppt/slides/slide1.xml"] = s1.encode("utf-8")

    d = rq3.load()
    new = [
        ("network", slide_network()),
        ("themes", rq3.slide_themes(d)),
        ("quality", rq3.slide_quality(d)),
        ("crosswalk", rq3.slide_crosswalk(d)),
        ("rq4", slide_rq4()),
        ("close", slide_close()),
    ]
    files["ppt/media/keerthana_network_map.png"] = MAP_PNG.read_bytes()

    order = [f"slide{n}.xml" for n in KEEP]
    for k, (_, slide) in enumerate(new):
        num = 20 + k
        name = f"slide{num}.xml"
        order.append(name)
        files[f"ppt/slides/{name}"] = slide.xml().encode("utf-8")
        img = (
            f'<Relationship Id="rIdMap" Type="{REL}/image" '
            'Target="../media/keerthana_network_map.png"/>'
            if "rIdMap" in slide.xml() else ""
        )
        files[f"ppt/slides/_rels/{name}.rels"] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/'
            f'2006/relationships"><Relationship Id="rId1" Type="{REL}/'
            'slideLayout" Target="../slideLayouts/slideLayout1.xml"/>'
            f'<Relationship Id="rId2" Type="{REL}/notesSlide" '
            f'Target="../notesSlides/notesSlide{num}.xml"/>{img}'
            "</Relationships>"
        ).encode("utf-8")
        files[f"ppt/notesSlides/notesSlide{num}.xml"] = rq3.notes_xml(
            len(order), slide.notes).encode("utf-8")
        files[f"ppt/notesSlides/_rels/notesSlide{num}.xml.rels"] = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/'
            f'2006/relationships"><Relationship Id="rId1" Type="{REL}/'
            'notesMaster" Target="../notesMasters/notesMaster1.xml"/>'
            f'<Relationship Id="rId2" Type="{REL}/slide" '
            f'Target="../slides/{name}"/></Relationships>'
        ).encode("utf-8")

    # presentation.xml: new slide list
    prel = files["ppt/_rels/presentation.xml.rels"].decode("utf-8")
    prel = re.sub(r'<Relationship Id="rId\d+" Type="[^"]*/slide" '
                  r'Target="slides/[^"]*"/>', "", prel)
    prel = prel.replace("</Relationships>", "".join(
        f'<Relationship Id="rIdS{i}" Type="{REL}/slide" '
        f'Target="slides/{name}"/>' for i, name in enumerate(order, 1)
    ) + "</Relationships>")
    files["ppt/_rels/presentation.xml.rels"] = prel.encode("utf-8")
    pres = files["ppt/presentation.xml"].decode("utf-8")
    ids = "".join(f'<p:sldId id="{300 + i}" r:id="rIdS{i}"/>'
                  for i in range(1, len(order) + 1))
    pres = re.sub(r"<p:sldIdLst>.*?</p:sldIdLst>",
                  f"<p:sldIdLst>{ids}</p:sldIdLst>", pres, flags=re.DOTALL)
    files["ppt/presentation.xml"] = pres.encode("utf-8")

    # content types: only parts that exist
    ct = files["[Content_Types].xml"].decode("utf-8")
    ct = re.sub(r'<Override PartName="/ppt/(slides|notesSlides|charts)/'
                r'[^"]+"[^>]*/>', "", ct)
    ct = re.sub(r'<Override PartName="/ppt/slideMasters/slideMaster'
                r'(?!1\.xml)[^"]+"[^>]*/>', "", ct)
    add = []
    for name in files:
        if re.match(r"ppt/slides/slide\d+\.xml$", name):
            add.append((name, PML + "slide+xml"))
        elif re.match(r"ppt/notesSlides/notesSlide\d+\.xml$", name):
            add.append((name, PML + "notesSlide+xml"))
        elif re.match(r"ppt/charts/chart\d+\.xml$", name):
            add.append((name, "application/vnd.openxmlformats-"
                              "officedocument.drawingml.chart+xml"))
    ct = ct.replace("</Types>", "".join(
        f'<Override PartName="/{n}" ContentType="{t}"/>' for n, t in add
    ) + "</Types>")
    files["[Content_Types].xml"] = ct.encode("utf-8")

    app = files["docProps/app.xml"].decode("utf-8")
    app = re.sub(r"<Slides>\d+</Slides>", f"<Slides>{len(order)}</Slides>",
                 app)
    app = re.sub(r"<Notes>\d+</Notes>", f"<Notes>{len(order)}</Notes>", app)
    files["docProps/app.xml"] = app.encode("utf-8")
    core = files["docProps/core.xml"].decode("utf-8")
    files["docProps/core.xml"] = core.replace(
        "Project D: RQ1 and RQ2", "Project D: final presentation"
    ).encode("utf-8")

    DST.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as zout:
        zout.writestr("[Content_Types].xml", files.pop("[Content_Types].xml"))
        for name, data in files.items():
            zout.writestr(name, data)
    print(f"wrote {DST} with {len(order)} slides")
    for w in rq3.WARNINGS:
        print("WARNING:", w)


if __name__ == "__main__":
    main()
