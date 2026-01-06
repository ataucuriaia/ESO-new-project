@echo off
REM ============================================
REM ESO Auto-Discovery API Setup Script
REM ============================================
REM This script helps you set up environment variables for auto-discovery
REM Run this script before executing the notebook
REM ============================================

echo.
echo ============================================
echo ESO Auto-Discovery API Setup
echo ============================================
echo.
echo Choose your search API provider:
echo.
echo 1. Google Custom Search (requires API key + Engine ID)
echo 2. SerpAPI (requires API key)
echo 3. Bing Web Search (requires API key)
echo 4. Skip / Disable auto-discovery
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo.
    set /p GOOGLE_CSE_API_KEY="Enter your Google CSE API Key: "
    set /p GOOGLE_CSE_ENGINE_ID="Enter your Google CSE Engine ID: "
    setx GOOGLE_CSE_API_KEY "%GOOGLE_CSE_API_KEY%"
    setx GOOGLE_CSE_ENGINE_ID "%GOOGLE_CSE_ENGINE_ID%"
    setx SEARCH_PROVIDER "google_cse"
    echo.
    echo ✓ Google Custom Search configured!
    echo   Note: You may need to restart your terminal/IDE for changes to take effect.
)

if "%choice%"=="2" (
    echo.
    set /p SERPAPI_KEY="Enter your SerpAPI Key: "
    setx SERPAPI_KEY "%SERPAPI_KEY%"
    setx SEARCH_PROVIDER "serpapi"
    echo.
    echo ✓ SerpAPI configured!
    echo   Note: You may need to restart your terminal/IDE for changes to take effect.
)

if "%choice%"=="3" (
    echo.
    set /p BING_SEARCH_KEY="Enter your Bing Search API Key: "
    setx BING_SEARCH_KEY "%BING_SEARCH_KEY%"
    setx SEARCH_PROVIDER "bing"
    echo.
    echo ✓ Bing Web Search configured!
    echo   Note: You may need to restart your terminal/IDE for changes to take effect.
)

if "%choice%"=="4" (
    setx SEARCH_PROVIDER "none"
    echo.
    echo ✓ Auto-discovery disabled.
)

echo.
echo ============================================
echo Setup complete!
echo ============================================
echo.
echo To get API keys:
echo   - Google CSE: https://developers.google.com/custom-search/v1/overview
echo   - SerpAPI: https://serpapi.com/
echo   - Bing: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api
echo.
pause

