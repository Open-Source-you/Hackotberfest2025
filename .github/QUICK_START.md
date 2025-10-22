# 🚀 Quick Start Guide - Omio PR Reviewer Bot

## ✅ Setup Complete!

Your GitHub repository is now configured with the **omio-labs/pr-reviewer-bot@v1** for automatic PR review and merging.

## 🎯 How to Test the Bot

### Method 1: Create a Test PR
1. **Create a new branch**: `git checkout -b test-omio-bot`
2. **Make a small change**: Add a comment to any file
3. **Commit and push**: 
   ```bash
   git add .
   git commit -m "Test: Add comment for Omio bot testing"
   git push origin test-omio-bot
   ```
4. **Create PR** with the `auto-merge` label
5. **Watch the magic happen!** 🎉

### Method 2: Use Existing PR
1. **Go to any existing PR**
2. **Add the `auto-merge` label**
3. **The bot will automatically process it**

## 🏷️ Important Labels

### ✅ Auto-Process Labels
- `auto-merge` - Enables automatic processing
- `bot-approved` - Added by bot when approved
- `omio-reviewed` - Added when reviewed by Omio bot

### ❌ Blocking Labels
- `do-not-merge` - Prevents auto-merge
- `needs-review` - Requires human review
- `wip` - Work in progress
- `draft` - Draft PR

## 🔧 Bot Configuration

The bot is configured in `.github/omio-bot-config.yml`:

```yaml
# Key settings
auto_approve: true      # Auto-approve PRs
auto_merge: true        # Auto-merge PRs
merge_method: 'squash'  # Merge method
require_approvals: 1    # Required approvals
```

## 📊 What Happens When You Create a PR

1. **Bot detects** new PR
2. **Reviews code** automatically
3. **Checks conditions** (labels, status checks, etc.)
4. **Auto-approves** if conditions met
5. **Auto-merges** when ready
6. **Adds labels** and comments

## 🛠️ Troubleshooting

### Bot Not Running?
- Check GitHub Actions tab
- Ensure workflow file exists
- Verify repository permissions

### PR Not Merging?
- Add `auto-merge` label
- Check for blocking labels
- Ensure status checks pass
- Verify branch is up to date

### Need to Disable Bot?
- Add `do-not-merge` label to PR
- Or modify `.github/omio-bot-config.yml`

## 📈 Benefits You'll See

- ⚡ **Faster PR processing** - No waiting for human review
- 🤖 **Consistent reviews** - Same criteria for all PRs
- 📝 **Automatic documentation** - Bot comments explain everything
- 🏷️ **Smart labeling** - Easy to track bot-processed PRs
- 🔒 **Security checks** - Built-in security scanning

## 🎉 You're All Set!

The Omio PR Reviewer Bot is now active and ready to automatically review and merge your pull requests. Just remember to add the `auto-merge` label to any PR you want the bot to process!

---

**Need help?** Check the full documentation in `.github/workflows/OMIO_BOT_README.md`