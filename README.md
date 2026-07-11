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

## Structure

- `scripts/` — scraper and generation script skeletons
- `rubric/` — the gap-scoring rubric and the growing exemplars file
- `lessons/` — one file per round of editor feedback, read before every
  new generation
