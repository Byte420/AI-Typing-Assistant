# AI Typing Assistant - GitHub Push Helper
Write-Host "🚀 AI Typing Assistant - GitHub Push Helper" -ForegroundColor Cyan
Write-Host "===========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "📝 Instructions:" -ForegroundColor Yellow
Write-Host "1. Create a repository on GitHub.com"
Write-Host "2. Enter your GitHub username and repository name below"
Write-Host "3. This script will push your code to GitHub"
Write-Host ""

$username = Read-Host "Enter your GitHub username"
$repo_name = Read-Host "Enter your repository name"

Write-Host ""
Write-Host "📋 Repository URL: https://github.com/$username/$repo_name" -ForegroundColor Green
Write-Host ""

$confirm = Read-Host "Ready to push? (y/n)"

if ($confirm -eq "y" -or $confirm -eq "Y") {
    Write-Host ""
    Write-Host "🔄 Adding remote origin..." -ForegroundColor Yellow
    git remote add origin "https://github.com/$username/$repo_name.git"
    
    Write-Host ""
    Write-Host "🔄 Setting branch to main..." -ForegroundColor Yellow
    git branch -M main
    
    Write-Host ""
    Write-Host "🔄 Pushing to GitHub..." -ForegroundColor Yellow
    git push -u origin main
    
    Write-Host ""
    Write-Host "✅ Done! Your code is now on GitHub." -ForegroundColor Green
    Write-Host "📋 Repository URL: https://github.com/$username/$repo_name" -ForegroundColor Green
} else {
    Write-Host "❌ Cancelled by user." -ForegroundColor Red
}

Read-Host "Press Enter to continue" 