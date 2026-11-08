# Career Consultant by Noel

A job-search system for Claude. Set it up once, and Claude runs your search with you:

- builds a verified **career twin** from your resumes, LinkedIn and notes
- scans job boards and **scores roles against your own priorities**
- tailors your CV to each job description, then **stress-tests it the way a hiring manager would**
- drafts recruiter replies and follow-ups for you to send
- keeps your **application tracker** up to date
- preps you for interviews and offers

Every reply opens with the stage it's running, so you always know what Claude is doing, and you can redirect it.

> **State: S4 · Research and fit.** You shared the Contoso JD, so I'm skipping the job scan.

## How it works

| Stage | Runs when |
|---|---|
| S0 · Setup | First run: create a Project and a career folder |
| S1 · Career twin | You share career info. Only your twin is updated. |
| S2 · Prospect | You ask for a job scan (Indeed, LinkedIn, the web) |
| S3 · Calibrate and shortlist | Scoring scan results, learning from what you keep, changing your preferences |
| S4 · Research and fit | You share a JD, or pick a role to apply for |
| S5 · Tailored resume | You want a CV for a role |
| S6 · Hiring-manager loop | Straight after S5: simulated reader scoring until the score stops improving |
| S7 · Outreach | Recruiter replies, cover emails, LinkedIn notes, thank-yous |
| S8 · Interview prep | Recall pack and mock interviews |
| S9 · Tracker | "Applied", "rejected", "they booked an interview", "show my tracker" |
| S10 · Offer | Offer maths, benchmarks and negotiation drafts |

**Shortcuts:**

- **Share a JD:** the scan is skipped.
- **Share a career update:** only the twin changes.
- **Say "change my job search preferences":** only the scoring changes.
- **Say "continue where we left off":** Claude picks up from your context file.

## Install

### Claude app (recommended)

1. Download [`career-consultant-by-noel.zip`](https://github.com/notnotnoel/career-consultant-by-noel/raw/main/dist/career-consultant-by-noel.zip). It's also in the `dist/` folder.
2. Check that **Code execution and file creation** is turned on in **Settings > Capabilities**.
   - On Team and Enterprise plans, an owner controls this setting.
3. Go to **Customize > Skills**, click **+**, choose **Create skill > Upload a skill**, and upload the zip.
4. In the Claude desktop app, create a Project (for example "Career HQ"), then say **"Set up my career consultant."** Claude walks you through connecting a folder for your career documents.

### Claude Code

```
/plugin install career-consultant-by-noel --marketplace notnotnoel/career-consultant-by-noel
```

Or, in two steps:

```
/plugin marketplace add notnotnoel/career-consultant-by-noel
/plugin install career-consultant-by-noel@noel-career-tools
```

### Works best with

- **The Indeed connector**, for job scans.
- **A browser Claude can use**, for LinkedIn.
- **Gmail** (optional), to save outreach drafts.
- **Python 3.8+ with `python-docx`**, for building resumes.
  - **LibreOffice** (optional) adds PDF export and a page-count check.
  - Claude's own sandbox usually has all of these already.

## What it creates

```
Career HQ/
├── 00_Career Twin.md            your verified career facts
├── 01_Application Tracker.md    every role: step, dates, follow-up, status
├── 02_Claude Context Window.md  handoff note between chats
└── 99_All Files/
    ├── 00_Career Sources/       your original resumes, screenshots, notes
    └── 01_<Company>_<Role>/     00_JD · 01_Custom Resume · 99_Claude scripts
```

Tip: use one chat per application, and rename it as the application moves (`Contoso · Pricing Analyst · Applied`).

## Your data

The skill has no servers of its own. Your files stay in your folder and your Claude account. Claude searches the web and job boards only when you ask for a scan or for company research.

- **Claude never sends a message or submits an application for you.** It drafts; you send.
- **Every CV line comes from your career twin.** Gaps are flagged and asked about, never invented.
- **ID numbers, bank details and passwords are never written to your files.**

## Troubleshooting

| Problem | Fix |
|---|---|
| Upload fails | The zip must contain the `career-consultant-by-noel` folder at its root, with `SKILL.md` inside. Use the zip from `dist/` as is. |
| No Skills section | Turn on code execution in **Settings > Capabilities**. |
| "Indeed isn't connected" | Add the Indeed connector, then ask for the scan again. |
| PDF fonts look different | Claude's sandbox may not have your font. Export the final PDF from Word or Pages. |
| A new chat doesn't know my progress | Connect the same folder to the new chat, then say "continue where we left off". |

## For contributors

```
.claude-plugin/                     plugin + marketplace manifests (Claude Code)
skills/career-consultant-by-noel/   the skill: SKILL.md, references/, scripts/, templates/
  evals/                            11 test cases (claude plugin eval format)
dev/trigger-eval-set.json           queries for tuning the skill description
dist/career-consultant-by-noel.zip  upload-ready skill for the Claude app
```

- **Validate:** run `claude plugin validate .`
- **Run the tests:** from the repo root, run `claude plugin eval . --allow-tools Write,Edit,Bash --scaffold --runs 1`. This needs Claude Code v2.1.269 or later. The runs are billed: each case runs with and without the skill, and three times by default.
- **Rebuild `dist/career-consultant-by-noel.zip` after every change to the skill:** zip the `skills/career-consultant-by-noel` folder without `evals/`, so the zip's root is that folder.

See [CHANGELOG.md](CHANGELOG.md) for version history. MIT licensed. Created by Noel Paliath; not affiliated with Anthropic.
