"""
Scrapes a limited set of recent posts (5-7) per profile using the
harvestapi/linkedin-profile-posts Apify actor.

Note: harvestapi/linkedin-post-search (used elsewhere, e.g. rr-tracker) is
a keyword search actor — it requires a search query and isn't meant for
"give me this one profile's own recent posts". Its own docs point to
linkedin-profile-posts for exactly this use case, so that's what this
script uses instead.

Requires APIFY_TOKEN as an environment variable.

Usage:
    python scrape_posts.py "https://linkedin.com/in/person-a"
"""
import os
from dotenv import load_dotenv

load_dotenv()
import sys
import json
from apify_client import ApifyClient

ACTOR_ID = "harvestapi/linkedin-profile-posts"
MAX_POSTS_PER_PROFILE = 7


def scrape_posts(profile_url: str, max_posts: int = MAX_POSTS_PER_PROFILE) -> list[dict]:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        raise RuntimeError("APIFY_TOKEN environment variable is not set")

    client = ApifyClient(token)

    # Verified against the actor's live docs (apify.com/harvestapi/
    # linkedin-profile-posts): targetUrls + maxPosts is the correct input.
    run_input = {
        "targetUrls": [profile_url],
        "maxPosts": max_posts,
    }

    run = client.actor(ACTOR_ID).call(run_input=run_input)

    results = []
    for item in client.dataset(run.default_dataset_id).iterate_items():
        results.append(item)
        if len(results) >= max_posts:
            break
    return results


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scrape_posts.py <profile_url>")
        sys.exit(1)

    data = scrape_posts(sys.argv[1])
    print(json.dumps(data, indent=2))
