"""
Scrapes LinkedIn profile data (about, experience, headline, last post date)
for a list of URLs using the harvestapi/linkedin-profile-scraper Apify actor.

Requires APIFY_TOKEN as an environment variable.

Usage:
    python scrape_profile.py "https://linkedin.com/in/person-a" "https://linkedin.com/in/person-b"
"""
import os
from dotenv import load_dotenv

load_dotenv()
import sys
import json
from apify_client import ApifyClient

ACTOR_ID = "harvestapi/linkedin-profile-scraper"


def scrape_profiles(urls: list[str]) -> list[dict]:
    token = os.environ.get("APIFY_TOKEN")
    if not token:
        raise RuntimeError("APIFY_TOKEN environment variable is not set")

    client = ApifyClient(token)

    # TODO: confirm exact input schema for this actor against current Apify
    # docs before first real run — field names below are a starting guess.
    run_input = {"profileUrls": urls}

    run = client.actor(ACTOR_ID).call(run_input=run_input)

    results = []
    for item in client.dataset(run.default_dataset_id).iterate_items():
        results.append(item)
    return results


if __name__ == "__main__":
    urls = sys.argv[1:]
    if not urls:
        print("Paste at least one LinkedIn profile URL as an argument.")
        sys.exit(1)

    data = scrape_profiles(urls)
    print(json.dumps(data, indent=2))
