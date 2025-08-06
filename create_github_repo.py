#!/usr/bin/env python3
"""
Script to help create and push to GitHub repository
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} successful")
            if result.stdout.strip():
                print(result.stdout.strip())
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr.strip())
            return False
    except Exception as e:
        print(f"❌ Error during {description}: {e}")
        return False

def main():
    """Main function to create and push to GitHub"""
    print("🚀 AI Typing Assistant - GitHub Repository Setup")
    print("=" * 60)
    
    # Check if we're in a git repository
    if not os.path.exists(".git"):
        print("❌ Not in a git repository. Run 'git init' first.")
        return
    
    # Check current status
    print("\n📊 Current repository status:")
    run_command("git status", "Checking repository status")
    
    print("\n🔗 To push to GitHub, you need to:")
    print("1. Create a new repository on GitHub.com")
    print("2. Copy the repository URL")
    print("3. Add it as a remote and push")
    
    # Get repository name from user
    repo_name = input("\nEnter your desired repository name (e.g., ai-typing-assistant): ").strip()
    
    if not repo_name:
        print("❌ Repository name is required.")
        return
    
    # Get GitHub username
    username = input("Enter your GitHub username: ").strip()
    
    if not username:
        print("❌ GitHub username is required.")
        return
    
    # Construct repository URL
    repo_url = f"https://github.com/{username}/{repo_name}.git"
    
    print(f"\n📋 Repository URL will be: {repo_url}")
    print("\n📝 Steps to complete:")
    print(f"1. Go to https://github.com/new")
    print(f"2. Create repository named: {repo_name}")
    print(f"3. Make it public or private (your choice)")
    print(f"4. DO NOT initialize with README (we already have one)")
    print(f"5. Click 'Create repository'")
    
    confirm = input(f"\nReady to push to {repo_url}? (y/n): ").strip().lower()
    
    if confirm != 'y':
        print("❌ Cancelled by user.")
        return
    
    # Add remote
    if run_command(f'git remote add origin "{repo_url}"', "Adding remote origin"):
        # Rename branch to main if needed
        run_command("git branch -M main", "Setting branch to main")
        
        # Push to GitHub
        if run_command("git push -u origin main", "Pushing to GitHub"):
            print("\n🎉 Successfully pushed to GitHub!")
            print(f"📋 Repository URL: https://github.com/{username}/{repo_name}")
            print(f"🔗 Clone URL: {repo_url}")
        else:
            print("\n❌ Failed to push to GitHub.")
            print("Possible issues:")
            print("- Repository doesn't exist on GitHub")
            print("- Authentication issues")
            print("- Network connectivity")
    else:
        print("\n❌ Failed to add remote.")

if __name__ == "__main__":
    main() 