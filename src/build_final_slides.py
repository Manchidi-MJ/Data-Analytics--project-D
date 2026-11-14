"""Build the final presentation deck from Dev's RQ1/RQ2 deck.

Standard library only. Keeps Dev's slides 1-8 (updating the title-slide
subtitle), inserts four slides for RQ3 and RQ4 before the closing slide and
rewrites the closing slide as project-wide answers, limits and next steps.

    python src/build_final_slides.py

Input : project-d/ProjectD_RQ1_RQ2_slides.pptx   (unchanged)
Output: project-d/ProjectD_final_slides.pptx
"""

import re
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

SRC = Path("project-d/ProjectD_RQ1_RQ2_slides.pptx")
DST = Path("project-d/ProjectD_final_slides.pptx")

DARK, TEAL, ORANGE, INK, CARD, MUTED = (
    "12343B", "2C6E63", "D1603D", "1F2A2E", "EAF1EF", "5C6B70",
)
NS = (
    'xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
    'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/'
    'relationships" '
    'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
)
FONT = (
    '<a:latin typeface="{f}" pitchFamily="34" charset="0"/>'
    '<a:ea typeface="{f}" pitchFamily="34" charset="-122"/>'
    '<a:cs typeface="{f}" pitchFamily="34" charset="-120"/>'
)


class Slide:
    def __init__(self, name, bg="FFFFFF"):
        self.name, self.bg, self.shapes, self.next_id = name, bg, [], 2

    def _id(self):
        self.next_id += 1
        return self.next_id - 1

    def text(self, x, y, w, h, paras, anchor="t"):
        """paras: list of dicts(text, size, bold, colour, font, bullet)."""
        body = []
        for para in paras:
            size = para.get("size", 1600)
            bold = ' b="1"' if para.get("bold") else ""
            font = FONT.format(f=para.get("font", "Calibri"))
            if para.get("bullet"):
                ppr = (
                    '<a:pPr marL="342900" indent="-342900"><a:spcAft>'
                    '<a:spcPts val="1000"/></a:spcAft><a:buSzPct '
                    'val="100000"/><a:buChar char="&#x2022;"/></a:pPr>'
                )
            else:
                ppr = (
                    '<a:pPr indent="0" marL="0"><a:spcAft><a:spcPts '
                    'val="600"/></a:spcAft><a:buNone/></a:pPr>'
                )
            body.append(
                f"<a:p>{ppr}<a:r><a:rPr lang=\"en-US\" sz=\"{size}\"{bold} "
                f'dirty="0"><a:solidFill><a:srgbClr val="{para["colour"]}"/>'
                f"</a:solidFill>{font}</a:rPr><a:t>{escape(para['text'])}"
                f'</a:t></a:r><a:endParaRPr lang="en-US" sz="{size}" '
                f'dirty="0"/></a:p>'
            )
        i = self._id()
        self.shapes.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Text {i}"></p:cNvPr>'
            f'<p:cNvSpPr txBox="1"/><p:nvPr></p:nvPr></p:nvSpPr><p:spPr>'
            f'<a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/>'
            f'</a:xfrm><a:prstGeom prst="rect"><a:avLst></a:avLst>'
            f'</a:prstGeom><a:noFill/><a:ln></a:ln></p:spPr><p:txBody>'
            f'<a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" '
            f'rtlCol="0" anchor="{anchor}"></a:bodyPr><a:lstStyle/>'
            f'{"".join(body)}</p:txBody></p:sp>'
        )

    def card(self, x, y, w, h):
        i = self._id()
        self.shapes.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Shape {i}"></p:cNvPr>'
            f'<p:cNvSpPr/><p:nvPr></p:nvPr></p:nvSpPr><p:spPr><a:xfrm>'
            f'<a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm>'
            f'<a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" '
            f'fmla="val 6316"/></a:avLst></a:prstGeom><a:solidFill>'
            f'<a:srgbClr val="{CARD}"/></a:solidFill><a:ln w="12700">'
            f'<a:solidFill><a:srgbClr val="{CARD}"/></a:solidFill>'
            f'<a:prstDash val="solid"/></a:ln></p:spPr></p:sp>'
        )

    def title(self, text, colour=DARK):
        self.text(548640, 365760, 11064240, 822960, [
            dict(text=text, size=3400, bold=True, colour=colour,
                 font="Cambria")], anchor="ctr")

    def stat(self, x, y, big, label, colour=TEAL):
        self.card(x, y, 3200400, 1737360)
        self.text(x + 228600, y + 182880, 2743200, 868680, [
            dict(text=big, size=4400, bold=True, colour=colour,
                 font="Cambria")], anchor="ctr")
        self.text(x + 228600, y + 1005840, 2743200, 640080, [
            dict(text=label, size=1400, colour=INK)])

    def bullets(self, x, y, w, h, items, colour=INK, size=1600):
        self.text(x, y, w, h, [
            dict(text=t, size=size, colour=colour, bullet=True)
            for t in items
        ])

    def footnote(self, text, colour=MUTED):
        self.text(548640, 6217920, 11064240, 400000, [
            dict(text=text, size=1200, colour=colour)])

    def xml(self):
        return (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f"<p:sld {NS}><p:cSld name=\"{self.name}\"><p:bg><p:bgPr>"
            f'<a:solidFill><a:srgbClr val="{self.bg}"/></a:solidFill>'
            "</p:bgPr></p:bg><p:spTree><p:nvGrpSpPr><p:cNvPr id=\"1\" "
            'name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr>'
            '<a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>'
            '<a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm>'
            f'</p:grpSpPr>{"".join(self.shapes)}</p:spTree></p:cSld>'
            "<p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>"
        )


