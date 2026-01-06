"""
QA Validation Script for ESO_new_project.ipynb
Run this AFTER executing the notebook to verify outputs meet requirements.
"""

import pandas as pd
import os
from collections import Counter

print("="*60)
print("QA VALIDATION FOR ESO PIPELINE")
print("="*60)

# 1. Check master output file exists
MASTER_FILE = "Organization_Database_MASTER_v1_0.csv"
if not os.path.exists(MASTER_FILE):
    print(f"\n❌ ERROR: Master output file not found: {MASTER_FILE}")
    print("   The notebook may not have completed successfully.")
    exit(1)
else:
    print(f"\n✓ Master output file found: {MASTER_FILE}")

# 2. Load and validate master file
try:
    df_master = pd.read_csv(MASTER_FILE)
    print(f"✓ Master file loaded: {df_master.shape[0]} rows × {df_master.shape[1]} columns")
except Exception as e:
    print(f"\n❌ ERROR: Cannot read master file: {e}")
    exit(1)

# 3. Check required columns exist
REQUIRED_COLS = ["Org Name", "Organization Type", "Long Name / Description", 
                 "Website URL", "Resources", "Industry ", "Track Record", 
                 "Charlottesville?", "Virginia?"]

missing_cols = [col for col in REQUIRED_COLS if col not in df_master.columns]
if missing_cols:
    print(f"\n❌ ERROR: Missing required columns: {missing_cols}")
else:
    print(f"\n✓ All required columns present")

# 4. Check for blank values in required columns
print("\n" + "-"*60)
print("CHECKING FOR BLANK VALUES IN REQUIRED COLUMNS")
print("-"*60)

blank_issues = []
for col in REQUIRED_COLS:
    if col in df_master.columns:
        blank_count = df_master[col].isna().sum() + (df_master[col].astype(str).str.strip() == "").sum()
        if blank_count > 0:
            blank_issues.append((col, blank_count))
            print(f"  ❌ {col}: {blank_count} blank values found")
        else:
            # Check for acceptable placeholders
            placeholder_values = ["Unknown", "Not publicly stated", "Needs manual review"]
            has_placeholders = df_master[col].astype(str).str.strip().isin(placeholder_values).any()
            if has_placeholders:
                placeholder_count = df_master[col].astype(str).str.strip().isin(placeholder_values).sum()
                print(f"  ✓ {col}: No blanks (uses placeholders: {placeholder_count} rows)")
            else:
                print(f"  ✓ {col}: No blanks")

if blank_issues:
    print(f"\n❌ ERROR: Found {len(blank_issues)} columns with blank values")
    print("   All required fields must have values (placeholders are acceptable)")
else:
    print(f"\n✓ No blank values in required columns")

# 5. Check People (Extracted) column
print("\n" + "-"*60)
print("CHECKING PEOPLE (EXTRACTED) COLUMN")
print("-"*60)

if "People (Extracted)" not in df_master.columns:
    print("  ❌ ERROR: 'People (Extracted)' column not found")
else:
    orgs_with_people = (df_master["People (Extracted)"] != "").sum()
    orgs_without_people = len(df_master) - orgs_with_people
    pct_with_people = 100 * orgs_with_people / len(df_master) if len(df_master) > 0 else 0
    
    print(f"  ✓ Column exists")
    print(f"  ✓ Organizations with people: {orgs_with_people} ({pct_with_people:.1f}%)")
    print(f"  ✓ Organizations without people: {orgs_without_people} ({100-pct_with_people:.1f}%)")
    
    # Check format (sample)
    sample_orgs = df_master[df_master["People (Extracted)"] != ""].head(3)
    if len(sample_orgs) > 0:
        print(f"\n  Sample formatted people entries:")
        for idx, row in sample_orgs.iterrows():
            org_name = str(row.get("Org Name", ""))[:40]
            people_str = str(row.get("People (Extracted)", ""))[:100]
            print(f"    {org_name}: {people_str}...")

# 6. Check for duplicate people within same org
print("\n" + "-"*60)
print("CHECKING FOR DUPLICATE PEOPLE WITHIN ORGS")
print("-"*60)

