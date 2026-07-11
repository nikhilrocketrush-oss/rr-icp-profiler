"""
Turns a problem statement into 2-3 outreach DM variants (text + voice-note
script). Same note as generate_problem_statement.py: Claude Code can do
this conversationally during the testing phase; this script is here for
when the workflow gets automated later.

Requires ANTHROPIC_API_KEY as an environment variable if run standalone.
"""
import os
import sys
from pathlib import Path

import anthropic

REPO_ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = REPO_ROOT / "lessons"


def load_lessons() -> str:
    if not LESSONS_DIR.exists():
        return ""
    files = sorted(LESSONS_DIR.glob("*.md"))
    return "\n\n".join(f.read_text() for f in files if f.name != "README.md")


def generate_dm_templates(problem_statement: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

    lessons = load_lessons()

    prompt = f"""Turn this problem statement into outreach DM drafts.

Problem statement:
{problem_statement}

Lessons from prior editor feedback (apply these first):
{lessons}

Write 2-3 variants: at least one written as a text DM, and one written as
a voice-note script. Keep the assumption-framed tone from the problem
statement — never accusatory, always inviting a yes/no response."""

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=800,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_dm_templates.py <problem_statement_text_file>")
        sys.exit(1)

    problem_statement = Path(sys.argv[1]).read_text()
    print(generate_dm_templates(problem_statement))
