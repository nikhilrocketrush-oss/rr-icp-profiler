"""
Scores a merged profile dataset against rubric/gap-rubric.md and drafts an
assumption-framed problem statement.

Note: during the interactive testing phase (see CLAUDE.md), Claude Code can
do this step directly in conversation instead of calling this script — this
file is here for when the workflow gets automated later.

Requires ANTHROPIC_API_KEY as an environment variable if run standalone.
"""
import os
from dotenv import load_dotenv

load_dotenv()
import sys
import json
from pathlib import Path

import anthropic

REPO_ROOT = Path(__file__).resolve().parent.parent
RUBRIC_PATH = REPO_ROOT / "rubric" / "gap-rubric.md"
EXEMPLARS_PATH = REPO_ROOT / "rubric" / "exemplars.md"
LESSONS_DIR = REPO_ROOT / "lessons"


def load_lessons() -> str:
    """Concatenate every lessons file so recent corrections are in context."""
    if not LESSONS_DIR.exists():
        return ""
    files = sorted(LESSONS_DIR.glob("*.md"))
    return "\n\n".join(f.read_text() for f in files if f.name != "README.md")


def generate_problem_statement(profile_data: dict, post_data: list[dict] | None) -> str:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    rubric = RUBRIC_PATH.read_text()
    exemplars = EXEMPLARS_PATH.read_text()
    lessons = load_lessons()

    prompt = f"""You are a marketer scoring a LinkedIn profile for outreach fit.

Rubric:
{rubric}

Exemplars and standing corrections:
{exemplars}

Lessons from prior editor feedback (apply these first):
{lessons}

Profile data:
{json.dumps(profile_data, indent=2)}

Post data (may be empty if posts weren't scraped):
{json.dumps(post_data or [], indent=2)}

Score the profile against the rubric, then write one assumption-framed
problem statement following the framing rule in the rubric. Output the
scores and the problem statement, nothing else."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_problem_statement.py <profile_json_path> [post_json_path]")
        sys.exit(1)

    profile_data = json.loads(Path(sys.argv[1]).read_text())
    post_data = json.loads(Path(sys.argv[2]).read_text()) if len(sys.argv) > 2 else None

    print(generate_problem_statement(profile_data, post_data))
