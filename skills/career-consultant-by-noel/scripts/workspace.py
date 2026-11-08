#!/usr/bin/env python3
"""Create and maintain a career-consultant-by-noel workspace.

Commands (run any of them with --help for details):
  init     ROOT                          create the root files and 99_All Files/00_Career Sources
  add      ROOT --company C --role R     add a tracker row only (for example a shortlisted role)
  new-job  ROOT --company C --role R     create 99_All Files/NN_<Company>_<Role>/ and add or update its row
  track    ROOT --company C --role R     update a row: --step, --applied, --followup, --due, --status, --link
  show     ROOT [--all]                  print the tracker: pinned first, then open by due date
  check    ROOT                          report anything missing from the workspace

Standard library only, Python 3.8+. Existing files are never overwritten.
"""
import argparse
import datetime as dt
import re
import shutil
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL_DIR / "templates"

TWIN = "00_Career Twin.md"
TRACKER = "01_Application Tracker.md"
CONTEXT = "02_Claude Context Window.md"
ROOT_FILES = [TWIN, TRACKER, CONTEXT]
ALL_FILES = "99_All Files"
SOURCES = "00_Career Sources"
JOB_SUBDIRS = ["00_JD", "01_Custom Resume", "99_Claude scripts"]

COLUMNS = ["Job title", "Company", "Step", "Date applied", "Follow-up action",
           "Follow-up due", "Status", "Link", "Folder"]
STEPS = ["Shortlisted", "Researching", "CV ready", "Applied", "Screening",
         "Interviewing", "Offer", "Closed"]
STATUSES = ["Open", "Pinned", "Closed"]
FOLLOW_UP_BUSINESS_DAYS = 5   # default nudge after applying


class WorkspaceError(Exception):
    pass


# ---------- helpers ----------

def today():
    return dt.date.today()


def parse_date(value):
    if value in (None, ""):
        return None
    if value.lower() == "today":
        return today()
    try:
        return dt.date.fromisoformat(value)
    except ValueError:
        raise WorkspaceError(f"Dates must look like 2026-11-08 or 'today', got {value!r}")


def add_business_days(start, days):
    current = start
    while days > 0:
        current += dt.timedelta(days=1)
        if current.weekday() < 5:
            days -= 1
    return current


def canonical(value, allowed, label):
    for option in allowed:
        if option.lower() == value.strip().lower():
            return option
    raise WorkspaceError(f"{label} must be one of: {', '.join(allowed)} (got {value!r})")


