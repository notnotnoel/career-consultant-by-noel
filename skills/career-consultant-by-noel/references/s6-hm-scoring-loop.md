# S6 · Hiring-manager scoring loop

Goal: read the CV the way the real readers will, before they do, and fix what they would object to. Tell the user once that this is a structured simulation, not a prediction of the outcome.

## Personas

Build 3–5 reader personas from the S4 research. Default weights:

| Persona | Weight | Reads for |
|---|---|---|
| Hiring manager | 35 | Can this person do the job from week one? |
| Business sponsor (skip-level) | 25 | Strategic value, and credibility with senior leaders |
| Peer or delivery partner | 20 | Will they be good to work with, and do they understand the work? |
| Recruiter screen | 20 | Keyword match, clarity, red flags (gaps, tenure, job-hopping) |

Adjust the set to the role. For example:
- add a technical interviewer for engineering roles
- add an investment committee member for private-equity roles

The weights must still sum to 100.

**Score anchors**, used by every persona:
- **90+:** would push for an interview immediately.
- **75–89:** strong yes.
- **60–74:** the maybe pile.
- **Under 60:** no.

## Loop

Run at most 5 iterations. Stop early once the compound score improves by less than 2 points twice in a row.

1. **Persona scores.** Each persona gives a score and its top two objections. Each objection quotes the line that triggered it, or names what's missing.
2. **Compound.** Compound = Σ(weight × score) ÷ 100.
3. **Revise.** Address the highest-weighted objections using twin facts only. If a fix needs a fact the twin doesn't hold, turn it into a question for the user instead of inventing the fact.
4. **Rebuild and re-score.**
   - Re-run the S5 truth gates.
   - Rebuild with `build_resume.py` as the next version.
   - Score again.

**Guard against inflation.** Personas judge the page, not your intent. A revision that adds keywords without evidence shouldn't raise the recruiter score, and a vaguer bullet shouldn't raise any score.

## Report

```
| Version | HM | Sponsor | Peer | Recruiter | Compound | What changed |
|---|---|---|---|---|---|---|
| v1 | 68 | 62 | 74 | 70 | 68 | First build |
| v2 | 76 | 70 | 75 | 79 | 75 | Led with margin result; added deal-desk scope |
```

Then give:
- the final file paths
- any open objections that need the user's input

Run `workspace.py track` to set the role's step to `CV ready`.
