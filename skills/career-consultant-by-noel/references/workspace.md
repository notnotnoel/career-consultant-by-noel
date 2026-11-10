# Workspace reference

Read this in S0, or when you need the folder layout, the script commands or environment fallbacks.

## Folder layout

```
<career folder>/
├── 00_Career Twin.md            verified career facts: the only source for CVs and messages
├── 01_Application Tracker.md    one row per role: step, dates, follow-up, status
├── 02_Claude Context Window.md  handoff note: current state, preferences, learned rules, standing rules
└── 99_All Files/
    ├── 00_Career Sources/       original resumes, LinkedIn export, screenshots, notes, format standard
    ├── 01_<Company>_<Role>/
    │   ├── 00_JD/
    │   ├── 01_Custom Resume/
    │   └── 99_Claude scripts/
    └── 02_<Company>_<Role>/ ...
```

## Scripts

Paths are relative to this skill's folder, not to the workspace.

| Command | Purpose |
|---|---|
| `python scripts/workspace.py init "<folder>"` | Create the root files and `99_All Files/00_Career Sources/`. Never overwrites existing files. |
| `python scripts/workspace.py add "<folder>" --company C --role R` | Add a tracker row only, for example a shortlisted role |
| `python scripts/workspace.py new-job "<folder>" --company C --role R` | Create the role folder and add or update its row |
| `python scripts/workspace.py track "<folder>" --company C --role R --step S` | Update step, dates, follow-up or status |
| `python scripts/workspace.py show "<folder>"` | Print the tracker, pinned first, overdue flagged |
| `python scripts/workspace.py check "<folder>"` | Report anything missing |
| `python scripts/build_resume.py <content.json> --out <dir> --name <stem> --preview` | Build a resume when no master template exists |

If Python can't reach the folder, create the same structure with your file tools.

## Environments
- **Claude desktop app, with a Project and a connected folder:** the intended setup.
- **Claude Code:** use the working directory, or a folder the user names.
- **No file access:** keep the three root files as Project documents, deliver other files as downloads, and say what couldn't be saved.
- **Connectors vary:** check which tools exist before promising a scan; name what's missing.
