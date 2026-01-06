#!/bin/bash
# ============================================
# ESO Auto-Discovery API Setup Script
# ============================================
# This script helps you set up environment variables for auto-discovery
# Run this script before executing the notebook: source setup_search_api.sh
# ============================================

echo ""
echo "============================================"
echo "ESO Auto-Discovery API Setup"
echo "============================================"
echo ""
echo "Choose your search API provider:"
echo ""
echo "1. Google Custom Search (requires API key + Engine ID)"
echo "2. SerpAPI (requires API key)"
echo "3. Bing Web Search (requires API key)"
echo "4. Skip / Disable auto-discovery"
echo ""
read -p "Enter your choice (1-4): " choice

case $choice in
    1)
        echo ""
        read -p "Enter your Google CSE API Key: " GOOGLE_CSE_API_KEY
        read -p "Enter your Google CSE Engine ID: " GOOGLE_CSE_ENGINE_ID
        export GOOGLE_CSE_API_KEY
        export GOOGLE_CSE_ENGINE_ID
        export SEARCH_PROVIDER="google_cse"
        echo "export GOOGLE_CSE_API_KEY=\"$GOOGLE_CSE_API_KEY\"" >> ~/.bashrc
        echo "export GOOGLE_CSE_ENGINE_ID=\"$GOOGLE_CSE_ENGINE_ID\"" >> ~/.bashrc
        echo "export SEARCH_PROVIDER=\"google_cse\"" >> ~/.bashrc
        echo ""
        echo "✓ Google Custom Search configured!"
        echo "  Environment variables set for this session and added to ~/.bashrc"
        ;;
    2)
        echo ""
        read -p "Enter your SerpAPI Key: " SERPAPI_KEY
        export SERPAPI_KEY
        export SEARCH_PROVIDER="serpapi"
        echo "export SERPAPI_KEY=\"$SERPAPI_KEY\"" >> ~/.bashrc
        echo "export SEARCH_PROVIDER=\"serpapi\"" >> ~/.bashrc
        echo ""
        echo "✓ SerpAPI configured!"
        echo "  Environment variables set for this session and added to ~/.bashrc"
        ;;
    3)
        echo ""
        read -p "Enter your Bing Search API Key: " BING_SEARCH_KEY
        export BING_SEARCH_KEY
        export SEARCH_PROVIDER="bing"
        echo "export BING_SEARCH_KEY=\"$BING_SEARCH_KEY\"" >> ~/.bashrc
        echo "export SEARCH_PROVIDER=\"bing\"" >> ~/.bashrc
        echo ""
        echo "✓ Bing Web Search configured!"
        echo "  Environment variables set for this session and added to ~/.bashrc"
        ;;
    4)
        export SEARCH_PROVIDER="none"
        echo ""
        echo "✓ Auto-discovery disabled."
        ;;
    *)
        echo "Invalid choice. Auto-discovery disabled."
        export SEARCH_PROVIDER="none"
        ;;
esac

echo ""
echo "============================================"
echo "Setup complete!"
echo "============================================"
echo ""
echo "To get API keys:"
echo "  - Google CSE: https://developers.google.com/custom-search/v1/overview"
echo "  - SerpAPI: https://serpapi.com/"
echo "  - Bing: https://www.microsoft.com/en-us/bing/apis/bing-web-search-api"
echo ""

