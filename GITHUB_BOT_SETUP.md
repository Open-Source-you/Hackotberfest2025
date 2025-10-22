# GitHub Auto Merge & Approve Bot Setup Guide

यह गाइड आपको GitHub repository में automatic PR acceptance और approval के लिए bot setup करने में मदद करेगा।

## 🤖 Bot Features

### Auto Merge Bot
- Automatically merges PRs when conditions are met
- Configurable merge conditions and requirements
- Support for different merge methods (squash, merge, rebase)
- Smart labeling and commenting

### Auto Approve Bot
- Automatically approves PRs based on configurable rules
- File change limits and commit requirements
- Label-based approval system
- Detailed approval comments

## 📁 Files Created

```
.github/
├── workflows/
│   ├── auto-merge-pr.yml          # Auto merge workflow
│   └── pr-auto-approve.yml        # Auto approve workflow
├── scripts/
│   ├── auto_merge_bot.py          # Advanced merge bot script
│   └── auto_approve_bot.py        # Advanced approve bot script
├── auto_merge_config.json         # Merge bot configuration
└── auto_approve_config.json       # Approve bot configuration
```

## 🚀 Setup Instructions

### 1. Repository Permissions

Ensure your repository has the following permissions enabled:

1. Go to **Settings** → **Actions** → **General**
2. Under **Workflow permissions**, select:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**

### 2. Branch Protection Rules (Optional but Recommended)

1. Go to **Settings** → **Branches**
2. Add rule for your main branch:
   - ✅ **Require pull request reviews before merging**
   - ✅ **Require status checks to pass before merging**
   - ✅ **Require branches to be up to date before merging**

### 3. Configure Bot Settings

#### Auto Merge Configuration (`.github/auto_merge_config.json`)

```json
{
  "auto_merge_enabled": true,
  "require_approvals": 1,
  "require_status_checks": true,
  "require_branch_up_to_date": true,
  "default_merge_method": "squash",
  "auto_merge_labels": ["auto-merge", "bot-approved"],
  "blocking_labels": ["do-not-merge", "needs-review", "wip"],
  "required_checks": ["CI", "code-quality"]
}
```

#### Auto Approve Configuration (`.github/auto_approve_config.json`)

```json
{
  "auto_approve_enabled": true,
  "auto_approve_labels": ["auto-approve", "bot-approve"],
  "blocking_labels": ["do-not-approve", "needs-review", "wip"],
  "max_file_changes": 50,
  "max_additions": 1000,
  "max_deletions": 1000
}
```

## 🎯 How to Use

### For Auto Merge:

1. **Create a PR** with the label `auto-merge`
2. **Ensure all checks pass** (CI, tests, etc.)
3. **Get required approvals** (default: 1)
4. **Bot will automatically merge** when conditions are met

### For Auto Approve:

1. **Create a PR** with the label `auto-approve`
2. **Ensure file changes are within limits**
3. **Bot will automatically approve** the PR
4. **Manual merge** or use auto-merge bot for final merge

## 🏷️ Available Labels

### Auto Merge Labels:
- `auto-merge` - Triggers automatic merging
- `bot-approved` - Added by bot when conditions are met

### Auto Approve Labels:
- `auto-approve` - Triggers automatic approval
- `bot-approve` - Alternative trigger for approval

### Blocking Labels:
- `do-not-merge` - Prevents auto-merge
- `do-not-approve` - Prevents auto-approval
- `needs-review` - Requires manual review
- `wip` - Work in progress, blocks both actions

## ⚙️ Configuration Options

### Auto Merge Bot Settings:

| Setting | Description | Default |
|---------|-------------|---------|
| `auto_merge_enabled` | Enable/disable auto-merge | `true` |
| `require_approvals` | Minimum approvals required | `1` |
| `require_status_checks` | Require all checks to pass | `true` |
| `require_branch_up_to_date` | Require branch to be up to date | `true` |
| `default_merge_method` | Merge method (squash/merge/rebase) | `squash` |
| `max_wait_time_minutes` | Max wait time for conditions | `30` |

### Auto Approve Bot Settings:

| Setting | Description | Default |
|---------|-------------|---------|
| `auto_approve_enabled` | Enable/disable auto-approval | `true` |
| `max_file_changes` | Maximum files that can be changed | `50` |
| `max_additions` | Maximum lines that can be added | `1000` |
| `max_deletions` | Maximum lines that can be deleted | `1000` |
| `min_commits` | Minimum commits required | `1` |
| `require_meaningful_commits` | Require meaningful commit messages | `true` |

## 🔧 Customization

### Adding Custom Conditions:

1. Edit the respective bot script (`.github/scripts/`)
2. Modify the `check_*_conditions` method
3. Add your custom logic
4. Update the configuration file as needed

### Adding Notifications:

Configure webhook URLs in the config files:

```json
{
  "notifications": {
    "slack_webhook": "https://hooks.slack.com/...",
    "discord_webhook": "https://discord.com/api/webhooks/...",
    "email_notifications": false
  }
}
```

## 🐛 Troubleshooting

### Common Issues:

1. **Bot not running**: Check workflow permissions
2. **PR not merging**: Verify all conditions are met
3. **Approval not working**: Check labels and file limits
4. **Permission errors**: Ensure proper GitHub token permissions

### Debug Steps:

1. Check **Actions** tab for workflow runs
2. Review workflow logs for error messages
3. Verify configuration files are valid JSON
4. Ensure required labels are present

## 📝 Example Workflows

### Basic Auto Merge:
```yaml
# Add to PR description or as a comment
/auto-merge
```

### Basic Auto Approve:
```yaml
# Add to PR description or as a comment
/auto-approve
```

### Manual Override:
```yaml
# Add blocking label to prevent auto-actions
/do-not-merge
/do-not-approve
```

## 🔒 Security Considerations

1. **Review all PRs** before enabling auto-merge
2. **Set appropriate file limits** to prevent large changes
3. **Use branch protection rules** for important branches
4. **Monitor bot activity** regularly
5. **Keep configuration files secure**

## 📞 Support

If you encounter any issues:

1. Check the workflow logs in the **Actions** tab
2. Review the configuration files for errors
3. Ensure all required permissions are set
4. Verify the bot scripts are properly configured

## 🎉 Success!

Once setup is complete, your GitHub repository will have:

- ✅ Automatic PR merging based on conditions
- ✅ Automatic PR approval with smart filtering
- ✅ Configurable rules and limits
- ✅ Detailed logging and comments
- ✅ Label-based control system

Happy coding! 🚀