#!/usr/bin/env python3
"""
Script to help push the AI Typing Assistant to GitHub
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a git command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} successful")
            if result.stdout.strip():
                print(result.stdout.strip())
        else:
            print(f"❌ {description} failed:")
            print(result.stderr.strip())
            return False
    except Exception as e:
        print(f"❌ Error during {description}: {e}")
        return False
    return True

def main():
    """Main function to push to GitHub"""
    print("🚀 AI Typing Assistant - GitHub Push Helper")
    print("=" * 50)
    
    # Check if we're in a git repository
    if not os.path.exists(".git"):
        print("❌ Not in a git repository. Run 'git init' first.")
        return
    
    # Check current status
    print("\n📊 Current repository status:")
    run_command("git status", "Checking repository status")
    
    # Get remote URL from user
    print("\n🔗 To push to GitHub:")
    print("1. Create a new repository on GitHub")
    print("2. Copy the repository URL (e.g., https://github.com/username/ai-typing-assistant.git)")
    print("3. Run the following commands:")
    print()
    print("git remote add origin <your-repository-url>")
    print("git branch -M main")
    print("git push -u origin main")
    print()
    
    # Ask if user wants to add remote
    remote_url = input("Enter your GitHub repository URL (or press Enter to skip): ").strip()
    
    if remote_url:
        # Add remote
        if run_command(f'git remote add origin "{remote_url}"', "Adding remote origin"):
            # Rename branch to main
            if run_command("git branch -M main", "Renaming branch to main"):
                # Push to GitHub
                if run_command("git push -u origin main", "Pushing to GitHub"):
                    print("\n🎉 Successfully pushed to GitHub!")
                    print(f"📋 Repository URL: {remote_url}")
                else:
                    print("\n❌ Failed to push to GitHub. Check your repository URL and try again.")
            else:
                print("\n❌ Failed to rename branch.")
        else:
            print("\n❌ Failed to add remote. Check your repository URL.")
    else:
        print("\n📝 Manual push instructions:")
        print("1. Create a repository on GitHub")
        print("2. Run: git remote add origin <your-repo-url>")
        print("3. Run: git branch -M main")
        print("4. Run: git push -u origin main")

if __name__ == "__main__":
    main() 