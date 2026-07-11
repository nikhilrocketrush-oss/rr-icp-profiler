# Lessons

One file per edit round, named `YYYY-MM-DD-<profile-slug>.md`. Each file
should capture:

- which profile this was for
- what Claude generated
- what the editor changed and why

Claude reads every file in this folder before generating a new problem
statement (see `CLAUDE.md` step 11). If a correction pattern repeats 3+
times, it gets promoted into `rubric/exemplars.md` or `rubric/gap-rubric.md`
instead of relying on this folder alone.
