# GitHub Pages Workflow Options

This directory contains optimized GitHub Pages workflows to reduce frequent builds.

## Available Workflows:

### 1. `pages.yml` (Recommended)
- **Triggers**: Only when HTML, CSS, JS, MD, or image files change
- **Excludes**: Python, Java, C++, notebooks, logs, temp files
- **Best for**: Active development with frequent content changes

### 2. `pages-conservative.yml` (Ultra Conservative)
- **Triggers**: Only when web content files change + scheduled every 6 hours
- **Excludes**: All non-web files (Python, Java, C++, data files, etc.)
- **Best for**: Reducing builds to minimum while maintaining functionality

## How to Use:

1. **Choose one workflow** (don't use both)
2. **Rename the chosen file** to `pages.yml` if you want it to be the default
3. **Delete the other file** to avoid conflicts
4. **Commit and push** to activate the new workflow

## Current Issue:
- Repository has 208 commits in the last week
- GitHub Pages was rebuilding on every push
- New workflows will only rebuild when relevant files change

## Expected Results:
- 80-90% reduction in workflow runs
- Faster development workflow
- Same functionality with better performance
