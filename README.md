# RocketRush ICP gap profiler

Standalone, interactive tool: paste LinkedIn profile URLs, get a
gap-scored, assumption-framed problem statement and DM drafts, in a
back-and-forth testing loop with an editor. No database — everything
lives in this repo as files.

See `CLAUDE.md` for the exact step-by-step behavior this project follows
when run through Claude Code.

## Setup

1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in `APIFY_TOKEN` (a separate
   Apify account from rr-tracker's) and, if needed, `ANTHROPIC_API_KEY`.
3. Open this repo in Claude Code and start a session — it will follow the
   workflow in `CLAUDE.md` automatically.

## Running without Claude Code

Go to the **Actions** tab of this repo → **ICP profile run** → **Run
workflow**. Paste profile URLs (one per line) and pick a `scrape_posts`
option:

- `auto` — applies the same recency rule from `CLAUDE.md` step 5: skips
  post scraping if the last post is 75+ days old, scrapes (max 7 posts)
  otherwise. The decision and its reason get logged in the result.
- `yes` / `no` — override the rule manually for this run.

This is the non-interactive equivalent of the live "ask before scraping
posts" question — since a workflow run isn't a conversation, `auto` makes
the same call and writes down why, so you can always see and override it
on the next run.

Results land in `results/<profile-slug>.json` (and a matching `.md` with
the problem statement and DM drafts, if `ANTHROPIC_API_KEY` is set as a
repo secret) — committed straight back into the repo.

Needs `APIFY_TOKEN` set as a repo secret. `ANTHROPIC_API_KEY` is optional —
without it, scraping still runs, but the problem-statement and DM steps
are skipped.

## Structure

- `scripts/` — scraper and generation script skeletons
- `rubric/` — the gap-scoring rubric and the growing exemplars file
- `lessons/` — one file per round of editor feedback, read before every
  new generation
