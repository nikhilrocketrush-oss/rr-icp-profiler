"""
Orchestrates one full run: scrape profile(s), decide whether to also scrape
posts (using the same recency rule from CLAUDE.md step 5), optionally
generate a problem statement + DM drafts, and write one result file per
profile into results/.

Meant to be called from .github/workflows/run-profiler.yml, but also
runnable locally:

    python scripts/run_batch.py --urls "https://linkedin.com/in/a" --scrape-posts auto
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from scrape_profile import scrape_profiles
from scrape_posts import scrape_posts as scrape_posts_for_profile

REPO_ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = REPO_ROOT / "results"
RECENCY_THRESHOLD_DAYS = 75  # roughly 2.5 months, per the skip guideline

# TODO: confirm which field the profile-scraper actor actually returns for
# the most recent post date once the actor schema is verified against real
# output — this list is a starting guess covering likely field names.
LAST_POST_DATE_FIELDS = ["lastPostDate", "latestPostDate", "last_post_date", "mostRecentPostDate"]


def find_last_post_date(profile_data: dict):
    for field in LAST_POST_DATE_FIELDS:
        if field in profile_data and profile_data[field]:
            return profile_data[field]
    return None


def days_since(date_str: str):
    for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S.%fZ"):
        try:
            dt = datetime.strptime(date_str, fmt).replace(tzinfo=timezone.utc)
            return (datetime.now(timezone.utc) - dt).days
        except ValueError:
            continue
    return None


def should_scrape_posts(choice: str, last_post_date):
    """Returns (do_scrape: bool, reason: str). This replaces the live
    ask-before-scraping question from an interactive session — since a
    workflow run isn't a conversation, 'auto' applies the same rule and
    logs why, so you can always see and override the decision."""
    if choice == "yes":
        return True, "Manually requested"
    if choice == "no":
        return False, "Manually skipped"
    if not last_post_date:
        return True, "Last post date unavailable, defaulting to scrape"
    age = days_since(str(last_post_date))
    if age is None:
        return True, "Could not parse last post date, defaulting to scrape"
    if age >= RECENCY_THRESHOLD_DAYS:
        return False, f"Last post was {age} days ago (>= {RECENCY_THRESHOLD_DAYS}), auto-skipping to save credits"
    return True, f"Last post was {age} days ago, recent enough to scrape"


def slugify(url: str) -> str:
    return url.rstrip("/").split("/")[-1] or "profile"


def run(urls: list[str], scrape_posts_choice: str):
    RESULTS_DIR.mkdir(exist_ok=True)
    profiles = scrape_profiles(urls)

    for url, profile_data in zip(urls, profiles):
        last_post_date = find_last_post_date(profile_data)
        do_scrape, reason = should_scrape_posts(scrape_posts_choice, last_post_date)

        post_data = scrape_posts_for_profile(url) if do_scrape else []

        problem_statement = None
        dm_drafts = None
        if os.environ.get("ANTHROPIC_API_KEY"):
            from generate_problem_statement import generate_problem_statement
            from generate_dm_templates import generate_dm_templates

            problem_statement = generate_problem_statement(profile_data, post_data or None)
            dm_drafts = generate_dm_templates(problem_statement)
        else:
            print("ANTHROPIC_API_KEY not set — skipping problem statement and DM generation")

        slug = slugify(url)
        result = {
            "url": url,
            "scraped_at": datetime.now(timezone.utc).isoformat(),
            "profile_data": profile_data,
            "last_post_date": last_post_date,
            "posts_scraped": do_scrape,
            "post_scrape_reason": reason,
            "post_data": post_data,
            "problem_statement": problem_statement,
            "dm_drafts": dm_drafts,
        }
        (RESULTS_DIR / f"{slug}.json").write_text(json.dumps(result, indent=2))

        if problem_statement:
            md = f"# {url}\n\n## Post scrape decision\n\n{reason}\n\n## Problem statement\n\n{problem_statement}\n\n## DM drafts\n\n{dm_drafts}\n"
            (RESULTS_DIR / f"{slug}.md").write_text(md)

        print(f"Wrote results/{slug}.json — posts_scraped={do_scrape} ({reason})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--urls", nargs="+", required=True)
    parser.add_argument("--scrape-posts", choices=["auto", "yes", "no"], default="auto")
    args = parser.parse_args()
    run(args.urls, args.scrape_posts)
