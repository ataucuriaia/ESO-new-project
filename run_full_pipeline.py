"""
Master Execution Script for ESO Pipeline
This script executes the notebook and runs QA validation, then provides a final status report.
"""

import subprocess
import sys
import os
import time
from pathlib import Path

print("="*60)
print("ESO PIPELINE - FULL EXECUTION")
print("="*60)
print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

# Track status
status = {
    "notebook_execution": "UNKNOWN",
    "master_csv_created": False,
    "qa_validation": "UNKNOWN",
    "blocking_issues": []
}

# Step 1: Check dependencies
print("Step 1: Checking dependencies...")
try:
    result = subprocess.run([sys.executable, "check_dependencies.py"], 
                          capture_output=True, text=True, timeout=30)
    if result.returncode != 0:
        print("❌ Dependency check failed:")
        print(result.stdout)
        print(result.stderr)
        status["blocking_issues"].append("Missing required packages - run: pip install pandas requests beautifulsoup4 lxml tqdm")
        print("\n" + "="*60)
        print("=== PIPELINE STATUS ===")
        print("Notebook execution: FAILED (dependencies missing)")
        print("Master CSV created: NO")
        print("QA validation: NOT RUN")
        print(f"Blocking issues: {', '.join(status['blocking_issues'])}")
        print("=======================")
        sys.exit(1)
    else:
        print("✓ All dependencies available")
except Exception as e:
    print(f"❌ Error checking dependencies: {e}")
    status["blocking_issues"].append(f"Dependency check error: {e}")
    sys.exit(1)

# Step 2: Verify input file exists
print("\nStep 2: Verifying input file...")
input_file = "Organization Database 1f24e34e337d8027b500d2a10b1ceaa7.csv"
if not os.path.exists(input_file):
    print(f"❌ Input file not found: {input_file}")
    status["blocking_issues"].append(f"Input file missing: {input_file}")
    print("\n" + "="*60)
    print("=== PIPELINE STATUS ===")
    print("Notebook execution: FAILED (input file missing)")
    print("Master CSV created: NO")
    print("QA validation: NOT RUN")
    print(f"Blocking issues: {', '.join(status['blocking_issues'])}")
    print("=======================")
    sys.exit(1)
else:
    print(f"✓ Input file found: {input_file}")

# Step 3: Execute notebook
print("\nStep 3: Executing notebook...")
print("This may take 15-20 minutes depending on number of organizations...")
notebook_file = "ESO_new_project.ipynb"

if not os.path.exists(notebook_file):
    print(f"❌ Notebook file not found: {notebook_file}")
    status["blocking_issues"].append(f"Notebook file missing: {notebook_file}")
    status["notebook_execution"] = "FAILED"
else:
    try:
        # Execute notebook using nbconvert
        print("Running notebook (this will take several minutes)...")
        result = subprocess.run(
            ["jupyter", "nbconvert", "--to", "notebook", "--execute", 
             "--inplace", notebook_file],
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        
        if result.returncode == 0:
            print("✓ Notebook execution completed")
            status["notebook_execution"] = "SUCCESS"
        else:
            print("❌ Notebook execution failed:")
            print(result.stdout)
            print(result.stderr)
            status["notebook_execution"] = "FAILED"
            status["blocking_issues"].append("Notebook execution error - check output above")
    except subprocess.TimeoutExpired:
        print("❌ Notebook execution timed out (>1 hour)")
        status["notebook_execution"] = "FAILED"
        status["blocking_issues"].append("Notebook execution timeout")
    except FileNotFoundError:
        print("❌ jupyter command not found. Please install jupyter:")
        print("  conda install jupyter")
        print("  or")
        print("  pip install jupyter")
        status["notebook_execution"] = "FAILED"
        status["blocking_issues"].append("Jupyter not installed")
    except Exception as e:
        print(f"❌ Error executing notebook: {e}")
        status["notebook_execution"] = "FAILED"
        status["blocking_issues"].append(f"Notebook execution error: {e}")

# Step 4: Check if master CSV was created
print("\nStep 4: Verifying master CSV creation...")
master_csv = "Organization_Database_MASTER_v1_0.csv"
if os.path.exists(master_csv):
    print(f"✓ Master CSV file created: {master_csv}")
    status["master_csv_created"] = True
    
    # Get file size
    file_size = os.path.getsize(master_csv)
    print(f"  File size: {file_size:,} bytes")
else:
    print(f"❌ Master CSV file not found: {master_csv}")
    status["master_csv_created"] = False
    if status["notebook_execution"] == "SUCCESS":
        status["blocking_issues"].append("Master CSV not created despite successful notebook execution")

# Step 5: Run QA validation
print("\nStep 5: Running QA validation...")
if status["master_csv_created"]:
    try:
        result = subprocess.run(
            [sys.executable, "qa_validation.py"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✓ QA validation passed")
            status["qa_validation"] = "PASSED"
        else:
            print("❌ QA validation failed")
            status["qa_validation"] = "FAILED"
            status["blocking_issues"].append("QA validation found issues - see output above")
    except Exception as e:
        print(f"❌ Error running QA validation: {e}")
        status["qa_validation"] = "FAILED"
        status["blocking_issues"].append(f"QA validation error: {e}")
else:
    print("⚠ Skipping QA validation (master CSV not created)")
    status["qa_validation"] = "NOT RUN"

# Final status report
print("\n" + "="*60)
print("=== PIPELINE STATUS ===")

# Notebook execution status
if status["notebook_execution"] == "SUCCESS":
    print("Notebook execution: SUCCESS")
elif status["notebook_execution"] == "FAILED":
    print("Notebook execution: FAILED")
else:
    print("Notebook execution: UNKNOWN")

# Master CSV status
if status["master_csv_created"]:
    print("Master CSV created: YES")
else:
    print("Master CSV created: NO")

# QA validation status
if status["qa_validation"] == "PASSED":
    print("QA validation: PASSED")
elif status["qa_validation"] == "FAILED":
    print("QA validation: FAILED")
elif status["qa_validation"] == "NOT RUN":
    print("QA validation: NOT RUN")
else:
    print("QA validation: UNKNOWN")

# Blocking issues
if status["blocking_issues"]:
    print(f"Blocking issues: {', '.join(status['blocking_issues'])}")
else:
    print("Blocking issues: NONE")

print("=======================")
print(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S')}")

# Exit code
if (status["notebook_execution"] == "SUCCESS" and 
    status["master_csv_created"] and 
    status["qa_validation"] == "PASSED" and 
    len(status["blocking_issues"]) == 0):
    print("\n✓ PIPELINE COMPLETED SUCCESSFULLY")
    sys.exit(0)
else:
    print("\n❌ PIPELINE COMPLETED WITH ISSUES")
    sys.exit(1)

