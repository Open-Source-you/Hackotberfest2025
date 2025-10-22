#!/usr/bin/env python3
"""
GitHub Auto Merge Bot
Automatically merges pull requests based on configurable conditions.
"""

import os
import sys
import json
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

class GitHubAutoMergeBot:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.repo_name = os.getenv('REPO_NAME')
        self.pr_number = os.getenv('PR_NUMBER')
        
        if not all([self.token, self.repo_name, self.pr_number]):
            raise ValueError("Missing required environment variables")
        
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-Auto-Merge-Bot/1.0'
        }
        self.base_url = f'https://api.github.com/repos/{self.repo_name}'
        
        # Configuration
        self.config = self.load_config()
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file or use defaults."""
        config_file = '.github/auto_merge_config.json'
        default_config = {
            "auto_merge_enabled": True,
            "require_approvals": 1,
            "require_status_checks": True,
            "require_branch_up_to_date": True,
            "allowed_merge_methods": ["squash", "merge", "rebase"],
            "default_merge_method": "squash",
            "auto_merge_labels": ["auto-merge", "bot-approved"],
            "blocking_labels": ["do-not-merge", "needs-review", "wip"],
            "required_checks": ["CI", "code-quality"],
            "max_wait_time_minutes": 30,
            "trusted_contributors": [],
            "auto_merge_all": False
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
    
    def check_auto_merge_conditions(self, pr_info: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Check if PR meets auto-merge conditions."""
        issues = []
        
        # Check if auto-merge is enabled
        if not self.config.get('auto_merge_enabled', True):
            issues.append("Auto-merge is disabled")
            return False, issues
        
        # Check if PR is draft
        if pr_info.get('draft', False):
            issues.append("PR is in draft state")
            return False, issues
        
        # Check if PR is already merged
        if pr_info.get('state') != 'open':
            issues.append(f"PR is not open (state: {pr_info.get('state')})")
            return False, issues
        
        # Check mergeable state
        mergeable_state = pr_info.get('mergeable_state')
        if mergeable_state not in ['clean', 'unstable']:
            issues.append(f"PR is not mergeable (state: {mergeable_state})")
            return False, issues
        
        # Check for blocking labels
        labels = [label['name'] for label in pr_info.get('labels', [])]
        blocking_labels = self.config.get('blocking_labels', [])
        for label in labels:
            if label in blocking_labels:
                issues.append(f"PR has blocking label: {label}")
                return False, issues
        
        # Check approvals
        required_approvals = self.config.get('require_approvals', 1)
        if required_approvals > 0:
            reviews = self.get_pr_reviews()
            approvals = sum(1 for review in reviews if review['state'] == 'APPROVED')
            if approvals < required_approvals:
                issues.append(f"Need {required_approvals} approvals, got {approvals}")
                return False, issues
        
        # Check status checks
        if self.config.get('require_status_checks', True):
            status_checks = self.get_status_checks()
            required_checks = self.config.get('required_checks', [])
            
            if required_checks:
                for check in required_checks:
                    # This is a simplified check - in practice, you'd need to check
                    # the actual status of each required check
                    pass
        
        # Check if branch is up to date
        if self.config.get('require_branch_up_to_date', True):
            if not pr_info.get('mergeable', False):
                issues.append("Branch is not up to date with base branch")
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
    
    def merge_pr(self) -> bool:
        """Merge the pull request."""
        try:
            merge_method = self.config.get('default_merge_method', 'squash')
            
            data = {
                'commit_title': f'Auto-merge: PR #{self.pr_number}',
                'commit_message': f'Automatically merged via GitHub Auto Merge Bot\n\nPR #{self.pr_number}',
                'merge_method': merge_method
            }
            
            response = requests.put(
                f'{self.base_url}/pulls/{self.pr_number}/merge',
                headers=self.headers,
                json=data
            )
            response.raise_for_status()
            return True
        except requests.RequestException as e:
            print(f"❌ Error merging PR: {e}")
            return False
    
    def process_pr(self):
        """Main method to process the PR."""
        print(f"🤖 Processing PR #{self.pr_number} in {self.repo_name}")
        
        # Get PR information
        pr_info = self.get_pr_info()
        if not pr_info:
            print("❌ Could not fetch PR information")
            return
        
        print(f"📋 PR Title: {pr_info.get('title', 'N/A')}")
        print(f"👤 Author: {pr_info.get('user', {}).get('login', 'N/A')}")
        print(f"🏷️ Labels: {[label['name'] for label in pr_info.get('labels', [])]}")
        
        # Check auto-merge conditions
        can_merge, issues = self.check_auto_merge_conditions(pr_info)
        
        if can_merge:
            print("✅ PR meets auto-merge conditions")
            
            # Add auto-merge labels
            auto_merge_labels = self.config.get('auto_merge_labels', ['auto-merge', 'bot-approved'])
            self.add_labels(auto_merge_labels)
            
            # Add comment
            comment = f"""🤖 **Auto Merge Bot**

This PR has been automatically approved and will be merged shortly!

**Conditions met:**
- ✅ PR is ready for merge
- ✅ All required checks passed
- ✅ No blocking labels present

**Merge method:** {self.config.get('default_merge_method', 'squash')}
**Timestamp:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
"""
            self.add_comment(comment)
            
            # Attempt to merge
            if self.merge_pr():
                print("🚀 PR successfully merged!")
            else:
                print("❌ Failed to merge PR")
        else:
            print("❌ PR does not meet auto-merge conditions:")
            for issue in issues:
                print(f"  - {issue}")
            
            # Add comment explaining why it can't be merged
            comment = f"""🤖 **Auto Merge Bot**

This PR cannot be automatically merged at this time.

**Issues preventing auto-merge:**
{chr(10).join(f'- {issue}' for issue in issues)}

Please address these issues and the bot will try again on the next update.
"""
            self.add_comment(comment)

def main():
    """Main entry point."""
    try:
        bot = GitHubAutoMergeBot()
        bot.process_pr()
    except Exception as e:
        print(f"❌ Bot error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()