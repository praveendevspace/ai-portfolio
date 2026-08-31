# Setting Up Your GitHub Projects Board

This turns your AI Career Transition Roadmap into a trackable GitHub Projects board — issues for each week, milestones for each phase, and labels to filter by type of work.

## Option A: Automated (recommended)

1. Install [GitHub CLI](https://cli.github.com) and run `gh auth login`.
2. Create your portfolio repo if you haven't: `gh repo create ai-portfolio --public --clone`
3. Put `roadmap_issues.csv` and `create_github_issues.py` in the same folder.
4. Run:
   ```
   python3 create_github_issues.py yourusername/ai-portfolio
   ```
   This creates one milestone per phase and one issue per week, pre-labeled (`phase-1`, `build`, `mlops`, `de-refresher`, `portfolio`, `job-search`, etc.).
5. Go to your repo → **Projects** tab → **New Project** → choose **Board** (Kanban) or **Roadmap** (timeline) view.
6. Click **Add items** → **Add from repository** → select all the issues you just created.
7. If using Board view, set up columns: `To Do`, `In Progress`, `Blocked`, `Done`.
8. If using Roadmap view, it will auto-lay-out issues by milestone (phase) — great for seeing the 9-month timeline at a glance.

## Option B: Manual (no CLI needed)

1. Open `roadmap_issues.csv` in Excel/Google Sheets/Numbers to see the full task list.
2. In your GitHub repo, go to **Issues** → **Milestones** → create one milestone per phase (Phase 0 through Phase 5).
3. Manually create an issue for each week, copy-pasting the Title and Body from the CSV, assigning it to the matching milestone, and adding the labels listed.
4. Create labels first under **Issues → Labels**: `phase-0` through `phase-5`, `learn`, `build`, `portfolio`, `mlops`, `de-refresher`, `job-search`, `buffer`.
5. Set up your Project board as in Option A, steps 5–7.

## Using the board day to day

- Move an issue to **In Progress** when you start that week; **Done** when you finish both the Learn and Build parts.
- Use the `de-refresher` label to filter and quickly see every week where your Data Engineering background gives you a shortcut.
- Use the `portfolio` label to see every milestone that produces something to show employers.
- When you start applying (around Week 32+), the `job-search` labeled issues become your application/networking checklist.

## Optional: pair with a learning journal

Since GitHub Projects only tracks tasks, consider pairing it with a lightweight markdown journal (Obsidian or Logseq) for weekly reflections — what you learned, what was confusing, what to revisit. Link each journal entry back to the relevant GitHub issue number for easy cross-reference.
