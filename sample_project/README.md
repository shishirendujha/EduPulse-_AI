# Sample Project (Codex Walkthrough)

This folder is intentionally separate from the rest of the repository so you can experiment without mixing changes. It contains a tiny Python script that reads a CSV file and prints a summary.

## Quick start

```bash
cd sample_project
python src/main.py
```

Expected output:

```
Sample Project Summary
Count: 5.0
Total: 39.0
Average: 7.80
```

## Step-by-step: how to work with Codex

1. **Understand the goal**
   - Write a clear, single-sentence request.
   - Example: “Create a script that summarizes numbers from a CSV file.”

2. **Locate relevant files**
   - List directories or open key files.
   - Example commands:
     - `ls`
     - `rg "summary" -n`

3. **Plan the change**
   - Decide the smallest set of files to edit.
   - Outline the steps (e.g., add a helper, add a script, update docs).

4. **Implement the change**
   - Make focused edits.
   - Keep new code small and readable.

5. **Run a quick check**
   - For this sample:
     - `python src/main.py`

6. **Review the results**
   - Make sure output matches expectations.
   - Re-run as needed.

7. **Commit your changes**
   - Use a descriptive commit message.
   - Example:
     - `git add sample_project`
     - `git commit -m "Add sample project walkthrough"`

## What’s inside

- `src/main.py`: entry point that loads data and prints a summary.
- `src/utils.py`: helper functions for parsing and summarizing.
- `data/numbers.csv`: tiny sample dataset.
