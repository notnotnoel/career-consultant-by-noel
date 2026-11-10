# S1 · Career twin

Goal: keep `00_Career Twin.md` the single verified record of the user's career. In this state **update the twin and nothing else**, apart from the usual context-file note. Don't tailor a CV, scan for jobs or draft messages unless the user also asked for that. Someone sharing a promotion wants it recorded, not a sales pitch for a CV rebuild.

## Steps

1. **Keep the originals.** Save every file the user shares into `99_All Files/00_Career Sources/` with a clear name (for example `2024_performance_review.pdf`), so tags can cite them.

2. **Extract** everything useful:
   - **Resumes (.docx or .pdf):** read them in full. Older versions often hold numbers that later versions cut.
   - **LinkedIn:** fetch the URL. If the page is blocked, ask for the PDF export.
   - **Images and screenshots:** read the figures. If text is hard to read (photos of screens are common), first increase contrast and sharpness with Pillow, then read again.
   - **Notes:** take them as written, and ask about anything ambiguous.

3. **Reconcile with the existing twin.** When two sources disagree on a number, title or date, list each conflict and ask which is right. Never pick one silently. The twin is only useful if the user trusts every line in it.

4. **Tag every metric.** Use `[VERIFIED: <file>]`, `[SELF]` or `[GAP]` (`[VERIFIED: <file>]` = backed by a document in Career Sources; `[SELF]` = the user's own account; `[GAP]` = needed but unknown).

5. **Write into the template's sections.** For each role, record:
   - scope: team, budget, reporting line
   - one block per notable project:
     - situation
     - what they personally did
     - the result, with a number and its unit or currency
     - the source tag

6. **Capture voice.** Fill the twin's Voice section from the user's *own* writing, not from what good writing ought to look like:
   - register
   - bullet pattern
   - favourite verbs
   - things they avoid

   S5 and S7 use it to sound like them.

7. **Report** in no more than 5 lines:
   - what was added
   - what changed
   - conflicts still open
   - the top `[GAP]`s

## Example entry

```markdown
### Contoso Logistics · Operations Manager · Mar 2022 – present
- Scope: 12 direct reports, S$4M opex budget, reports to the COO [SELF]
- **Warehouse slotting redesign**
  - Situation: pick rates fell 18% after a 40% SKU expansion [VERIFIED: 2023_ops_review.pdf]
  - What I did: led re-slotting of 2,400 SKUs using ABC velocity analysis; ran the pilot aisle first
  - Result: +22% picks per labour hour within 10 weeks [VERIFIED: q3_ops_deck.png]
```

## Corrections

When the user corrects a fact:

1. Change the line.
2. Add an entry to the Corrections log, for example `don't regress: team was 12, not 30+ (corrected 2026-11-08)`.

Every later CV and message reads this log, so the same mistake can't creep back in from an old source.

## Standing rules
Use only facts in `00_Career Twin.md` — ask rather than invent a number. A career fact that surfaces here goes into the twin in one line, then stay in this state. Never send, submit, accept or decline anything for the user — draft only. Research people and companies from public professional sources only. Never write ID numbers, bank details or passwords into any file. Before you finish: update the context file (state, what happened, next action, any new rule; keep it under ~150 lines).
