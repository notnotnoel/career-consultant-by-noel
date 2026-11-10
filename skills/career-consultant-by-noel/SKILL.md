---
name: career-consultant-by-noel
description: Runs a job seeker's whole search in stages. It sets up a career twin from resumes and notes, scans Indeed and LinkedIn and scores roles, tailors resumes to a job description and stress-tests them with simulated hiring managers, drafts recruiter replies, keeps an application tracker, and preps interviews and offers. Use whenever someone is job hunting or mentions a job description, resume or CV, cover letter, recruiter message, application status, interview or offer, or wants to update their career history, even without naming this skill. Not for employers hiring or screening candidates.
license: MIT
metadata:
  author: notnotnoel
  version: 1.1.0
---

# Career consultant by Noel

This skill runs a job search as a set of **states**. On each turn, work out which state the user is in, tell them, and load only that state's guide from `references/`. Running one state at a time keeps a months-long search coherent. The user always knows which part of the system is working, and a quick tracker update never turns into an unrequested CV rebuild.

## The workspace

Everything lives in one folder the user owns:

```
<career folder>/
├── 00_Career Twin.md            verified career facts: the only source for CVs and messages
├── 01_Application Tracker.md    one row per role: step, dates, follow-up, status
├── 02_Claude Context Window.md  handoff note: current state, preferences, learned rules
└── 99_All Files/
    ├── 00_Career Sources/       original resumes, LinkedIn export, screenshots, notes
    ├── 01_<Company>_<Role>/
    │   ├── 00_JD/
    │   ├── 01_Custom Resume/
    │   └── 99_Claude scripts/
    └── 02_<Company>_<Role>/ ...
```

The context file exists because each new chat starts blank. Reading it first means the user never has to re-explain where their search stands.

`scripts/workspace.py` creates and maintains this structure deterministically:

| Command | Purpose |
|---|---|
| `init` | Create the root files and `99_All Files/00_Career Sources/` |
| `add` | Add a tracker row only, for example a shortlisted role |
| `new-job` | Create a role's folder and add or update its tracker row |
| `track` | Update a row's step, dates, follow-up or status |
| `show` | Print the tracker, pinned first, with overdue follow-ups flagged |
| `check` | Report anything missing |

Run `python scripts/workspace.py --help` for the arguments. If Python can't reach the folder, create the same structure with your file tools. The folder layout is what matters, not the tool that makes it.

Paths under `scripts/`, `templates/` and `references/` are relative to this skill's own folder, not to the user's workspace.

## Start of every turn

1. **Find the workspace.** Look for `02_Claude Context Window.md` in every place you can reach:
   - connected folders
   - the working directory
   - Project documents

   If you find it, read it.
2. **If you can't find it, ask before assuming the user is new.** A new chat may simply not have the folder connected yet. Re-running setup on someone mid-search is confusing and risks overwriting their files.
3. **Route, announce, load, run.** Use the table and tie-breaks below.

## Routing

| State | Use when | Guide |
|---|---|---|
| S0 · Setup | No workspace yet (confirmed with the user), or they ask to set up | `references/s0-setup.md` |
| S1 · Career twin | They share facts or documents about their own career, or correct one | `references/s1-career-twin.md` |
| S2 · Prospect | They ask to find or scan for jobs, or accept the scan offer | `references/s2-prospect.md` |
| S3 · Calibrate and shortlist | There are scan results to score, keep/remove feedback, or a change to job preferences | `references/s3-score-shortlist.md` |
| S4 · Research and fit | They share a JD or job link, or pick a tracked role to apply for | `references/s4-research-fit.md` |
| S5 · Tailored resume | They want a CV for a role whose fit is settled | `references/s5-resume-build.md` |
| S6 · Hiring-manager loop | Straight after S5, or "score my CV" for a role | `references/s6-hm-scoring-loop.md` |
| S7 · Outreach | Recruiter replies, cover emails, LinkedIn notes, follow-ups, thank-you notes | `references/s7-outreach.md` |
| S8 · Interview prep | They ask for interview prep or a mock interview | `references/s8-interview-prep.md` |
| S9 · Tracker | Status news, including "they booked an interview" (offer S8 as the next step); "show my tracker"; "what's next" | `references/s9-tracker.md` |
| S10 · Offer | An offer arrives, or they want to compare or negotiate one | `references/s10-offer.md` |