duplicate_issues = []
for idx, row in df_master.iterrows():
    org_name = str(row.get("Org Name", ""))
    people_str = str(row.get("People (Extracted)", ""))
    
    if people_str and "(" in people_str:
        # Extract person names (simple check)
        people_parts = people_str.split("),")
        person_names = []
        for part in people_parts:
            if "(" in part:
                name = part.split("(")[0].strip()
                if name:
                    person_names.append(name.lower())
        
        # Check for duplicates
        if len(person_names) != len(set(person_names)):
            duplicate_issues.append(org_name)

if duplicate_issues:
    print(f"  ⚠ WARNING: Found {len(duplicate_issues)} orgs with potential duplicate people")
    print(f"    Sample: {duplicate_issues[:3]}")
else:
    print(f"  ✓ No duplicate people detected within orgs")

# 7. Validate org capabilities
print("\n" + "-"*60)
print("VALIDATING ORG CAPABILITIES")
print("-"*60)

if "org_capabilities" in df_master.columns:
    all_caps = []
    for caps_str in df_master["org_capabilities"]:
        if caps_str and str(caps_str).strip():
            all_caps.extend([c.strip() for c in str(caps_str).split(";")])
    
    allowed_caps = {"Regulatory / FDA", "Clinical & Translational Support", 
                    "IP / Legal / Licensing", "Manufacturing / GMP / Scale-Up"}
    found_caps = set(all_caps)
    forbidden_caps = found_caps - allowed_caps
    
    # Check for forbidden keywords
    forbidden_keywords = ["funding", "fund", "grant", "sbir", "sttr", "investor", 
                         "fundraising", "customer discovery", "prototyping", "product development"]
    found_forbidden = []
    for cap in all_caps:
        cap_lower = cap.lower()
        for keyword in forbidden_keywords:
            if keyword in cap_lower:
                found_forbidden.append(cap)
                break
    
    if forbidden_caps:
        print(f"  ❌ ERROR: Found forbidden capabilities: {forbidden_caps}")
    elif found_forbidden:
        print(f"  ❌ ERROR: Found forbidden keywords in capabilities: {set(found_forbidden)}")
    else:
        print(f"  ✓ All capabilities are in allowed set")
        if all_caps:
            cap_counts = Counter(all_caps)
            print(f"  ✓ Capability distribution:")
            for cap, count in cap_counts.most_common():
                print(f"      {cap}: {count}")
else:
    print("  ⚠ 'org_capabilities' column not found (may be expected if no capabilities identified)")

# 8. Placeholder usage report
print("\n" + "-"*60)
print("PLACEHOLDER USAGE REPORT")
print("-"*60)

placeholder_counts = {}
for col in REQUIRED_COLS:
    if col in df_master.columns:
        if col == "Track Record":
            placeholder_counts[col] = (df_master[col] == "Not publicly stated").sum()
        elif col == "Organization Type":
            placeholder_counts[col] = (df_master[col] == "Needs manual review").sum()
        else:
            placeholder_counts[col] = (df_master[col] == "Unknown").sum()

for col, count in placeholder_counts.items():
    if count > 0:
        pct = 100 * count / len(df_master)
        print(f"  {col:30s}: {count:4d} ({pct:5.1f}%)")

# 9. Final summary
print("\n" + "="*60)
print("QA SUMMARY")
print("="*60)
print(f"Total organizations: {len(df_master)}")
print(f"Required columns checked: {len(REQUIRED_COLS)}")
print(f"Columns with blanks: {len(blank_issues)}")
print(f"Organizations with people: {orgs_with_people if 'People (Extracted)' in df_master.columns else 'N/A'}")
print(f"Org capabilities validated: {'✓' if 'org_capabilities' in df_master.columns and not forbidden_caps else 'N/A'}")

if blank_issues or (forbidden_caps if 'org_capabilities' in df_master.columns else False):
    print("\n❌ VALIDATION FAILED - See errors above")
    exit(1)
else:
    print("\n✓ VALIDATION PASSED - All checks successful")
    exit(0)

