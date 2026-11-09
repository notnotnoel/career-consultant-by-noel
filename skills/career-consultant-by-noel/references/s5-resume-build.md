# S5 · Tailored resume

Goal: a CV for one role that a busy reader can scan in 30 seconds, built only from twin facts, that can be regenerated whenever something changes.

**Inputs:**
- the twin
- the S4 priority criterion and fit table
- the JD in `00_JD/`

## Step 0: check for a locked format

Look in `99_All Files/00_Career Sources/` for `Resume Format Standard.md` and for a master resume the user has approved.

- **If either exists, follow the master-template path:**
  1. Copy the master `.docx` into `01_Custom Resume/` under the new file name.
  2. Replace the text paragraph by paragraph. Keep every style, the numbering, tables, borders, margins and fonts. Add or remove items by duplicating or deleting existing paragraphs of the same type, never by creating new formatting.
  3. Render to PDF and compare page 1 with the master's page 1: font, sizes, spacing, numbering and section order. Fix any difference before delivery.
  4. Then run the quality loops and truth gates below, and skip steps 1, 3 and 7.
- **If neither exists:** use the steps below. After the user approves a CV, offer to make it the master and write a `Resume Format Standard.md` from it (see `templates/Resume Format Standard.template.md`).

## Steps

1. **Write the content file.** Save it at `<role folder>/99_Claude scripts/resume_content.json`, following `templates/resume_content.example.json`.
   - Let the priority criterion decide order and depth. Experience that serves it gets full bullets. The rest is compressed or moved into `earlier_experience`.
   - Use the user's resume preferences from the twin: page limit, font, file naming.

2. **Write every bullet to this standard:**
   - Outcome and metric first, then how ("by …").
   - No more than two rendered lines.
   - Explicit units and currency: "S$4M", not "4M".
   - Strong, specific verbs. Avoid "helped" and "responsible for".
   - Use the JD's own terms where they're true.
   - Sound like the twin's Voice section.

3. **Build it.** Run:

   ```bash
   python scripts/build_resume.py "<role folder>/99_Claude scripts/resume_content.json" \
     --out "<role folder>/01_Custom Resume" --name "<YYYY-MM-DD>_<Initials>_Resume_<Company>_v1" --preview
   ```

   - The script writes the DOCX.
   - When LibreOffice is available, it also converts to PDF.
   - If the CV runs past `max_pages`, it steps the body font down 0.2 pt at a time (never below `min_body_pt`) until it fits.
   - It prints the page count, the final font size and any font substitution.
   - Bump the version number (v2, v3, …) on every rebuild after the user has seen a version.

4. **Look at it.** Open the preview PNGs and check:
   - spacing
   - overflow
   - lone lines at the top of page two
   - anything that looks broken

   Recruiters reject broken-looking CVs before reading a word.

5. **Run three loops before the user sees it:**
   - **ATS loop.** Every JD must-have keyword appears somewhere it's true. List any you couldn't place truthfully.
   - **Voice loop.** It reads like the user, with no generic filler such as "results-driven" or "dynamic".
   - **Line-standard loop.** Every bullet meets the standard in step 2.

6. **Truth gates:**
   - Every number traces to a twin line.
   - Tools and certifications appear only if the twin lists them as confirmed.
   - Certification names match the issuer's official naming.

7. **Check the font.** If the build reports a substitution, tell the user to export the final PDF from Word or Pages on their own machine, and to check that it still fits the page limit there.

Then go straight to **S6**.
