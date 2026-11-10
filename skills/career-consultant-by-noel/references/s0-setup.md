# S0 · Setup

Goal: a working folder, a user who understands how the system behaves, and a first career twin. Don't rush through setup. Every later state is only as good as the twin built here.

Track progress with this checklist. A step marked ⏸ ends your turn, so wait for the user before going on.

```
- [ ] 0.1 Project and folder ⏸
- [ ] 0.2 Scaffold + overview (same reply) ⏸
- [ ] 0.3 Context drop ⏸ → run S1
- [ ] 0.4 Offer a first scan ⏸ → S2
```

## 0.1 Project and folder ⏸

Tell the user, in three short steps:

1. **Create a Project in Claude** (for example "Career HQ"), and keep every career chat inside it. The files and the history then stay together.
2. **Make a folder on your computer for all career documents** (for example `Documents/Career HQ`), and connect it to this chat from the Claude desktop app.
3. **Reply with the folder's name** once it's connected.

If the conversation already has a folder or working directory that's clearly meant for this, confirm it instead of asking for a new one.

If folder tools never appear (for example the user is on web or mobile only), offer the fallback:
- keep the three root files as Project documents, and
- deliver everything else as downloads.

## 0.2 Scaffold and overview (same reply)

Do both in one reply, so the user is reading while the files are being made.

**A. Scaffold.** Run:

```bash
python scripts/workspace.py init "<folder>"
```

Use your file tools instead if Python can't reach the folder. Then confirm what was created in two lines.

The script never overwrites existing files, so it's safe to run again.

**B. Overview** (no more than 15 lines). Cover:

- **How it works.** The search runs in states, and every reply opens by naming the active one.
- **The states**, one line each, S0–S10.
- **Shortcuts:**
  - Share a JD and the scan is skipped.
  - Share a career update and only the twin changes.
  - Say "recalibrate" and only the job preferences change.
  - Say "continue" and it picks up from the context file.
- **The three files:**
  - The twin holds the facts.
  - The tracker holds the applications.
  - The context file is the handoff note between chats.
- **Habits:**
  - Use one chat per application, renamed with its status.
  - Start a new chat in the Project any time to add career information.

Close with: **"Ready to set up your career twin?"** ⏸

## 0.3 Context drop ⏸

Ask for everything the user has. More material makes a truer twin, and screenshots of real slides or reviews are the strongest evidence:

- Resumes, any version and any age.
- LinkedIn profile: the URL, or the PDF export (Profile → More → Save to PDF).
- Photos or screenshots: project slides, performance reviews, awards, dashboards.
- Notes for each role: scope, team size, budget, the numbers, and what *they* personally drove.
- Compensation baseline: base, bonus, allowances. This is optional, and only used to score salary uplift.

Save the originals into `99_All Files/00_Career Sources/`, so that `[VERIFIED]` tags can point at real files. Then run **S1** on everything.

Remind them: *"You can start a new chat in this Project any time and send more. I'll add it to your career twin."*

## 0.4 Hand-off ⏸

1. List the top `[GAP]`s worth filling, at most five, each with why it matters (for example "no team size on the Contoso role, which most manager JDs ask about").
2. Then ask: **"Would you like me to run a first job scan?"**
   - Yes → S2.
   - No → note it in the context file and stop.

## Fast track (user arrives with a task)

When there's no workspace but the user brings a concrete task, such as a JD or a recruiter message:

1. Do 0.1 and 0.2A only: get the folder, then run `init`.
2. Ask for at least one resume, then run S1 on it.
3. Skip the overview and go straight to the task's state, for example `references/s4-research-fit.md`.

Tailoring without career facts would mean inventing them.

## Standing rules
Use only facts in `00_Career Twin.md` — ask rather than invent a number. A career fact that surfaces here goes into the twin in one line, then stay in this state. Never send, submit, accept or decline anything for the user — draft only. Research people and companies from public professional sources only. Never write ID numbers, bank details or passwords into any file. Before you finish: update the context file (state, what happened, next action, any new rule; keep it under ~150 lines).