def build_slides():
    left_w, right_x = 7315200, 8412480

    s10 = Slide("Slide 10")
    s10.title("RQ3: Topic clusters are broad and overlap")
    s10.bullets(548640, 1463040, left_w, 4389120, [
        "TF-IDF + KMeans on titles and abstracts, k tested from 4 to 10",
        "Manual review of 125 health-heavy records removed 123 as out of "
        "scope, leaving 2,972 papers and k=5",
        "Generative AI in higher education (32%) and broad foundations and "
        "policy (28%) are the largest themes",
        "Smaller themes: ML and student performance (22%), health crossover "
        "(11%), intelligent tutoring (7%)",
        "Method check: silhouette 0.013 vs -0.012 for grouping by country. "
        "A small edge, and both are near zero",
    ])
    s10.stat(right_x, 1554480, "0.013", "silhouette, topic clusters")
    s10.stat(right_x, 3566160, "-0.012", "silhouette, country baseline",
             ORANGE)
    s10.footnote("Read the clusters as overlapping themes, not validated "
                 "topic categories.")

    s11 = Slide("Slide 11")
    s11.title("RQ3: Several collaboration communities, mostly national")
    s11.bullets(548640, 1463040, left_w, 4389120, [
        "1,641 EU27 institutions, 7,557 co-authorship ties, 139 with no EU27 "
        "collaborator",
        "Louvain finds 46 communities; 16 are large (90+ papers each)",
        "71% of ties stay inside a community",
        "Big communities follow countries: France 118 of 140 institutions, "
        "Italy 89 of 129, Spain 68 of 119, Portugal 56 of 89",
        "A few mix countries (communities 2, 6, 9 and 12)",
    ])
    s11.stat(right_x, 1554480, "46", "communities (modularity 0.64)")
    s11.stat(right_x, 3566160, "71%", "of ties inside a community", ORANGE)
    s11.footnote("Louvain maximises within-community ties, so this shows a "
                 "clear split, not a natural boundary. EU27 scope only.")

    s12 = Slide("Slide 12")
    s12.title("RQ3: Topics cut across the communities")
    s12.bullets(548640, 1463040, left_w, 4389120, [
        "Each paper placed in the community of its institutions "
        "(2,772 of 2,972 papers)",
        "Topic cluster vs network community: almost no overlap",
        "Community vs country: much stronger overlap",
        "Every community contains all five topics, so the same themes, such "
        "as generative AI in higher education, are studied in many countries "
        "by groups that rarely co-author",
        "A country-based story such as \"Spain does X\" is not supported",
    ])
    s12.stat(right_x, 1554480, "0.03", "NMI, topic cluster vs community")
    s12.stat(right_x, 3566160, "0.45", "NMI, community vs country", ORANGE)
    s12.footnote("NMI: 0 means unrelated partitions, 1 means identical.")

    s13 = Slide("Slide 13")
    s13.title("RQ4: Our search misses most relevant work")
    s13.bullets(548640, 1463040, left_w, 4389120, [
        "Precision about 80% (95% CI 70.6-86.7%) on a 100-paper audit",
        "False positives: AI papers with no education link, patient "
        "education",
        "Recall about 21% (95% CI 15.9-27.2%) against 200 OpenAlex "
        "AI-in-education papers",
        "English papers found at 28%, non-English at 11%",
        "Misses use terms such as ChatGPT, chatbot, LLM and GenAI",
        "22-37% of works lost their country",
    ])
    s13.stat(right_x, 1554480, "80%", "precision (over-capture 20%)")
    s13.stat(right_x, 3566160, "21%", "recall (under-capture 79%)", ORANGE)
    s13.footnote("Recall is against a benchmark sample, not a complete list "
                 "of relevant papers.")

    last = Slide("Slide 9", bg=DARK)
    last.title("Answers, limits and next steps", "FFFFFF")
    last.text(548640, 1371600, 5303520, 365760, [
        dict(text="What drives the field?", size=2200, bold=True,
             colour="9CC9BF", font="Cambria")], anchor="ctr")
    last.bullets(548640, 1874520, 5303520, 4206240, [
        "No single institution or venue dominates (top institution: 1.3% of "
        "papers)",
        "Several collaboration communities, mostly national or regional",
        "Topics cut across those communities",
        "Output grew more than sixfold from 2020 to 2025",
        "Scopus listing filters venues, not relevance",
    ], colour="FFFFFF", size=1400)
    last.text(6309360, 1371600, 5303520, 365760, [
        dict(text="Limits and next steps", size=2200, bold=True,
             colour="F3A58C", font="Cambria")], anchor="ctr")
    last.bullets(6309360, 1874520, 5303520, 4206240, [
        "Recall about 21%: rankings are provisional, and non-English work is "
        "under-counted",
        "EU27-only network may overstate fragmentation",
        "Text clusters are weak (silhouette about 0.01)",
        "2026 is a partial year; STRICT is provisional",
        "Next: widen the search (ChatGPT, LLM, non-English terms), include UK, "
        "CH and NO, test other community settings",
    ], colour="FFFFFF", size=1400)
    return [s10, s11, s12, s13], last


