# S9 · Tracker

Goal: the user can see every application and the next action on each, without reading their inbox.

## Columns

Keep these columns, in this order. `workspace.py` depends on them:

`Job title | Company | Step | Date applied | Follow-up action | Follow-up due | Status | Link | Folder`

**Step** is one of:
- Shortlisted
- Researching
- CV ready
- Applied
- Screening
- Interviewing
- Offer
- Closed

**Status** is one of:
- **Open**
- **Pinned:** sorts to the top.
- **Closed**

## Commands

```bash
python scripts/workspace.py show  "<folder>"            # pinned first, then open by due date; overdue flagged
python scripts/workspace.py track "<folder>" --company "Contoso" --role "Pricing Analyst" --step Applied
python scripts/workspace.py track "<folder>" --company "Northwind" --role "Ops Lead" --step Closed --followup "Rejected after screen"
python scripts/workspace.py add   "<folder>" --company "Fabrikam" --role "Supply Lead" --link "<url>"
```

`track` fills in sensible defaults, so you don't need to:
- Moving to **Applied** stamps today's date, and sets a follow-up 5 business days out.
- Moving to **Closed** closes the row.

## Behaviour

- **Status update** ("applied to X", "rejected by Y"): update the row and confirm in one line.
- **Interview booked:** set the step to `Interviewing`, with the interview date as the follow-up due date. Then offer S8 prep as the next step, but don't start it unasked.
- **Offer received:** set the step to `Offer`, then offer S10.
- **"Show my tracker"** or **"what's next"**: run `show`. Overdue follow-ups appear at the top, and closed rows are folded into a count.
- **Right after a new shortlist (from S3):** show the tracker, then ask **"Which job should I help you apply for?"** Recommend:
  - *"Start a new chat in this Project for each application. That keeps each conversation focused as the application moves forward."*
  - *"Rename each chat with its status, for example `Contoso · Pricing Analyst · Applied`, and update the name as it moves."*
