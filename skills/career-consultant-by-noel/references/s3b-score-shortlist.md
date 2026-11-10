# S3b · Score and shortlist

Goal: score scan results with the confirmed rubric, show the top 10, and learn from what the user keeps and removes.

If the context file has no confirmed **Search preferences**, run `references/s3a-calibrate.md` first.

## Contents
- 3.2 Score
- 3.3 Present the top 10 ⏸
- 3.4 Learn from keep/remove

## 3.2 Score

For each candidate:

1. **Score each parameter 0–100** against the anchors. The anchors are in the context file's Search preferences. For fit, match each JD must-have and nice-to-have to twin evidence (✅ = 1, 🟡 = 0.5, 🔴 = 0), then Fit = 100 × (2 × must-have credit + nice-to-have credit) ÷ (2 × number of must-haves + number of nice-to-haves). If a hard-gate must-have is 🔴, cap fit at 45.
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

## Standing rules
Use only facts in `00_Career Twin.md` — ask rather than invent a number. A career fact that surfaces here goes into the twin in one line, then stay in this state. Never send, submit, accept or decline anything for the user — draft only. Research people and companies from public professional sources only. Never write ID numbers, bank details or passwords into any file. Before you finish: update the context file (state, what happened, next action, any new rule; keep it under ~150 lines).
