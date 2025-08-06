@echo off
echo 🚀 AI Typing Assistant - GitHub Push Helper
echo ============================================
echo.
echo 📝 Instructions:
echo 1. Create a repository on GitHub.com
echo 2. Enter your GitHub username and repository name below
echo 3. This script will push your code to GitHub
echo.
set /p username="Enter your GitHub username: "
set /p repo_name="Enter your repository name: "
echo.
echo 📋 Repository URL: https://github.com/%username%/%repo_name%
echo.
set /p confirm="Ready to push? (y/n): "
if /i "%confirm%"=="y" (
    echo.
    echo 🔄 Adding remote origin...
    git remote add origin https://github.com/%username%/%repo_name%.git
    echo.
    echo 🔄 Setting branch to main...
    git branch -M main
    echo.
    echo 🔄 Pushing to GitHub...
    git push -u origin main
    echo.
    echo ✅ Done! Your code is now on GitHub.
    echo 📋 Repository URL: https://github.com/%username%/%repo_name%
) else (
    echo ❌ Cancelled by user.
)
pause 