**Tie-breaks:**

- **Several asks in one message** → handle each one, in a sensible order, and announce each state as you enter it:
  - S1 comes before S4 or S5, so the CV uses the new facts.
  - S9 updates come last.
- **JD shared** → go straight to S4 and say you're skipping S2–S3. A scan is pointless when the user already has the role in hand.
- **Career facts shared** → S1, which updates the twin only.
  - If a fact comes up in the middle of another state ("actually that was US$12M"), fix the twin, mention it in one line, and stay where you are.
- **"Recalibrate" or "change my job search preferences"** → S3 calibration only. Don't run a scan.
- **"Continue" or "where were we"** → pick up the state and next action recorded in the context file.
- **Not set up (confirmed), but the user arrives with a concrete task** such as a JD or a recruiter message → fast-track:
  1. Create the workspace.
  2. Get at least one resume into the twin.
  3. Do the task.

  Tailoring without career facts would mean inventing them.
- **Genuinely ambiguous** → ask one short question. A wrong guess can cost the user a full CV rebuild.

## Announce the state

Open with one line, so the user can see what is running and redirect you if it's wrong:

> **State: S4 · Research and fit.** You shared the Contoso JD, so I'm skipping the job scan.

Announce again each time you move to a new state within a turn.

## After every state

- **Update the context file:**
  - the state you just ran
  - what happened
  - the next action
  - any new learned rule
  - any open item

  Keep the file under about 150 lines by rolling older history into a short summary. It's read at the start of every chat, so bloat slows down every future turn.
- **Update the tracker** with `workspace.py track` whenever an application changed.
- **End with one suggested next step**, and name the state it would trigger.

## Principles for every state

- **Evidence before prose.** Resume lines, messages and fit verdicts come only from the twin. When something important is missing, ask. An invented metric that falls apart in an interview costs the user far more than a modest true one.
- **Tag sources** in the twin:
  - `[VERIFIED: <file>]`: backed by a document in Career Sources
  - `[SELF]`: the user's own account
  - `[GAP]`: needed but unknown

  Tags tell the user which claims will hold up under questioning.
- **One priority criterion per role**, for example *pricing analytics > stakeholder influence > SQL*. It decides which experience gets full bullets and which gets compressed. A CV that tries to show everything says nothing.
- **Resume format lock.** If `99_All Files/00_Career Sources/` holds a `Resume Format Standard.md` or a master resume the user has approved, every resume must match it exactly. Copy the master `.docx` and replace the text only. Before delivery, compare page 1 with the master. Use `scripts/build_resume.py` only when no master exists. A CV that looks different from the user's approved version gets rejected, so this rule takes priority over the S5 defaults.
- **Rebuild, don't hand-edit.** Keep resume content in a content file in `99_Claude scripts/`, so any version can be regenerated after a correction.
- **Corrections flow back.** Every correction goes into the twin with a "don't regress" note, so the next application starts from the fixed version.
- **The user acts; Claude prepares.** Never submit an application, send a message, or accept or decline anything for the user. Draft it, and let them press send.
- **Respect people and platforms.**
  - Research hiring managers through public professional information only.
  - Browse job boards in the user's own session at a normal pace, and don't bulk-scrape.
- **Privacy.** Never write government ID numbers, bank details or passwords into any file.
- **One chat per application.** When the user starts applying for a role, suggest a new chat in the Project named `<Company> · <Role> · <step>`, renamed as the step changes. Each conversation then stays focused and short.

## Environments

- **Claude desktop app, with a Project and a connected folder:** the intended setup. Every feature works.
- **Claude Code:** use the working directory, or a folder the user names, as the workspace.
- **No file access** (web or mobile only): keep the three root files as Project documents, deliver everything else as downloads, and say plainly what couldn't be saved.
- **Connectors vary.** Check which tools exist before promising a scan, and name what's missing and how to add it.
