# S3 · Calibrate, score and shortlist

Three jobs in this state:
- calibrate the rubric with the user
- score roles consistently
- learn from what the user keeps and removes

## Contents
- 3.1 Calibrate ⏸
- 3.2 Score
- 3.3 Present the top 10 ⏸
- 3.4 Learn from keep/remove

## 3.1 Calibrate ⏸

**When recalibrating**, start from the current Search preferences in the context file, and ask only about what the user's message leaves open. Often you can go straight to the recommendation. Making someone re-answer six questions to change one priority is the opposite of helpful.

**On a first calibration**, ask up to six short questions. Use multiple choice where the interface allows it.

1. Rank what matters most: career growth, compensation, work-life balance, stability, learning, brand or prestige.
2. Business role, technical role, or a hybrid?
3. Target titles or functions, and any titles to avoid.
4. Locations, remote or hybrid preference, and any visa or relocation constraints.
5. Current compensation baseline, and the smallest step up worth moving for.
6. Deal-breakers: industries, company size or stage, travel, management style.

Then **recommend** a rubric, compactly. Start from the default four parameters below and re-weight them by the user's ranking. Add or swap a parameter when the answers call for it. For example, "work-life balance first" earns its own parameter, at 20–30%, scored from work-life ratings and hours signals in the JD. Weights sum to 100.

| Parameter | Measures | 90+ looks like | Under 50 looks like |
|---|---|---|---|
| Fit | How much of the JD the twin proves | Proves ≥80% of must-haves, no hard gaps | Misses a hard gate (licence, language, required years or domain) |
| Compensation | Posted or estimated band vs baseline + target uplift | Band clearly above the target uplift | Below the current baseline |
| Career growth | Title and scope step, exec exposure, brand value for the next move, sector momentum | Clear step up in title and scope | Sideways or down |
| Workplace | Overall rating, management sub-rating, work-life signals | ≥4.2 overall with strong management reviews | Under 3.3, or poor management reviews |

The rating thresholds are defaults. Adjust them for the user's market.

**Explain how fit is determined**:

1. Extract the JD's must-haves and nice-to-haves.
2. Match each one to twin evidence:
   - ✅ proven = 1
   - 🟡 adjacent = 0.5
   - 🔴 missing = 0
3. Fit = 100 × (2 × must-have credit + nice-to-have credit) ÷ (2 × number of must-haves + number of nice-to-haves).
4. If a hard-gate must-have is 🔴, cap fit at 45.

Hard filters exclude a role outright; they aren't scored. Examples: wrong location, below the comp floor, a named deal-breaker.

Ask the user to confirm or adjust. Then tell them: *"You can recalibrate any time. Start a new chat in this Project and say 'change my job search preferences'."*

Write the confirmed rubric into the **Search preferences** block of the context file.

## 3.2 Score

For each candidate:

1. **Score each parameter 0–100** against the anchors.
2. **Fill missing data honestly.**
   - **No posted band:** estimate it from comparable postings or salary sites, and label it "est." with the source.
   - **Nothing credible available:** score 50 and label it "n/a". A made-up number misleads more than an honest blank.
   - **Ratings:** treat them the same way.
3. **Compound** = Σ(weight × score) ÷ 100, rounded to a whole number.
4. **Apply learned rules** from the context file:
   - exclusions first
   - then nudges, each worth at most ±5, with a total of at most ±10
5. **Tie-break** on career growth, then fit.

## 3.3 Present the top 10 ⏸

Show only the top 10. The first scan is the user's first real impression of this system, so every entry should be specific enough that they learn something about the role they didn't know from its title.

**Quality bar.** Check every entry before showing it:
- The apply link has been opened, and the posting is still live.
- "What it is" comes from the body of the JD, not the title.
- "Why you" cites a specific twin item: a project, metric or skill.
- Scores come from the formula, and the source of the comp figure is labelled.
- There are no duplicates and no hard-filter violations.
- The risk line is honest. A list with no downsides reads as a sales pitch.

**Format:**

> **1. Senior Pricing Analyst · Contoso** · Singapore (hybrid) · **Compound 84** · [Apply](https://example.com/job)
> - **What it is:** owns list-price and discount guardrails for the APAC B2B catalogue; partners with sales ops on deal desk approvals.
> - **Why you:** your Fabrikam margin-leakage project (+2.1 pts gross margin) is this job's core problem.
> - **Scores:** Fit 88 · Comp 75 (posted S$9–11k/mo) · Growth 85 · Workplace 80 (management 3.9)
> - **Watch out:** asks for Tableau, and your twin only shows Power BI.

Finish with one line on the scan itself, for example "48 postings scanned, 31 after filters". Then ask: **"Which should I keep, and which should I drop? A reason for any drop helps me learn."** ⏸

## 3.4 Learn from keep/remove

1. **Add the keepers to the tracker.** Run `workspace.py add` for each, with step `Shortlisted`. Folders come later, in S4, when the user decides to apply.

2. **Turn patterns into learned rules.** A rule needs at least two decisions or a stated reason behind it, because one removal is an anecdote, not a preference. Write each rule into the context file with its evidence and the date:

   ```
   - [2026-11-08] Exclude: agency-posted roles (dropped 3 of 3; "no agencies")
   - [2026-11-08] Nudge +5: roles reporting to a C-level exec (kept 4 of 4)
   ```

   - Keep at most 10 active rules.
   - Retire a rule when a later decision contradicts it.

3. **Leave the user's weights alone.** They belong to the user. Learned rules only filter and nudge.

4. **Tell the user what changed**, in a short list: each rule added or removed, and why.

5. **Go to S9.** Show the tracker, and ask which job to help with first.
