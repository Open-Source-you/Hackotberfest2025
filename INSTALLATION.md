# Installation Guide for Hacktoberfest 2025

This guide will help new contributors set up the project locally and start contributing without confusion.

---

## Prerequisites

Before starting, ensure you have:

- **Git** installed
- **Node.js** installed
- Basic knowledge of using the command line

---

## Step 1: Clone the Repository

Clone the repository to your local machine:

```sh
$ git clone https://github.com/Open-Source-you/Hackotberfest2025.git
$ cd Hackotberfest2025
```

---

## Step 2: Add Upstream Repository

Add a reference to the original repository to keep your fork synced:

```sh
$ git remote add upstream https://github.com/Open-Source-you/Hackotberfest2025.git
$ git remote -v
```

---

## Step 3: Sync with Upstream

Make sure your local `main` branch is up-to-date with the upstream repository:

```sh
$ git fetch --all --prune
$ git checkout main
$ git reset --hard upstream/main
$ git push origin main
```

---

## Step 4: Create a New Branch

Always create a separate branch for your contributions:

```sh
$ git checkout -b BranchName
```

---

## Step 5: Add Changes and Commit

After making changes, add them and commit with a meaningful message:

```sh
$ git add .
$ git commit -m "Describe your changes"
```

---

## Step 6: Push to Forked Repository

Push your branch to your GitHub fork:

```sh
$ git push -u origin BranchName
```

---

## Step 7: Submit Pull Request

Go to your GitHub fork, click **Compare & Pull Request**, and submit your PR with a descriptive title and explanation of your changes.

---

## Optional: Install Pre-commit Hooks

To automatically format code before committing:

```bash
pip install pre-commit
pre-commit install
```

---

## Troubleshooting Tips

- If `git push` fails, check your remote URLs using `git remote -v`.
- If changes do not appear, ensure you are on the correct branch.
- Always sync with `upstream/main` before starting new work.

---

🎉 You are now ready to contribute to Hacktoberfest 2025!
