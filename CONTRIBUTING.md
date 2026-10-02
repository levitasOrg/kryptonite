# Contributing

## Add an attack module

1. Copy `modules/_TEMPLATE.md` to `modules/<your-dimension>.md`.
2. Fill in the frontmatter: `name` (matches the file name), `description` (one sentence), `applies-to` (stack signals).
3. Fill in every body section in the template, then delete its comment block.
4. Open a pull request. CI checks that the frontmatter is complete.

A good module finds a class of real-world failure no existing module covers, and every probe has a clear pass / fail signal.

## Change a phase or reference

The phase skills and `references/` are contracts that other files depend on. If you change the finding schema or severity rubric, update `scripts/validate_findings.py` and its tests in the same pull request.

## Run the tests

```bash
python3 -m pip install pytest
python3 -m pytest -q scripts/tests
```

## Pull requests

- One change per pull request.
- Say what you tested and on what kind of app.
