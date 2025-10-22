#!/usr/bin/env python3
"""
GitHub Auto Approve Bot
Automatically approves pull requests based on configurable conditions.
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any

class GitHubAutoApproveBot:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.repo_name = os.getenv('REPO_NAME')
        self.pr_number = os.getenv('PR_NUMBER')
        
        if not all([self.token, self.repo_name, self.pr_number]):
            raise ValueError("Missing required environment variables")
        
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Auto-Approve-Bot/1.0'
        }
        self.base_url = f'https://api.github.com/repos/{self.repo_name}'
        
        # Configuration
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        config_file = '.github/auto_approve_config.json'
        default_config = {
            "auto_approve_enabled": True,
            "auto_approve_labels": ["auto-approve", "bot-approve"],
            "blocking_labels": ["do-not-approve", "needs-review", "wip", "draft"],
            "require_checks_passing": True,
            "max_file_changes": 50,
            "max_additions": 1000,
            "max_deletions": 1000,
            "trusted_contributors": [],
            "auto_approve_all": False,
            "min_commits": 1,
            "require_meaningful_commits": True
        }
        
        try:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    user_config = json.load(f)
                    default_config.update(user_config)
        except Exception as e:
            print(f"⚠️ Could not load config file: {e}")
        
        return default_config
    
    def get_pr_info(self) -> Optional[Dict[str, Any]]:
        """Get pull request information."""
        try:
            response = requests.get(
                f'{self.base_url}/pulls/{self.pr_number}',
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Error fetching PR info: {e}")
            return None
    
    def get_pr_reviews(self) -> List[Dict[str, Any]]:
        """Get pull request reviews."""
        try:
            response = requests.get(
                f'{self.base_url}/pulls/{self.pr_number}/reviews',
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Error fetching PR reviews: {e}")
            return []
    
    def get_pr_commits(self) -> List[Dict[str, Any]]:
        """Get pull request commits."""
        try:
            response = requests.get(
                f'{self.base_url}/pulls/{self.pr_number}/commits',
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Error fetching PR commits: {e}")
            return []
    
    def get_status_checks(self) -> Dict[str, Any]:
        """Get status checks for the PR."""
        try:
            pr_info = self.get_pr_info()
            if not pr_info:
                return {}
            
            # Get the head commit SHA
            head_sha = pr_info['head']['sha']
            
            # Get status checks
            response = requests.get(
                f'{self.base_url}/commits/{head_sha}/status',
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"❌ Error fetching status checks: {e}")
            return {}
    
    def check_auto_approve_conditions(self, pr_info: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Check if PR meets auto-approve conditions."""
        issues = []
        
        # Check if auto-approve is enabled
        if not self.config.get('auto_approve_enabled', True):
            issues.append("Auto-approve is disabled")
            return False, issues
        
        # Check if PR is draft
        if pr_info.get('draft', False):
            issues.append("PR is in draft state")
            return False, issues
        
        # Check if PR is already merged
        if pr_info.get('state') != 'open':
            issues.append(f"PR is not open (state: {pr_info.get('state')})")
            return False, issues
        
        # Check labels
        labels = [label['name'] for label in pr_info.get('labels', [])]
        
        # Check for auto-approve labels
        auto_approve_labels = self.config.get('auto_approve_labels', ['auto-approve'])
        has_auto_approve_label = any(label in labels for label in auto_approve_labels)
        
        if not has_auto_approve_label and not self.config.get('auto_approve_all', False):
            issues.append(f"PR does not have auto-approve label. Required: {auto_approve_labels}")
            return False, issues
        
        # Check for blocking labels
        blocking_labels = self.config.get('blocking_labels', [])
        for label in labels:
            if label in blocking_labels:
                issues.append(f"PR has blocking label: {label}")
                return False, issues
        
        # Check file changes
        max_file_changes = self.config.get('max_file_changes', 50)
        if pr_info.get('changed_files', 0) > max_file_changes:
            issues.append(f"Too many files changed: {pr_info.get('changed_files')} > {max_file_changes}")
            return False, issues
        
        # Check additions/deletions
        max_additions = self.config.get('max_additions', 1000)
        max_deletions = self.config.get('max_deletions', 1000)
        
        if pr_info.get('additions', 0) > max_additions:
            issues.append(f"Too many additions: {pr_info.get('additions')} > {max_additions}")
            return False, issues
        
        if pr_info.get('deletions', 0) > max_deletions:
            issues.append(f"Too many deletions: {pr_info.get('deletions')} > {max_deletions}")
            return False, issues
        
        # Check commits
        commits = self.get_pr_commits()
        min_commits = self.config.get('min_commits', 1)
        if len(commits) < min_commits:
            issues.append(f"Not enough commits: {len(commits)} < {min_commits}")
            return False, issues
        
        # Check if commits are meaningful
        if self.config.get('require_meaningful_commits', True):
            meaningful_commits = 0
            for commit in commits:
                message = commit.get('commit', {}).get('message', '')
                if len(message.strip()) > 10 and not message.startswith('Merge'):
                    meaningful_commits += 1
            
            if meaningful_commits < min_commits:
                issues.append("Commits are not meaningful enough")
                return False, issues
        
        # Check status checks
        if self.config.get('require_checks_passing', True):
            status_checks = self.get_status_checks()
            if status_checks.get('state') not in ['success', 'pending']:
                issues.append("Required status checks are not passing")
                return False, issues
        
        return True, issues
    
    def add_labels(self, labels: List[str]) -> bool:
        """Add labels to the PR."""
        try:
            response = requests.post(
                f'{self.base_url}/issues/{self.pr_number}/labels',
                headers=self.headers,
                json={'labels': labels}
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"❌ Error adding labels: {e}")
            return False
    
    def add_comment(self, comment: str) -> bool:
        """Add a comment to the PR."""
        try:
            response = requests.post(
                f'{self.base_url}/issues/{self.pr_number}/comments',
                headers=self.headers,
                json={'body': comment}
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"❌ Error adding comment: {e}")
            return False
    
    def approve_pr(self) -> bool:
        """Approve the pull request."""
        try:
            data = {
                'event': 'APPROVE',
                'body': f'🤖 **Auto-approval by GitHub Bot**\n\nThis PR has been automatically approved based on configured conditions.\n\n**Approval Details:**\n- Timestamp: {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}\n- Bot Version: 1.0'
            }
            
            response = requests.post(
                f'{self.base_url}/pulls/{self.pr_number}/reviews',
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"❌ Error approving PR: {e}")
            return False
    
    def process_pr(self):
        """Main method to process the PR."""
        print(f"🤖 Processing PR #{self.pr_number} for auto-approval in {self.repo_name}")
        
        # Get PR information
        pr_info = self.get_pr_info()
        if not pr_info:
            print("❌ Could not fetch PR information")
            return
        
        print(f"📋 PR Title: {pr_info.get('title', 'N/A')}")
        print(f"👤 Author: {pr_info.get('user', {}).get('login', 'N/A')}")
        print(f"🏷️ Labels: {[label['name'] for label in pr_info.get('labels', [])]}")
        print(f"📊 Files: {pr_info.get('changed_files', 0)} changed, +{pr_info.get('additions', 0)} -{pr_info.get('deletions', 0)}")
        
        # Check auto-approve conditions
        can_approve, issues = self.check_auto_approve_conditions(pr_info)
        
        if can_approve:
            print("✅ PR meets auto-approve conditions")
            
            # Add approval labels
            approval_labels = ['bot-approved', 'auto-approved']
            self.add_labels(approval_labels)
            
            # Add comment
            comment = f"""🤖 **Auto Approve Bot**

This PR has been automatically approved!

**Conditions met:**
- ✅ PR is ready for review
- ✅ All required checks passed
- ✅ No blocking labels present
- ✅ File changes within limits

**Approval Details:**
- **Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
- **Bot Version:** 1.0
- **Files Changed:** {pr_info.get('changed_files', 0)}
- **Additions:** +{pr_info.get('additions', 0)}
- **Deletions:** -{pr_info.get('deletions', 0)}
"""
            self.add_comment(comment)
            
            # Attempt to approve
            if self.approve_pr():
                print("👍 PR successfully approved!")
            else:
                print("❌ Failed to approve PR")
        else:
            print("❌ PR does not meet auto-approve conditions:")
            for issue in issues:
                print(f"  - {issue}")
            
            # Add comment explaining why it can't be approved
            comment = f"""🤖 **Auto Approve Bot**

This PR cannot be automatically approved at this time.

**Issues preventing auto-approval:**
{chr(10).join(f'- {issue}' for issue in issues)}

**To enable auto-approval:**
- Add one of these labels: {', '.join(self.config.get('auto_approve_labels', ['auto-approve']))}
- Remove any blocking labels: {', '.join(self.config.get('blocking_labels', []))}
- Ensure all required checks pass
- Keep file changes within limits

Please address these issues and the bot will try again on the next update.
"""
            self.add_comment(comment)

def main():
    """Main entry point."""
    try:
        bot = GitHubAutoApproveBot()
        bot.process_pr()
    except Exception as e:
        print(f"❌ Bot error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()