# 🚀 Force Merge Guide - Ignore Failing Checks

## ✅ Problem Solved!

Your bot is now configured to **force merge PRs even when checks are failing**!

## 🔧 What Changed

### 1. **Omio Bot Configuration** (`.github/omio-bot-config.yml`)
- ✅ `require_approvals: 0` - No approvals required
- ✅ `require_status_checks: false` - Don't require status checks
- ✅ `require_branch_up_to_date: false` - Don't require up to date
- ✅ `all_checks_passing: false` - Allow merge with failing checks

### 2. **Main Workflow** (`.github/workflows/omio-pr-reviewer.yml`)
- ✅ Force merge mode enabled
- ✅ Ignores PR state checks
- ✅ Merges regardless of failing checks
- ✅ Adds "force-merged" and "ignore-checks" labels

### 3. **New Force Merge Workflow** (`.github/workflows/force-merge-pr.yml`)
- ✅ Manual trigger for any PR
- ✅ Force approves PRs
- ✅ Force merges with admin bypass
- ✅ Adds appropriate labels and comments

## 🚀 How to Use

### Method 1: Automatic (Recommended)
1. **Create a PR** as usual
2. **Add the `auto-merge` label**
3. **The bot will force merge** even with failing checks!

### Method 2: Manual Force Merge
1. **Go to Actions tab** in GitHub
2. **Run "Force Merge PR" workflow**
3. **Enter PR number** when prompted
4. **Bot will force merge** the PR

### Method 3: Script (Advanced)
```bash
# Set GitHub token
export GITHUB_TOKEN=your_token_here

# Force merge PR #123
python3 .github/scripts/force-merge-pr.py owner/repo 123
```

## 🏷️ New Labels

### ✅ Force Merge Labels
- `force-merge` - PR is being force merged
- `ignore-checks` - Failing checks are ignored
- `force-merged` - PR was force merged
- `bot-approved` - Force approved by bot

## 📊 What Happens Now

When you create a PR with the `auto-merge` label:

1. **Bot detects** the PR
2. **Force approves** the PR (ignoring checks)
3. **Force merges** the PR (ignoring checks)
4. **Adds labels** indicating force merge
5. **Comments** explaining the force merge

## ⚠️ Important Notes

- **Failing checks are ignored** - CI, code-quality, etc. won't block merge
- **Only conflicts are checked** - Merge conflicts will still block
- **Blocking labels still work** - `do-not-merge` will still prevent merge
- **Force merge is logged** - All force merges are documented

## 🎯 Example Workflow

```bash
# 1. Create a branch
git checkout -b feature-branch

# 2. Make changes (even if they break tests)
echo "// This might break tests" >> some-file.js
git add .
git commit -m "Add feature (might break tests)"

# 3. Push and create PR
git push origin feature-branch

# 4. Create PR with 'auto-merge' label
# 5. Bot will force merge despite failing tests!
```

## 🔍 Monitoring

Check these places for force merge activity:
- **GitHub Actions** - See force merge workflows
- **PR Comments** - Bot explains what it did
- **PR Labels** - See force merge labels
- **Commit Messages** - "Force merge" in commit title

## 🎉 Success!

Your bot will now merge PRs even when:
- ❌ CI checks fail
- ❌ Code quality checks fail  
- ❌ Security scans fail
- ❌ Test coverage is low
- ❌ Any other checks fail

**Just add the `auto-merge` label and watch the magic happen!** 🚀

---

**Status**: ✅ **ACTIVE** - Force merge mode enabled!  
**Last Updated**: $(date)  
**Bot Version**: omio-labs/pr-reviewer-bot@v1 (Force Merge Mode)