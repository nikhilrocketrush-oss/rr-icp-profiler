# RocketRush ICP gap profiler — Claude Code project instructions

Standalone project. Not connected to rr-tracker or any Firebase/Firestore system.
All state lives in this repo as files.

## What this project does

Given a set of LinkedIn profile URLs, this project scrapes profile data (and
optionally recent posts), scores the profile against a gap rubric, and drafts
an assumption-framed problem statement plus outreach DM variants — following
the methodology described by the RocketRush sales consultant (see
`rubric/gap-rubric.md`).

## Conversation flow (follow this exactly, in order)

1. On session start, greet the user and ask them to paste the LinkedIn
   profile URLs they want processed.
2. Run `scripts/scrape_profile.py` against ONLY those URLs, using the
   `harvestapi/linkedin-profile-scraper` Apify actor. Do not touch the post
   scraper yet.
3. Once the scrape returns, extract and display in chat: name, headline,
   about section, experience/career history, and (if the actor returns it)
   the date of their most recent post.
4. Ask the user: continue with just this profile data, or also scrape posts?
5. Always show the last-post date as part of that question, along with a
   recommendation — e.g. "last post was ~3 months ago, I'd suggest skipping
   the post scrape to save credits." This is a suggestion only. The final
   call always belongs to the person handling the profile — never
   auto-skip.
6. If the user wants posts scraped, run `scripts/scrape_posts.py` using the
   `harvestapi/linkedin-post-search` actor, limited to 5-7 posts per
   profile. Do not pull a full post history — this mirrors how rr-tracker
   conserves Apify credits.
7. Run `scripts/generate_problem_statement.py`: score the merged dataset
   against `rubric/gap-rubric.md`, then generate an assumption-framed
   problem statement (never accusatory — "most people I work with who are
   facing X want Y, are you facing something similar?").
8. Run `scripts/generate_dm_templates.py`: turn the problem statement into
   2-3 DM variants (text + voice-note script).
9. Present the final problem statement and DM drafts in chat for review.
10. When the editor gives edits, write them to a new dated file in
    `lessons/` (format: `lessons/YYYY-MM-DD-<profile-slug>.md`) — capture
    what was wrong and what the corrected version looked like.
11. Before starting step 7 on any new profile, read every file currently in
    `lessons/` first and apply what's been learned. If the same kind of
    correction shows up 3+ times across lesson files, propose an update to
    `rubric/gap-rubric.md` or `rubric/exemplars.md` rather than relying on
    the lessons folder alone.

## Credentials (set as repo/environment secrets, never hardcoded)

- `APIFY_TOKEN` — a separate Apify account from the one rr-tracker uses
- `ANTHROPIC_API_KEY` — only needed if scripts call the Claude API directly
  outside of Claude Code itself; if Claude Code is doing the generation
  steps interactively, this may not be required

## Explicit non-goals

- No Firebase, Firestore, or any external database
- No connection to the rr-tracker repo or its data
- No scheduling/automation yet — this is an interactive, testing-phase tool
