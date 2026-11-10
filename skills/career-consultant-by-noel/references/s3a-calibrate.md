# S3a · Calibrate

Goal: a scoring rubric the user has confirmed, saved in the **Search preferences** block of the context file. Run this on a first scan (from S2) or when the user wants to change their job search preferences. Don't run a scan from here.

## Calibrate ⏸

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

Write the confirmed rubric (weights, anchors and hard filters) into the **Search preferences** block of the context file. S3b scores from that block.

Then return to the state that called this one (S2 continues the scan), or stop if the user only wanted to recalibrate.

## Standing rules
Use only facts in `00_Career Twin.md` — ask rather than invent a number. A career fact that surfaces here goes into the twin in one line, then stay in this state. Never send, submit, accept or decline anything for the user — draft only. Research people and companies from public professional sources only. Never write ID numbers, bank details or passwords into any file. Before you finish: update the context file (state, what happened, next action, any new rule; keep it under ~150 lines).
