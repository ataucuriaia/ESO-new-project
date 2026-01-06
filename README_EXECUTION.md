# ESO Pipeline - Quick Start

## One-Command Execution

To run the entire pipeline and get a final status report, simply execute:

```bash
conda activate eso_env
python run_full_pipeline.py
```

This single command will:
1. ✅ Check all dependencies
2. ✅ Execute the notebook end-to-end
3. ✅ Run QA validation
4. ✅ Provide final status report

## Expected Final Output

When complete, you'll see:

```
=== PIPELINE STATUS ===
Notebook execution: SUCCESS
Master CSV created: YES
QA validation: PASSED
Blocking issues: NONE
=======================
```

## What Gets Created

- **Primary Output:** `Organization_Database_MASTER_v1_0.csv`
- **QA Logs (if any):** `scrape_failures.csv`, `dedupe_log.csv`

## If Something Fails

The script will clearly indicate:
- What step failed
- What blocking issues exist
- What you need to do next

## Manual Steps (if needed)

If the automated script doesn't work, see `EXECUTION_GUIDE.md` for manual steps.

