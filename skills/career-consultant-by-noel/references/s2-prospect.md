# S2 · Prospect

Goal: a clean pool of live candidate roles, which S3 then scores. Skip this state entirely when the user shares a JD.

## 2.1 Check the tools

- **Indeed:** look for the Indeed connector's tools (`search_jobs`, `get_job_details`, `get_company_data`). If they're missing, ask the user to connect Indeed from the connectors menu and wait. It's the richest structured source for this state.
- **LinkedIn:** there's no connector, so use a browser in the user's own signed-in session. If no browser is available, say LinkedIn will be skipped this run.
- **Web search:** use it to supplement, for example company career pages and postings the boards missed.

Every role you show must come from a tool result or a page you actually opened in this session. If a source is unavailable, say so, and don't fill the gap from memory. Invented or stale listings waste the user's applications and their trust.

## 2.2 Calibrate first

If the context file has no confirmed **Search preferences**, run S3 step 3.1 before searching. An uncalibrated first scan is the fastest way to lose the user's trust in the whole system.

## 2.3 Plan the search

Build 6–12 queries from target titles × locations × seniority synonyms. Also add adjacent titles that the twin genuinely supports. For example, an operations analyst with strong pricing work should also search "Pricing Analyst". Leave out anything a hard filter excludes.

## 2.4 Collect

For each plausible result, record:
- title
- company
- location and work mode
- posted date
- apply URL
- salary band (only if posted)
- the JD text, from the job details
- company rating, plus the management sub-rating when available

Aim for 30–60 raw candidates.

## 2.5 Clean

Remove:
- **Duplicates.** The same role is often posted on several boards. Keep the employer's own posting when you can find it.
- **Postings that are closed or expired**, and any older than about 30 days unless they're clearly still open.
- **Anything that fails a hard filter.**

Then hand the pool to S3, step 3.2.
