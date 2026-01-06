# ESO Pipeline Execution Guide

## Prerequisites

1. **Activate your Conda environment:**
   ```bash
   conda activate eso_env
   ```

2. **Verify Python version:**
   ```bash
   python --version
   ```
   Should show Python 3.10.x

3. **Verify required packages:**
   ```bash
   python -c "import pandas, requests, bs4, tqdm, lxml; print('All packages available')"
   ```

## Step 1: Install Missing Packages (if needed)

If any package is missing, run this in a terminal (with eso_env activated):

```bash
pip install pandas requests beautifulsoup4 lxml tqdm
```

Or if you prefer conda:
```bash
conda install -c conda-forge pandas requests beautifulsoup4 lxml tqdm
```

## Step 2: Execute Full Pipeline (RECOMMENDED)

**Single command to run everything and get final status:**

```bash
python run_full_pipeline.py
```

This script will:
1. Check dependencies
2. Execute the notebook automatically
3. Run QA validation
4. Provide final status report in the exact format requested

**Expected output format:**
```
=== PIPELINE STATUS ===
Notebook execution: SUCCESS / FAILED
Master CSV created: YES / NO
QA validation: PASSED / FAILED
Blocking issues: NONE / <list issues>
=======================
```

## Alternative: Manual Execution

If you prefer to run steps manually:

### Step 2a: Execute the Notebook

**Option A: Using Jupyter Notebook**
1. Open Jupyter Notebook:
   ```bash
   jupyter notebook
   ```
2. Navigate to `ESO_new_project.ipynb`
3. Ensure kernel is set to `eso_env` (check top-right)
4. Run all cells: `Kernel` → `Restart & Run All`

**Option B: Using JupyterLab**
1. Open JupyterLab:
   ```bash
   jupyter lab
   ```
2. Open `ESO_new_project.ipynb`
3. Ensure kernel is `eso_env`
4. Run all cells: `Run` → `Run All Cells`

**Option C: Using nbconvert (command line)**
```bash
jupyter nbconvert --to notebook --execute --inplace ESO_new_project.ipynb
```

### Step 2b: Run QA Validation

After notebook execution completes, run the validation script:

```bash
python qa_validation.py
```

This will:
- Verify master CSV file exists
- Check for blank values in required columns
- Validate people extraction format
- Check for duplicate people
- Validate org capabilities
- Generate placeholder usage report

## Expected Outputs

After successful execution, you should have:

1. **Primary Output:**
   - `Organization_Database_MASTER_v1_0.csv` (single master file)

2. **Optional QA Logs:**
   - `scrape_failures.csv` (if any scraping failures occurred)
   - `dedupe_log.csv` (if any duplicates were skipped during expansion)

## Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution:** Install missing package:
```bash
pip install <package_name>
```

### Issue: "FileNotFoundError: Organization Database..."
**Solution:** Ensure the CSV file is in the same directory as the notebook

### Issue: Kernel not found
**Solution:** 
1. Install ipykernel in eso_env:
   ```bash
   conda install ipykernel
   python -m ipykernel install --user --name eso_env --display-name "Python (eso_env)"
   ```
2. Restart Jupyter and select the eso_env kernel

### Issue: Notebook hangs during scraping
**Solution:** 
- The notebook uses rate limiting (1 second between requests)
- For 492 organizations, expect ~8-10 minutes of scraping time
- If it hangs, check network connectivity or firewall settings

## Manual QA Checklist

If you prefer manual verification:

- [ ] Notebook completes without errors
- [ ] `Organization_Database_MASTER_v1_0.csv` exists
- [ ] File contains all original organizations
- [ ] No blank values in required columns (A, B, E, F, J, K, L, M, N)
- [ ] "People (Extracted)" column exists and contains formatted strings
- [ ] No duplicate people within same org
- [ ] Org capabilities limited to 4 approved types only
- [ ] No funding/SBIR/customer discovery categories

