#!/usr/bin/env python3
"""Build a tailored resume (DOCX, plus PDF when LibreOffice is available) from a JSON content file.

Usage:
  python build_resume.py CONTENT.json --out DIR --name FILE_STEM [--no-pdf] [--preview]

Writes DIR/FILE_STEM.docx and, when LibreOffice is installed, DIR/FILE_STEM.pdf. With a PDF it
checks the page count and steps every font size down by 0.2 pt (never below layout.min_body_pt)
until the resume fits layout.max_pages. --preview renders each page to a PNG in a temporary
folder (needs pdftoppm) so you can look at the result before sharing it.

Content format: see templates/resume_content.example.json. Any text field accepts **bold** and
[label](https://link). Requires python-docx (pip install python-docx); pypdf is optional.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

try:
    from docx import Document
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_TAB_ALIGNMENT
    from docx.opc.constants import RELATIONSHIP_TYPE as RT
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Cm, Pt, RGBColor
except ImportError:
    sys.exit("python-docx is required. Install it with: pip install python-docx")

PAPER_CM = {"A4": (21.0, 29.7), "LETTER": (21.59, 27.94)}
DEFAULT_LAYOUT = {
    "paper": "A4",
    "font": "Georgia",
    "body_pt": 10.5,
    "min_body_pt": 9.4,
    "max_pages": 2,
    "margins_cm": 1.8,
    "accent_hex": "1F3864",
    "section_order": ["profile", "skills", "experience", "education", "additional"],
    "titles": {"profile": "Profile", "skills": "Skills", "experience": "Experience",
               "earlier": "Earlier experience", "education": "Education"},
}
SECTIONS = {"profile", "skills", "experience", "education", "additional"}
STEP_PT = 0.2
INLINE = re.compile(r"(\*\*.+?\*\*|\[[^\]]+\]\([^)\s]+\))")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)\)")
EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
# Elements that must follow w:pBdr inside w:pPr (OOXML schema order).
PBDR_SUCCESSORS = ("w:shd", "w:tabs", "w:suppressAutoHyphens", "w:kinsoku", "w:wordWrap",
                   "w:overflowPunct", "w:topLinePunct", "w:autoSpaceDE", "w:autoSpaceDN",
                   "w:bidi", "w:adjustRightInd", "w:snapToGrid", "w:spacing", "w:ind",
                   "w:contextualSpacing", "w:mirrorIndents", "w:suppressOverlap", "w:jc",
                   "w:textDirection", "w:textAlignment", "w:textboxTightWrap", "w:outlineLvl",
                   "w:divId", "w:cnfStyle", "w:rPr", "w:sectPr", "w:pPrChange")


def load_content(path):
    try:
        content = json.loads(Path(path).read_text(encoding="utf-8"))
    except FileNotFoundError:
        sys.exit(f"Content file not found: {path}")
    except json.JSONDecodeError as exc:
        sys.exit(f"{path} is not valid JSON: line {exc.lineno}, column {exc.colno}: {exc.msg}")
    layout = {**DEFAULT_LAYOUT, **content.get("layout", {})}
    layout["titles"] = {**DEFAULT_LAYOUT["titles"], **content.get("layout", {}).get("titles", {})}
    errors = validate(content, layout)
    if errors:
        sys.exit("Fix the content file first:\n- " + "\n- ".join(errors))
    return content, layout


def validate(content, layout):
    errors = []
    if not (content.get("header") or {}).get("name"):
        errors.append("header.name is required")
    if layout["paper"].upper() not in PAPER_CM:
        errors.append("layout.paper must be A4 or Letter")
    if not re.fullmatch(r"[0-9A-Fa-f]{6}", str(layout["accent_hex"])):
        errors.append("layout.accent_hex must be six hex digits, for example 1F3864")
    if layout["min_body_pt"] > layout["body_pt"]:
        errors.append("layout.min_body_pt must not be larger than layout.body_pt")
    unknown = [s for s in layout["section_order"] if s not in SECTIONS]
    if unknown:
        errors.append(f"layout.section_order has unknown sections {unknown}; use {sorted(SECTIONS)}")
    columns = (content.get("skills") or {}).get("columns", [])
    if len(columns) > 4:
        errors.append("skills.columns: use at most 4 columns")
    for i, col in enumerate(columns):
        if not col.get("title") or not isinstance(col.get("items"), list):
            errors.append(f"skills.columns[{i}] needs a title and an items list")
    for i, job in enumerate(content.get("experience", [])):
        for key in ("employer", "title"):
            if not job.get(key):
                errors.append(f"experience[{i}].{key} is required")
        for j, bullet in enumerate(job.get("bullets", [])):
            if isinstance(bullet, dict):
                if not bullet.get("text"):
                    errors.append(f"experience[{i}].bullets[{j}].text is required")
            elif not isinstance(bullet, str):
                errors.append(f"experience[{i}].bullets[{j}] must be text or {{text, sub}}")
    for i, block in enumerate(content.get("additional", [])):
        if not block.get("title") or not isinstance(block.get("items"), list):
            errors.append(f"additional[{i}] needs a title and an items list")
    return errors


class ResumeBuilder:
    def __init__(self, content, layout, body_pt):
        self.content, self.layout, self.body = content, layout, body_pt
        self.accent = RGBColor.from_string(layout["accent_hex"].upper())
        self.muted = RGBColor(0x55, 0x55, 0x55)
        self.doc = Document()
        self._page_setup()

    # ----- setup -----
    def _page_setup(self):
        width, height = PAPER_CM[self.layout["paper"].upper()]
        margin = self.layout["margins_cm"]
        section = self.doc.sections[0]
        section.page_width, section.page_height = Cm(width), Cm(height)
        for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
            setattr(section, side, Cm(margin))
        self.text_width = Cm(width - 2 * margin)
        font = self.layout["font"]
        for name in ("Normal", "List Bullet", "List Bullet 2"):
            style = self.doc.styles[name]
            style.font.name = font
            style.font.size = Pt(self.body)
            rfonts = style.element.get_or_add_rPr().get_or_add_rFonts()
            for attr in ("w:ascii", "w:hAnsi", "w:eastAsia", "w:cs"):
                rfonts.set(qn(attr), font)
            fmt = style.paragraph_format
            fmt.space_before, fmt.space_after, fmt.line_spacing = Pt(0), Pt(0), 1.0
            if name != "Normal":
                fmt.space_after = Pt(1.5)

    # ----- text primitives -----
    def run(self, para, text, size=None, bold=False, italic=False, color=None):
        run = para.add_run(text)
        run.font.size = Pt(size or self.body)
        run.bold = True if bold else None
        run.italic = True if italic else None
        if color is not None:
            run.font.color.rgb = color
        return run

    def link(self, para, label, url, size=None):
        if EMAIL.match(url):
            url = "mailto:" + url
        rel_id = para.part.relate_to(url, RT.HYPERLINK, is_external=True)
        hyperlink = OxmlElement("w:hyperlink")
        hyperlink.set(qn("r:id"), rel_id)
        run = OxmlElement("w:r")
        rpr = OxmlElement("w:rPr")
        for tag, val in (("w:color", "0563C1"), ("w:sz", str(round((size or self.body) * 2))), ("w:u", "single")):
            el = OxmlElement(tag)
            el.set(qn("w:val"), val)
            rpr.append(el)
        text = OxmlElement("w:t")
        text.text = label
        text.set(qn("xml:space"), "preserve")
        run.append(rpr)
        run.append(text)
        hyperlink.append(run)
        para._p.append(hyperlink)

    def rich(self, para, text, size=None, bold=False, italic=False, color=None):
        for part in INLINE.split(text):
            if not part:
                continue
            match = LINK.fullmatch(part)
            if match:
                self.link(para, match.group(1), match.group(2), size)
            elif part.startswith("**") and part.endswith("**") and len(part) > 4:
                self.run(para, part[2:-2], size, True, italic, color)
            else:
                self.run(para, part, size, bold, italic, color)

    def two_sided(self, left, right="", left_bold=True, left_italic=False, right_italic=False, keep=True):
        para = self.doc.add_paragraph()
        para.paragraph_format.tab_stops.add_tab_stop(self.text_width, WD_TAB_ALIGNMENT.RIGHT)
        para.paragraph_format.keep_with_next = keep
        self.rich(para, left, bold=left_bold, italic=left_italic)
        if right:
            self.run(para, "\t" + right, self.body - 0.5, italic=right_italic, color=self.muted)
        return para

    def heading(self, title):
        para = self.doc.add_paragraph()
        fmt = para.paragraph_format
        fmt.space_before, fmt.space_after, fmt.keep_with_next = Pt(self.body * 0.9), Pt(2.5), True
        self.run(para, title.upper(), self.body + 0.5, bold=True, color=self.accent)
        border = OxmlElement("w:pBdr")
        bottom = OxmlElement("w:bottom")
        for attr, val in (("w:val", "single"), ("w:sz", "6"), ("w:space", "1"),
                          ("w:color", self.layout["accent_hex"].upper())):
            bottom.set(qn(attr), val)
        border.append(bottom)
        para._p.get_or_add_pPr().insert_element_before(border, *PBDR_SUCCESSORS)

    def bullet(self, text, level=1):
        para = self.doc.add_paragraph(style="List Bullet" if level == 1 else "List Bullet 2")
        self.rich(para, text)

    # ----- sections -----
    def header(self):
        head = self.content["header"]
        name = self.doc.add_paragraph()
        self.run(name, head["name"], self.body + 9, bold=True, color=self.accent)
        if head.get("headline"):
            line = self.doc.add_paragraph()
            self.rich(line, head["headline"], self.body + 0.5, italic=True)
        contact = head.get("contact") or []
        if contact:
            line = self.doc.add_paragraph()
            line.paragraph_format.space_before = Pt(2)
            for i, item in enumerate(contact):
                if i:
                    self.run(line, "  ·  ", self.body - 0.5, color=self.muted)
                item = item.strip()
                if EMAIL.match(item):
                    self.link(line, item, item, self.body - 0.5)
                else:
                    self.rich(line, item, self.body - 0.5)

    def profile(self):
        text = self.content.get("profile")
        if text:
            self.heading(self.layout["titles"]["profile"])
            self.rich(self.doc.add_paragraph(), text)

    def skills(self):
        columns = (self.content.get("skills") or {}).get("columns", [])
        if not columns:
            return
        self.heading(self.layout["titles"]["skills"])
        table = self.doc.add_table(rows=1, cols=len(columns))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        width = int(self.text_width / len(columns))
        for cell, col in zip(table.rows[0].cells, columns):
            cell.width = width
            first = cell.paragraphs[0]
            first.paragraph_format.space_after = Pt(1)
            self.run(first, col["title"], self.body, bold=True, color=self.accent)
            for item in col["items"]:
                para = cell.add_paragraph()
                para.paragraph_format.left_indent = Pt(8)       # hanging indent keeps wrapped
                para.paragraph_format.first_line_indent = Pt(-8)  # lines aligned with the text
                self.rich(para, "• " + item, self.body - 0.5)

    def experience(self):
        jobs = self.content.get("experience", [])
        earlier = self.content.get("earlier_experience", [])
        if not jobs and not earlier:
            return
        self.heading(self.layout["titles"]["experience"])
        for i, job in enumerate(jobs):
            left = f"**{job['employer']}**" + (f", {job['location']}" if job.get("location") else "")
            first = self.two_sided(left, job.get("dates", ""), left_bold=False)
            if i:
                first.paragraph_format.space_before = Pt(self.body * 0.6)
            title = self.doc.add_paragraph()
            title.paragraph_format.keep_with_next = True
            self.rich(title, job["title"], italic=True)
            if job.get("summary"):
                summary = self.doc.add_paragraph()
                summary.paragraph_format.space_after = Pt(1.5)
                self.rich(summary, job["summary"], self.body - 0.5, color=self.muted)
            for bullet in job.get("bullets", []):
                if isinstance(bullet, dict):
                    self.bullet(bullet["text"])
                    for sub in bullet.get("sub", []):
                        self.bullet(sub, level=2)
                else:
                    self.bullet(bullet)
        if earlier:
            label = self.doc.add_paragraph()
            label.paragraph_format.space_before = Pt(self.body * 0.6)
            label.paragraph_format.keep_with_next = True
            self.run(label, self.layout["titles"]["earlier"], bold=True)
            for item in earlier:
                left = f"**{item['employer']}**" + (f", {item['title']}" if item.get("title") else "")
                self.two_sided(left, item.get("dates", ""), left_bold=False, keep=False)

    def education(self):
        schools = self.content.get("education", [])
        if not schools:
            return
        self.heading(self.layout["titles"]["education"])
        for school in schools:
            self.two_sided(f"**{school['school']}**", school.get("dates", ""), left_bold=False)
            if school.get("degree"):
                self.rich(self.doc.add_paragraph(), school["degree"], italic=True)
            if school.get("details"):
                self.rich(self.doc.add_paragraph(), school["details"], self.body - 0.5)

    def additional(self):
        for block in self.content.get("additional", []):
            self.heading(block["title"])
            for item in block["items"]:
                self.rich(self.doc.add_paragraph(), item)

    def build(self, path):
        self.header()
        for section in self.layout["section_order"]:
            getattr(self, section)()
        self.doc.save(str(path))


# ----- PDF helpers -----
def convert_to_pdf(docx_path):
    office = shutil.which("soffice") or shutil.which("libreoffice")
    if not office:
        return None, "LibreOffice isn't installed, so no PDF was made and the page count wasn't checked."
    with tempfile.TemporaryDirectory() as profile:
        cmd = [office, f"-env:UserInstallation={Path(profile).as_uri()}", "--headless",
               "--convert-to", "pdf", "--outdir", str(docx_path.parent), str(docx_path)]
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        except subprocess.TimeoutExpired:
            return None, "PDF conversion timed out after 3 minutes."
    pdf = docx_path.with_suffix(".pdf")
    if result.returncode != 0 or not pdf.exists():
        return None, f"PDF conversion failed: {(result.stderr or result.stdout).strip()[:300]}"
    return pdf, None


def count_pages(pdf):
    try:
        from pypdf import PdfReader
        return len(PdfReader(str(pdf)).pages)
    except ImportError:
        return len(re.findall(rb"/Type\s*/Page(?!s)", pdf.read_bytes()))


def font_substitution(font):
    matcher = shutil.which("fc-match")
    if not matcher:
        return None
    found = subprocess.run([matcher, font, "--format=%{family}"], capture_output=True, text=True).stdout
    family = found.split(",")[0].strip()
    if family and family.lower() != font.lower():
        return (f"'{font}' isn't installed here, so the PDF used '{family}' and page breaks may differ in Word. "
                "Export the final PDF from Word or Pages on your own machine and re-check the page count.")
    return None


def render_previews(pdf):
    renderer = shutil.which("pdftoppm")
    if not renderer:
        return [], "pdftoppm isn't installed, so no preview images were made."
    folder = Path(tempfile.mkdtemp(prefix="resume_preview_"))
    subprocess.run([renderer, "-png", "-r", "80", str(pdf), str(folder / pdf.stem)], check=False)
    return sorted(folder.glob("*.png")), None


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("content", help="resume content JSON")
    parser.add_argument("--out", required=True, help="output folder, for example '<role>/01_Custom Resume'")
    parser.add_argument("--name", required=True, help="file name without extension")
    parser.add_argument("--no-pdf", action="store_true", help="skip PDF conversion and the page check")
    parser.add_argument("--preview", action="store_true", help="render PNG previews of each page")
    args = parser.parse_args()

    content, layout = load_content(args.content)
    out_dir = Path(args.out).expanduser()
    out_dir.mkdir(parents=True, exist_ok=True)
    docx_path = out_dir / f"{args.name}.docx"
    notes, pdf, pages = [], None, None

    size = float(layout["body_pt"])
    while True:
        ResumeBuilder(content, layout, size).build(docx_path)
        if args.no_pdf:
            break
        pdf, error = convert_to_pdf(docx_path)
        if error:
            notes.append(error)
            break
        pages = count_pages(pdf)
        if pages <= layout["max_pages"]:
            break
        if size <= layout["min_body_pt"] + 1e-9:
            limit = layout["max_pages"]
            notes.append(f"Still {pages} pages at the minimum body size ({size:g} pt), over the limit of "
                         f"{limit} page{'s' if limit != 1 else ''}. Cut or compress content instead of "
                         "shrinking the text further.")
            break
        size = max(round(size - STEP_PT, 2), float(layout["min_body_pt"]))

    print(f"DOCX: {docx_path.resolve()}")
    if pdf:
        print(f"PDF:  {pdf.resolve()}")
        print(f"Pages: {pages} (limit {layout['max_pages']}) at body {size:g} pt")
        substitution = font_substitution(layout["font"])
        if substitution:
            notes.append(substitution)
        if args.preview:
            images, error = render_previews(pdf)
            if error:
                notes.append(error)
            for image in images:
                print(f"Preview: {image}")
    for note in notes:
        print(f"NOTE: {note}")


if __name__ == "__main__":
    main()
