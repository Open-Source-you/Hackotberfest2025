# Omio PR Reviewer Bot Setup

This repository is configured with the **omio-labs/pr-reviewer-bot@v1** action for automated PR review and merging.

## 🤖 What This Bot Does

- **Automatically reviews** all pull requests
- **Auto-approves** PRs that meet the configured criteria
- **Auto-merges** PRs once all conditions are satisfied
- **Adds labels** to track bot-processed PRs
- **Leaves comments** with review status and next steps

## 📋 Configuration

The bot is configured via `.github/omio-bot-config.yml` with the following key settings:

### Auto-Review Settings
- ✅ **Auto-approve**: Enabled
- ✅ **Auto-merge**: Enabled  
- ✅ **Merge method**: Squash
- ✅ **Required approvals**: 1 (bot approval counts)

### File Patterns
The bot reviews these file types:
- Python (`.py`)
- JavaScript/TypeScript (`.js`, `.ts`, `.tsx`, `.jsx`)
- Java (`.java`)
- C/C++ (`.cpp`, `.c`, `.h`)
- Go (`.go`)
- Rust (`.rs`)
- And many more...

### Excluded Patterns
The bot skips these directories/files:
- `node_modules/`, `vendor/`, `target/`, `build/`, `dist/`
- Test directories (`test/`, `tests/`, `spec/`, `__tests__/`)
- Minified files (`.min.js`, `.min.css`)
- Log files and temporary files

## 🚀 How to Use

### For Contributors
1. **Create a PR** as usual
2. **Add the `auto-merge` label** to enable automatic processing
3. **Wait for the bot** to review and process your PR
4. **No manual intervention** needed - the bot handles everything!

### For Maintainers
1. **Monitor the bot** via GitHub Actions tab
2. **Check bot comments** on PRs for status updates
3. **Review configuration** in `.github/omio-bot-config.yml` if needed
4. **Add blocking labels** like `do-not-merge` to prevent auto-merge

## 🏷️ Labels Used

The bot automatically adds these labels:
- `omio-reviewed` - PR has been reviewed by the bot
- `auto-approved` - PR has been auto-approved
- `ready-to-merge` - PR is ready for auto-merge
- `bot-processed` - PR has been processed by the bot

## ⚠️ Blocking Labels

These labels will prevent auto-merge:
- `do-not-merge`
- `needs-review`
- `wip`
- `draft`
- `blocked`
- `security-review`

## 🔧 Customization

To modify bot behavior, edit `.github/omio-bot-config.yml`:

```yaml
# Example: Change merge method
merge_method: 'merge'  # or 'rebase'

# Example: Require more approvals
require_approvals: 2

# Example: Add custom file patterns
include_patterns:
  - "**/*.custom"
```

## 📊 Workflow Triggers

The bot runs on:
- PR opened
- PR synchronized (new commits)
- PR reopened
- PR marked as ready for review
- PR review submitted
- Check suite completed

## 🛠️ Troubleshooting

### Bot Not Running?
1. Check if the workflow file exists: `.github/workflows/omio-pr-reviewer.yml`
2. Verify GitHub Actions are enabled for the repository
3. Check the Actions tab for any failed runs

### PR Not Auto-Merging?
1. Ensure the PR has the `auto-merge` label
2. Check that all required status checks are passing
3. Verify no blocking labels are present
4. Make sure the branch is up to date

### Bot Comments Not Appearing?
1. Check the bot has proper permissions
2. Verify the GitHub token is valid
3. Look for errors in the Actions logs

## 🔒 Security

The bot:
- ✅ Only processes non-draft PRs
- ✅ Respects branch protection rules
- ✅ Requires status checks to pass
- ✅ Validates file size and count limits
- ✅ Checks for security issues
- ✅ Skips sensitive file patterns

## 📈 Benefits

- **Faster PR processing** - No waiting for human review
- **Consistent reviews** - Same criteria applied to all PRs
- **Reduced maintainer workload** - Bot handles routine PRs
- **Better code quality** - Automated checks catch issues early
- **Improved developer experience** - Faster feedback loop

## 🆘 Support

If you encounter issues:
1. Check the [GitHub Actions logs](https://github.com/your-repo/actions)
2. Review the bot configuration in `.github/omio-bot-config.yml`
3. Check the [omio-labs/pr-reviewer-bot documentation](https://github.com/omio-labs/pr-reviewer-bot)

---

**Happy coding! 🎉** The bot is here to make your PR workflow smoother and faster.