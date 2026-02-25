@echo off
echo "🚀 INITIATING HYPERCODE LAUNCH SEQUENCE..."
echo "---------------------------------------------"

:: 1. Check for GH_TOKEN
if "%GH_TOKEN%"=="" (
    echo "⚠️  WARNING: GH_TOKEN not set. Topic update will be skipped."
    echo "👉 Set it with: $env:GH_TOKEN='your_token'"
) else (
    echo "✅ GH_TOKEN detected. Updating Repository Topics..."
    python update_topics.py
)

:: 2. Display Launch Content
echo.
echo "---------------------------------------------"
echo "📢 LAUNCH CONTENT READY (Copy & Post):"
echo "---------------------------------------------"
type docs\strategy\LAUNCH_KIT.md

echo.
echo "---------------------------------------------"
echo "✅ DEPLOYMENT PREP COMPLETE"
echo "👉 NEXT STEP: Go to GitHub Repo -> Settings -> Pages -> Source: /docs"
echo "👉 NEXT STEP: Post the content above to Reddit/Twitter"
echo "---------------------------------------------"
pause
