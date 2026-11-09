# Changelog

## 1.1.0 · 2026-11-09

- **Resume format lock.** When the user has an approved master resume or a `Resume Format Standard.md` in Career Sources, every CV is built by copying that master and replacing the text only. Page 1 is compared with the master before delivery. The generic builder is used only when no master exists.
- **New template:** `templates/Resume Format Standard.template.md`, for recording a user's approved format.

## 1.0.0 · 2026-11-08

First public release.

- **Eleven states (S0–S10)** with automatic routing and a visible state announcement on every reply. The states cover setup, career twin, prospecting, calibration and shortlisting, research and fit, tailored resume, hiring-manager scoring loop, outreach, interview prep, tracker, and offer.
- **Shortcuts:**
  - A shared JD skips the scan.
  - A career update only updates the twin.
  - "Change my job search preferences" only recalibrates.
  - "Continue" resumes from the context file.
- **Workspace contract:**
  - three root files: career twin, application tracker, context window
  - `99_All Files/` holding career sources and one folder per role
- **`scripts/workspace.py`:** cross-platform workspace and tracker management (`init`, `add`, `new-job`, `track`, `show`, `check`).
- **`scripts/build_resume.py`:** builds a resume DOCX and PDF from a JSON content file, shrinks the text to fit the page limit, flags font substitution, and renders previews.
- **Scoring:** an explicit fit formula, honest handling of missing salary and rating data, and learned shortlisting rules with an evidence threshold.
- **Tests:** 11 test cases in `evals/`, runnable with `claude plugin eval`, plus a trigger test set in `dev/`.
- **Packaging:** a Claude Code plugin manifest and marketplace, so the skill installs from GitHub.