def main():
    new_slides, last = build_slides()
    with zipfile.ZipFile(SRC) as zin:
        files = {n: zin.read(n) for n in zin.namelist()}

    # title slide: cover the whole project
    s1 = files["ppt/slides/slide1.xml"].decode("utf-8")
    old = re.search(r"Descriptive analysis: RQ1[^<]*", s1).group(0)
    s1 = s1.replace(
        old,
        "RQ1-RQ2 descriptive analysis  |  RQ3 clusters and communities  |  "
        "RQ4 search validation",
    )
    files["ppt/slides/slide1.xml"] = s1.encode("utf-8")

    # closing slide: keep its notes/rels, replace the content
    files["ppt/slides/slide9.xml"] = last.xml().encode("utf-8")
    notes = files["ppt/notesSlides/notesSlide9.xml"].decode("utf-8")
    files["ppt/notesSlides/notesSlide9.xml"] = notes.encode("utf-8")

    rels_slide = (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/'
        '2006/relationships"><Relationship Id="rId1" Type="http://schemas.'
        "openxmlformats.org/officeDocument/2006/relationships/slideLayout\" "
        'Target="../slideLayouts/slideLayout1.xml"/></Relationships>'
    )
    ct = files["[Content_Types].xml"].decode("utf-8")
    pres = files["ppt/presentation.xml"].decode("utf-8")
    prel = files["ppt/_rels/presentation.xml.rels"].decode("utf-8")

    new_ids, new_rids = [], []
    for k, slide in enumerate(new_slides):
        n = 10 + k
        files[f"ppt/slides/slide{n}.xml"] = slide.xml().encode("utf-8")
        files[f"ppt/slides/_rels/slide{n}.xml.rels"] = rels_slide.encode()
        ct = ct.replace(
            "</Types>",
            f'<Override PartName="/ppt/slides/slide{n}.xml" ContentType='
            '"application/vnd.openxmlformats-officedocument.presentationml.'
            'slide+xml"/></Types>',
        )
        rid = f"rId{100 + k}"
        prel = prel.replace(
            "</Relationships>",
            f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.'
            f'org/officeDocument/2006/relationships/slide" Target="slides/'
            f'slide{n}.xml"/></Relationships>',
        )
        new_ids.append(f'<p:sldId id="{270 + k}" r:id="{rid}"/>')
        new_rids.append(rid)

    # order: slides 1-8, new slides, closing slide
    marker = '<p:sldId id="264" r:id="rId10"/>'
    assert marker in pres
    pres = pres.replace(marker, "".join(new_ids) + marker)

    files["[Content_Types].xml"] = ct.encode("utf-8")
    files["ppt/presentation.xml"] = pres.encode("utf-8")
    files["ppt/_rels/presentation.xml.rels"] = prel.encode("utf-8")

    app = files["docProps/app.xml"].decode("utf-8")
    app = app.replace("<Slides>9</Slides>", "<Slides>13</Slides>")
    files["docProps/app.xml"] = app.encode("utf-8")

    DST.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(DST, "w", zipfile.ZIP_DEFLATED) as zout:
        # [Content_Types].xml first, as the format expects
        zout.writestr("[Content_Types].xml", files.pop("[Content_Types].xml"))
        for name, data in files.items():
            zout.writestr(name, data)
    print(f"wrote {DST} with {8 + len(new_slides) + 1} slides")


if __name__ == "__main__":
    main()
