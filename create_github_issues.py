#!/usr/bin/env python3
"""
Bulk-create GitHub issues (and milestones) from roadmap_issues.csv using GitHub CLI.

PREREQUISITES:
  1. Install GitHub CLI: https://cli.github.com
  2. Authenticate: gh auth login
  3. Create your repo (if not already done): gh repo create ai-portfolio --public
  4. Place this script and roadmap_issues.csv in the same folder
  5. pip install nothing extra - uses only the standard library + the gh CLI

USAGE:
  python3 create_github_issues.py <owner>/<repo>

Example:
  python3 create_github_issues.py yourusername/ai-portfolio
"""

import csv
import subprocess
import sys
from pathlib import Path

CSV_FILE = Path(__file__).parent / "roadmap_issues.csv"


def run(cmd, check=True):
    print(f"  $ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0 and check:
        print(f"    (non-fatal) {result.stderr.strip()}")
    return result


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 create_github_issues.py <owner>/<repo>")
        sys.exit(1)

    repo = sys.argv[1]

    if subprocess.run(["which", "gh"], capture_output=True).returncode != 0:
        print("GitHub CLI (gh) not found. Install from https://cli.github.com and run 'gh auth login' first.")
        sys.exit(1)

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    phases = sorted(set(row["Phase"] for row in rows))

    print(f"Creating {len(phases)} milestones in {repo} ...")
    for phase in phases:
        run(["gh", "api", f"repos/{repo}/milestones", "-f", f"title={phase}"], check=False)

    print(f"\nCreating {len(rows)} issues in {repo} ...")
    for row in rows:
        title = f"{row['Week']}: {row['Title']}"
        labels = [l.strip() for l in row["Labels"].split(",") if l.strip()]
        cmd = [
            "gh", "issue", "create",
            "--repo", repo,
            "--title", title,
            "--body", row["Body"],
            "--milestone", row["Phase"],
        ]
        for label in labels:
            cmd += ["--label", label]
        run(cmd, check=False)

    print("\nDone. Go to your repo -> Projects tab -> New Project -> Board or Roadmap view, and add these issues.")


if __name__ == "__main__":
    main()
