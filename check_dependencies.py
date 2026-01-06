"""
Dependency Check Script
Run this BEFORE executing the notebook to verify all required packages are available.
"""

import sys

print("="*60)
print("DEPENDENCY CHECK FOR ESO PIPELINE")
print("="*60)
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

required_packages = {
    "pandas": "pandas",
    "requests": "requests",
    "beautifulsoup4": "bs4",
    "lxml": "lxml",
    "tqdm": "tqdm"
}

missing_packages = []
installed_packages = []

print("\nChecking required packages:")
for package_name, import_name in required_packages.items():
    try:
        __import__(import_name)
        installed_packages.append(package_name)
        print(f"  ✓ {package_name}")
    except ImportError:
        missing_packages.append(package_name)
        print(f"  ❌ {package_name} - MISSING")

if missing_packages:
    print(f"\n❌ Missing packages: {', '.join(missing_packages)}")
    print("\nTo install missing packages, run:")
    print(f"  pip install {' '.join(missing_packages)}")
    print("\nOr if using conda:")
    print(f"  conda install -c conda-forge {' '.join(missing_packages)}")
    sys.exit(1)
else:
    print(f"\n✓ All required packages are installed")
    print(f"  Installed: {', '.join(installed_packages)}")
    sys.exit(0)

