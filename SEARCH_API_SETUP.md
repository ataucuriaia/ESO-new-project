# Auto-Discovery Setup Guide

The ESO pipeline now supports **automatic organization discovery** via web search APIs. This guide explains how to enable it.

## Quick Start

Auto-discovery is **automatically enabled** if you have API keys set in your environment variables. The notebook will detect which keys are available and use the appropriate provider.

## Option 1: Use Setup Scripts (Recommended)

### Windows
Run `setup_search_api.bat` and follow the prompts:
```cmd
setup_search_api.bat
```

### Linux/Mac
Run the setup script:
```bash
chmod +x setup_search_api.sh
source setup_search_api.sh
```

## Option 2: Manual Setup

### Windows (PowerShell)
```powershell
# For Google Custom Search
$env:GOOGLE_CSE_API_KEY = "your_api_key_here"
$env:GOOGLE_CSE_ENGINE_ID = "your_engine_id_here"
$env:SEARCH_PROVIDER = "google_cse"

# For SerpAPI
$env:SERPAPI_KEY = "your_api_key_here"
$env:SEARCH_PROVIDER = "serpapi"

# For Bing
$env:BING_SEARCH_KEY = "your_api_key_here"
$env:SEARCH_PROVIDER = "bing"
```

### Windows (Command Prompt)
```cmd
set GOOGLE_CSE_API_KEY=your_api_key_here
set GOOGLE_CSE_ENGINE_ID=your_engine_id_here
set SEARCH_PROVIDER=google_cse
```

### Linux/Mac
```bash
# For Google Custom Search
export GOOGLE_CSE_API_KEY="your_api_key_here"
export GOOGLE_CSE_ENGINE_ID="your_engine_id_here"
export SEARCH_PROVIDER="google_cse"

# For SerpAPI
export SERPAPI_KEY="your_api_key_here"
export SEARCH_PROVIDER="serpapi"

# For Bing
export BING_SEARCH_KEY="your_api_key_here"
export SEARCH_PROVIDER="bing"
```

### Permanent Setup (Windows)
Use `setx` to make environment variables persistent:
```cmd
setx GOOGLE_CSE_API_KEY "your_api_key_here"
setx GOOGLE_CSE_ENGINE_ID "your_engine_id_here"
setx SEARCH_PROVIDER "google_cse"
```
**Note:** You'll need to restart your terminal/IDE after using `setx`.

### Permanent Setup (Linux/Mac)
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export GOOGLE_CSE_API_KEY="your_api_key_here"
export GOOGLE_CSE_ENGINE_ID="your_engine_id_here"
export SEARCH_PROVIDER="google_cse"
```

## Supported Providers

### 1. Google Custom Search JSON API
- **Free tier:** 100 queries/day
- **Get keys:** https://developers.google.com/custom-search/v1/overview
- **Required:** `GOOGLE_CSE_API_KEY` + `GOOGLE_CSE_ENGINE_ID`

### 2. SerpAPI
- **Free tier:** 100 queries/month
- **Get keys:** https://serpapi.com/
- **Required:** `SERPAPI_KEY`

### 3. Bing Web Search API
- **Free tier:** 3,000 queries/month
- **Get keys:** https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
- **Required:** `BING_SEARCH_KEY`

## Auto-Detection Priority

If multiple API keys are available, the notebook uses this priority:
1. Google Custom Search (if both key and engine ID are set)
2. SerpAPI (if key is set)
3. Bing Web Search (if key is set)

You can override by explicitly setting `SEARCH_PROVIDER`:
```bash
export SEARCH_PROVIDER="serpapi"  # Force SerpAPI even if Google keys exist
```

## How It Works

1. **Discovery:** The notebook searches for organizations using targeted queries for each of the 4 capabilities:
   - Regulatory / FDA
   - Clinical & Translational Support
   - IP / Legal / Licensing
   - Manufacturing / GMP / Scale-Up

2. **Filtering:** Results are scored by confidence (keyword matches, org indicators, URL quality)

3. **Prioritization:** Up to 25 new orgs per capability (100 total) are added immediately

4. **Backlog:** All additional candidates are saved to `expansion_backlog.csv` for future runs

5. **Deduplication:** New orgs are checked against existing database before adding

## Verification

When you run the notebook, you should see one of these messages:
- `✓ Auto-discovery enabled: Google Custom Search (keys found in environment)`
- `✓ Auto-discovery enabled: SerpAPI (key found in environment)`
- `✓ Auto-discovery enabled: Bing Web Search (key found in environment)`
- `ℹ Auto-discovery disabled: No API keys found in environment variables`

## Troubleshooting

**Q: Auto-discovery is not working**
- Check that environment variables are set: `echo $GOOGLE_CSE_API_KEY` (Linux/Mac) or `echo %GOOGLE_CSE_API_KEY%` (Windows)
- Restart your terminal/IDE after setting variables with `setx` (Windows)
- Verify API keys are valid and have remaining quota

**Q: Which provider should I use?**
- **Google CSE:** Best for general web search, requires creating a Custom Search Engine
- **SerpAPI:** Easiest setup, handles Google search results
- **Bing:** Good free tier (3,000 queries/month), straightforward API

**Q: Can I use multiple providers?**
- The notebook uses one provider at a time (priority order above)
- You can switch providers by changing `SEARCH_PROVIDER` environment variable

## Security Notes

- **Never commit API keys to git**
- Keys are read from environment variables only (never hardcoded)
- Use `.env` files or system environment variables
- Consider using a secrets manager for production

