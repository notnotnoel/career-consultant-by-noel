---
name: career-consultant-by-noel
description: Runs a job seeker's whole search in stages. It sets up a career twin from resumes and notes, scans Indeed and LinkedIn and scores roles, tailors resumes to a job description and stress-tests them with simulated hiring managers, drafts recruiter replies, keeps an application tracker, and preps interviews and offers. Use whenever someone is job hunting or mentions a job description, resume or CV, cover letter, recruiter message, application status, interview or offer, or wants to update their career history, even without naming this skill. Not for employers hiring or screening candidates.
license: MIT
metadata:
  author: notnotnoel
  version: 1.2.0
---

# Career consultant: state selector

This file only picks the state. Read **one** state guide from `references/` and follow it. Don't read the other guides; loading them costs tokens and adds nothing.

## 1. Load context
Find `02_Claude Context Window.md` in a connected folder, the working directory or the Project documents. Read it: it holds the current state, search preferences, learned rules and standing rules, and standing rules always apply. If you can't find it, ask whether the user has set up before. A new chat may only be missing the folder connection.

## 2. Pick the state (first match wins)

| Condition | State | Read |
|---|---|---|
| Several requests in one message | Run each state in order: S1 first, S9 last | (each guide in turn) |
| "Change my job search preferences" / "recalibrate" | S3a · Calibrate (no scan) | `references/s3a-calibrate.md` |
| A JD or job link is shared (skip S2–S3) | S4 · Research and fit | `references/s4-research-fit.md` |
| Facts or documents about the user's own career, or a correction | S1 · Career twin (twin only) | `references/s1-career-twin.md` |
| "Continue" / "where were we" | The state named in the context file | that state's guide |
| No workspace (confirmed), or the user asks to set up | S0 · Setup | `references/s0-setup.md` |
| Find or scan for jobs | S2 · Prospect | `references/s2-prospect.md` |
| Scan results to score, or keep/remove feedback | S3b · Score and shortlist | `references/s3b-score-shortlist.md` |
| A CV for a role whose fit is settled | S5 · Tailored resume, then S6 | `references/s5-resume-build.md` |
| "Score my CV", or straight after S5 | S6 · Hiring-manager loop | `references/s6-hm-scoring-loop.md` |
| Recruiter reply, cover email, LinkedIn note, follow-up, thank-you | S7 · Outreach | `references/s7-outreach.md` |
| Interview prep or a mock interview is asked for | S8 · Interview prep | `references/s8-interview-prep.md` |
| Status news ("applied", "rejected", "interview booked"), "show my tracker", "what's next" | S9 · Tracker | `references/s9-tracker.md` |
| An offer to evaluate or negotiate | S10 · Offer | `references/s10-offer.md` |

- **Not set up, but the user brings a task** (a JD, a recruiter message): read `s0-setup.md` for the fast track. Create the workspace, get one resume into the twin, then do the task.
- **Unclear:** ask one short question.
- **Folder layout, scripts, environments:** read `references/workspace.md` only when needed.

## 3. Announce
Open with one line: **State: S4 · Research and fit.** + the reason (for example "You shared the Contoso JD, so I'm skipping the scan."). Announce again each time the state changes.

## 4. Rules for every state
- Use only facts in `00_Career Twin.md`. If something is missing, ask; never invent a number.
- A career fact found during another state goes into the twin; mention it in one line and stay in your state.
- Never send, submit, accept or decline anything for the user. Draft only.
- Research people from public professional information only. Browse job boards in the user's session at a normal pace.
- Never write ID numbers, bank details or passwords into files.
- Resumes: if `99_All Files/00_Career Sources/` has a format standard or an approved master resume, copy the master and replace text only (S5 Step 0).

## 5. After the state
- Update the context file: state, what happened, next action, new rules. Keep it under ~150 lines.
- If an application changed, update the tracker (`python scripts/workspace.py track …`).
- End with one next step and the state it starts. When the user starts an application, suggest a new chat named `<Company> · <Role> · <step>`.