def clean_name(text, limit=40):
    text = re.sub(r'[\\/:*?"<>|]+', " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text[:limit].rstrip() or "Untitled"


def norm(text):
    return re.sub(r"\s+", " ", text or "").strip().lower()


def require_root(root):
    if not root.is_dir():
        raise WorkspaceError(f"Folder not found: {root}. Run 'init' first or check the path.")


# ---------- tracker file ----------

def split_row(line):
    cells = re.split(r"(?<!\\)\|", line.strip())
    if cells and cells[0] == "":
        cells = cells[1:]
    if cells and cells[-1] == "":
        cells = cells[:-1]
    return [c.strip().replace("\\|", "|") for c in cells]


def join_row(cells):
    return "| " + " | ".join(c.replace("|", "\\|") for c in cells) + " |"


def read_tracker(root):
    path = root / TRACKER
    if not path.exists():
        raise WorkspaceError(f"{TRACKER} not found in {root}. Run 'init' first.")
    lines = path.read_text(encoding="utf-8").splitlines()
    header_at = next((i for i, l in enumerate(lines) if l.strip().startswith("|")
                      and split_row(l)[:1] == ["Job title"]), None)
    if header_at is None:
        raise WorkspaceError(f"{TRACKER} has no table starting with '| Job title |'.")
    header = split_row(lines[header_at])
    if header != COLUMNS:
        raise WorkspaceError(f"{TRACKER} columns changed. Expected: {' | '.join(COLUMNS)}")
    rows, end = [], header_at + 2
    while end < len(lines) and lines[end].strip().startswith("|"):
        cells = split_row(lines[end])
        cells = (cells + [""] * len(COLUMNS))[:len(COLUMNS)]
        rows.append(dict(zip(COLUMNS, cells)))
        end += 1
    return path, lines[:header_at], rows, lines[end:]


def write_tracker(path, before, rows, after):
    out = list(before)
    out.append(join_row(COLUMNS))
    out.append("|" + "---|" * len(COLUMNS))
    out.extend(join_row([r[c] for c in COLUMNS]) for r in rows)
    out.extend(after)
    path.write_text("\n".join(out).rstrip("\n") + "\n", encoding="utf-8")


def find_row(rows, company, role, required=True):
    c, r = norm(company), norm(role)
    exact = [row for row in rows if norm(row["Company"]) == c and norm(row["Job title"]) == r]
    if exact:
        return exact[0]
    loose = [row for row in rows if norm(row["Company"]) == c
             and (r in norm(row["Job title"]) or norm(row["Job title"]) in r)]
    if len(loose) == 1:
        return loose[0]
    if not required:
        return None
    options = [f"{row['Job title']} · {row['Company']}" for row in rows if norm(row["Company"]) == c]
    hint = f" Rows at {company}: {'; '.join(options)}" if options else ""
    raise WorkspaceError(f"No tracker row for {role!r} at {company!r}.{hint}")


def new_row(company, role, step, link, folder=""):
    return {"Job title": role.strip(), "Company": company.strip(), "Step": step,
            "Date applied": "", "Follow-up action": "", "Follow-up due": "",
            "Status": "Open", "Link": link or "", "Folder": folder}


def apply_updates(row, args):
    if getattr(args, "step", None):
        row["Step"] = canonical(args.step, STEPS, "Step")
    if getattr(args, "applied", None):
        row["Date applied"] = parse_date(args.applied).isoformat()
    if getattr(args, "followup", None) is not None:
        row["Follow-up action"] = args.followup.strip()
    if getattr(args, "due", None):
        row["Follow-up due"] = parse_date(args.due).isoformat()
    if getattr(args, "status", None):
        row["Status"] = canonical(args.status, STATUSES, "Status")
    if getattr(args, "link", None):
        row["Link"] = args.link.strip()

    # Sensible defaults so callers don't have to remember them.
    if row["Step"] == "Applied":
        if not row["Date applied"]:
            row["Date applied"] = today().isoformat()
        if not row["Follow-up due"]:
            row["Follow-up due"] = add_business_days(
                parse_date(row["Date applied"]), FOLLOW_UP_BUSINESS_DAYS).isoformat()
        if not row["Follow-up action"]:
            row["Follow-up action"] = "Follow up with the recruiter"
    if row["Step"] == "Closed":
        row["Status"] = "Closed"
        if getattr(args, "due", None) is None:
            row["Follow-up due"] = ""
    return row


def describe(row):
    bits = [f"{row['Job title']} · {row['Company']}", f"step {row['Step']}", f"status {row['Status']}"]
    if row["Follow-up due"]:
        bits.append(f"follow-up {row['Follow-up due']}: {row['Follow-up action'] or '-'}")
    return " | ".join(bits)


# ---------- commands ----------

def cmd_init(args):
    root = Path(args.root).expanduser()
    root.mkdir(parents=True, exist_ok=True)
    created, kept = [], []
    for name in ROOT_FILES:
        target = root / name
        if target.exists():
            kept.append(name)
        else:
            shutil.copyfile(TEMPLATES / name, target)
            created.append(name)
    sources = root / ALL_FILES / SOURCES
    existed = sources.exists()
    sources.mkdir(parents=True, exist_ok=True)
    (created if not existed else kept).append(f"{ALL_FILES}/{SOURCES}/")
    print(f"Workspace: {root.resolve()}")
    if created:
        print("Created: " + ", ".join(created))
    if kept:
        print("Already there (left unchanged): " + ", ".join(kept))


def cmd_add(args):
    root = Path(args.root).expanduser()
    require_root(root)
    path, before, rows, after = read_tracker(root)
    row = find_row(rows, args.company, args.role, required=False)
    if row:
        apply_updates(row, args)
        action = "Updated"
    else:
        row = new_row(args.company, args.role, canonical(args.step or "Shortlisted", STEPS, "Step"), args.link)
        apply_updates(row, args)
        rows.append(row)
        action = "Added"
    write_tracker(path, before, rows, after)
    print(f"{action}: {describe(row)}")


def next_job_number(all_files):
    numbers = [int(m.group(1)) for p in all_files.iterdir() if p.is_dir()
               for m in [re.match(r"^(\d{2})_", p.name)] if m]
    return max([n for n in numbers if n > 0], default=0) + 1


def cmd_new_job(args):
    root = Path(args.root).expanduser()
    require_root(root)
    all_files = root / ALL_FILES
    all_files.mkdir(exist_ok=True)
    suffix = f"_{clean_name(args.company)}_{clean_name(args.role)}"
    existing = [p for p in all_files.iterdir() if p.is_dir() and p.name.lower().endswith(suffix.lower())
                and re.match(r"^\d{2}_", p.name)]
    if existing:
        folder, made = existing[0], False
    else:
        folder, made = all_files / f"{next_job_number(all_files):02d}{suffix}", True
    for sub in JOB_SUBDIRS:
        (folder / sub).mkdir(parents=True, exist_ok=True)
    rel = f"{ALL_FILES}/{folder.name}"

    path, before, rows, after = read_tracker(root)
    row = find_row(rows, args.company, args.role, required=False)
    if row is None:
        row = new_row(args.company, args.role, "Researching", args.link, rel)
        rows.append(row)
    row["Folder"] = rel
    apply_updates(row, args)
    write_tracker(path, before, rows, after)
    print(f"{'Created' if made else 'Reused'} folder: {folder.resolve()}")
    print(f"Tracker: {describe(row)}")


def cmd_track(args):
    root = Path(args.root).expanduser()
    require_root(root)
    path, before, rows, after = read_tracker(root)
    row = find_row(rows, args.company, args.role)
    apply_updates(row, args)
    write_tracker(path, before, rows, after)
    print(f"Updated: {describe(row)}")


def cmd_show(args):
    root = Path(args.root).expanduser()
    require_root(root)
    _, _, rows, _ = read_tracker(root)
    if not rows:
        print("The tracker is empty.")
        return
    now = today()

    def due(row):
        d = parse_date(row["Follow-up due"]) if row["Follow-up due"] else None
        return d or dt.date.max

    active = [r for r in rows if r["Status"] != "Closed"]
    closed = [r for r in rows if r["Status"] == "Closed"]
    active.sort(key=lambda r: (r["Status"] != "Pinned", due(r)))
    overdue = [r for r in active if due(r) < now]
    if overdue:
        print(f"Overdue follow-ups ({len(overdue)}): " +
              "; ".join(f"{r['Company']} ({r['Follow-up due']}: {r['Follow-up action'] or 'follow up'})" for r in overdue))
        print()
    shown = active + (closed if args.all else [])
    cols = ["Job title", "Company", "Step", "Date applied", "Follow-up action", "Follow-up due", "Status"]
    print(join_row(cols))
    print("|" + "---|" * len(cols))
    for r in shown:
        status = r["Status"] + (" (overdue)" if r in overdue else "")
        print(join_row([r["Job title"], r["Company"], r["Step"], r["Date applied"],
                        r["Follow-up action"], r["Follow-up due"], status]))
    if closed and not args.all:
        print(f"\n{len(closed)} closed application(s) hidden. Use --all to include them.")


def cmd_check(args):
    root = Path(args.root).expanduser()
    issues = []
    if not root.is_dir():
        print(f"Folder not found: {root}")
        sys.exit(1)
    for name in ROOT_FILES:
        if not (root / name).exists():
            issues.append(f"missing {name}")
    try:
        read_tracker(root)
    except WorkspaceError as exc:
        if (root / TRACKER).exists():
            issues.append(str(exc))
    all_files = root / ALL_FILES
    if not (all_files / SOURCES).is_dir():
        issues.append(f"missing {ALL_FILES}/{SOURCES}/")
    if all_files.is_dir():
        for job in sorted(p for p in all_files.iterdir() if p.is_dir() and re.match(r"^\d{2}_", p.name)):
            if job.name.startswith("00_"):
                continue
            for sub in JOB_SUBDIRS:
                if not (job / sub).is_dir():
                    issues.append(f"{ALL_FILES}/{job.name} is missing {sub}/")
    context = root / CONTEXT
    if context.exists() and "## Search preferences" not in context.read_text(encoding="utf-8"):
        issues.append(f"{CONTEXT} has no '## Search preferences' section")
    if issues:
        print("Workspace issues:\n- " + "\n- ".join(issues))
        sys.exit(1)
    print("Workspace looks complete.")


# ---------- CLI ----------

def build_parser():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def with_root(p):
        p.add_argument("root", help="the career folder")
        return p

    def with_row_fields(p, need_ids=True):
        p.add_argument("--company", required=need_ids)
        p.add_argument("--role", required=need_ids, help="job title")
        p.add_argument("--step", help=" / ".join(STEPS))
        p.add_argument("--applied", help="date applied: YYYY-MM-DD or 'today'")
        p.add_argument("--followup", help="next action, for example 'Nudge the recruiter'")
        p.add_argument("--due", help="follow-up due date: YYYY-MM-DD or 'today'")
        p.add_argument("--status", help=" / ".join(STATUSES))
        p.add_argument("--link", help="posting URL")
        return p

    with_root(sub.add_parser("init", help="create the workspace")).set_defaults(func=cmd_init)
    with_row_fields(with_root(sub.add_parser("add", help="add a tracker row"))).set_defaults(func=cmd_add)
    with_row_fields(with_root(sub.add_parser("new-job", help="create a role folder"))).set_defaults(func=cmd_new_job)
    with_row_fields(with_root(sub.add_parser("track", help="update a tracker row"))).set_defaults(func=cmd_track)
    show = with_root(sub.add_parser("show", help="print the tracker"))
    show.add_argument("--all", action="store_true", help="include closed applications")
    show.set_defaults(func=cmd_show)
    with_root(sub.add_parser("check", help="check the workspace")).set_defaults(func=cmd_check)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except WorkspaceError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
