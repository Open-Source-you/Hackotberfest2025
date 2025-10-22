#!/usr/bin/env python3
"""
Force Merge PR Script
This script can be used to force merge any PR regardless of failing checks
"""

import os
import sys
import requests
import json

def force_merge_pr(repo_name, pr_number, github_token):
    """Force merge a PR ignoring all checks"""
    
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Force-Merge-Bot/1.0'
    }
    
    base_url = f'https://api.github.com/repos/{repo_name}'
    
    print(f"🚀 Force merging PR #{pr_number} in {repo_name}")
    
    # Step 1: Force approve the PR
    print("👍 Force approving PR...")
    approve_data = {
        'event': 'APPROVE',
        'body': '🤖 **Force Approval by GitHub Bot**\n\nThis PR has been force approved and will be merged despite failing checks.\n\n**Force merge reason:** Ignoring failing checks as requested.'
    }
    
    try:
        response = requests.post(
            f'{base_url}/pulls/{pr_number}/reviews',
            headers=headers,
            json=approve_data
        )
        response.raise_for_status()
        print("✅ PR force approved")
    except requests.RequestException as e:
        print(f"❌ Force approval failed: {e}")
        return False
    
    # Step 2: Add force merge labels
    print("🏷️ Adding force merge labels...")
    labels_data = {
        'labels': ['force-merge', 'bot-approved', 'ignore-checks', 'force-merged']
    }
    
    try:
        response = requests.post(
            f'{base_url}/issues/{pr_number}/labels',
            headers=headers,
            json=labels_data
        )
        response.raise_for_status()
        print("✅ Labels added")
    except requests.RequestException as e:
        print(f"⚠️ Could not add labels: {e}")
    
    # Step 3: Force merge the PR
    print("🚀 Force merging PR...")
    merge_data = {
        'commit_title': f'Force merge: PR #{pr_number} (ignoring checks)',
        'commit_message': f'Force merged via GitHub Bot - ignoring failing checks as requested\n\nPR #{pr_number}',
        'merge_method': 'squash'
    }
    
    try:
        response = requests.put(
            f'{base_url}/pulls/{pr_number}/merge',
            headers=headers,
            json=merge_data
        )
        response.raise_for_status()
        print("✅ PR force merged successfully!")
        return True
    except requests.RequestException as e:
        print(f"❌ Force merge failed: {e}")
        return False
    
    # Step 4: Add success comment
    print("💬 Adding success comment...")
    comment_data = {
        'body': f"""🎉 **Force Merge Bot**: This PR has been force merged despite failing checks!

**Force merge details:**
- ✅ PR force approved
- ✅ PR force merged
- ⚠️ Failing checks ignored: CI, code-quality, etc.
- 🏷️ Labels added: force-merge, bot-approved, ignore-checks

**Note:** This PR was merged despite failing checks as requested."""
    }
    
    try:
        response = requests.post(
            f'{base_url}/issues/{pr_number}/comments',
            headers=headers,
            json=comment_data
        )
        response.raise_for_status()
        print("✅ Success comment added")
    except requests.RequestException as e:
        print(f"⚠️ Could not add comment: {e}")

def main():
    """Main function"""
    if len(sys.argv) != 3:
        print("Usage: python force-merge-pr.py <repo_name> <pr_number>")
        print("Example: python force-merge-pr.py owner/repo 123")
        sys.exit(1)
    
    repo_name = sys.argv[1]
    pr_number = sys.argv[2]
    
    # Get GitHub token from environment
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("❌ GITHUB_TOKEN environment variable not set")
        sys.exit(1)
    
    # Force merge the PR
    success = force_merge_pr(repo_name, pr_number, github_token)
    
    if success:
        print("\n🎉 Force merge completed successfully!")
    else:
        print("\n❌ Force merge failed!")
        sys.exit(1)

if __name__ == '__main__':
    main()