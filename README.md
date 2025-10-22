#  Hacktoberfest 2025 Is Awesome🔥
<img width="1814" height="891" alt="image" src="https://github.com/user-attachments/assets/fb5725be-afeb-4a97-96f1-e3d05a73fc7b" />


<div align="center">

[![Open Source Love](https://firstcontributions.github.io/open-source-badges/badges/open-source-v1/open-source.svg)](https://github.com/Open-Source-you/Hackotberfest2022)
<img src="https://img.shields.io/badge/HacktoberFest-2025-blueviolet" alt="Hacktober Badge"/>
<img src="https://img.shields.io/static/v1?label=%E2%AD%90&message=If%20Useful&style=style=flat&color=BC4E99" alt="Star Badge"/>
<a href="https://github.com/Open-Source-you" ><img src="https://img.shields.io/badge/Contributions-welcome-green.svg?style=flat&logo=github" alt="Contributions" /></a>

</div>


### This repository aims to help code beginners with their first successful pull request and open source contribution. :partying_face:

:star: Feel free to use this project to make your first contribution to an open-source project on GitHub. Practice making your first pull request to a public repository before doing the real thing!

:star: Make sure to grab some cool swags during Hacktoberfest by getting involved in the open-source community.

### This repository is open to all members of the GitHub community. Any member can contribute to this project! :grin:

## What is Hacktoberfest? :thinking:
A month-long celebration from October 1st to October 31st, presented by [DigitalOcean](https://www.digitalocean.com/) and [DEV Community](https://dev.to/), in collaboration with [GitHub](https://github.com/blog/2433-celebrate-open-source-this-october-with-hacktoberfest), to get people involved in [Open Source](https://github.com/open-source). Create your very first pull request to any public repository on GitHub and contribute to the open-source developer community.

[https://hacktoberfest.digitalocean.com/](https://hacktoberfest.digitalocean.com/)

## Rules :fire:
To qualify for the __official limited edition Hacktoberfest shirt__, you must register [here](https://hacktoberfest.digitalocean.com/) and make four Pull Requests (PRs) between October 1-31, 2025 (in any time zone). PRs can be made to any public repository on GitHub, not only the ones with issues labeled Hacktoberfest. This year, the __first 10,000__ participants who complete the challenge will earn a T-shirt.

## Steps to follow :scroll:

### Tip : Complete this process in GitHub (in your browser)

```mermaid
flowchart LR
    Fork[Fork the project]-->branch[Create a New Branch]
    branch-->Edit[Edit file]
    Edit-->commit[Commit the changes]
    commit -->|Finally|creatpr((Create a Pull Request))

 ```

### 1. Star The Repository :star2:

Star the repository by pressing the topmost-right button to start your wonderful journey.

### 2. Fork it :fork_and_knife:

You can get your own fork/copy of [Hacktoberfest2025](https://github.com/Open-Source-you/Hackotberfest2025/fork) by using the <a href="https://github.com/Open-Source-you/Hackotberfest2025/fork"><kbd><b>Fork</b></kbd></a> button.


### 3. Clone it :busts_in_silhouette:

`NOTE: commands are to be executed on Linux, Mac, and Windows(using Powershell)`

You need to clone or (download) it to local machine using

```sh
$ git clone https://github.com/Open-Source-you/Hackotberfest2025.git
```

> This makes a local copy of the repository in your machine.
Once you have cloned the `Hacktoberfest-2025` repository in Github, move to that folder first using change directory command on Linux, Mac, and Windows(PowerShell to be used).

```sh
# This will change directory to a folder Hacktoberfest-2025
$ cd Hackotberfest2025
```

Move to this folder for all other commands.

### 4. Set it up :arrow_up:

Run the following commands to see that *your local copy* has a reference to *your forked remote repository* in Github :octocat:

```sh
$ git remote -v
origin  https://github.com/Your_Username/Hacktoberfest-2025.git (fetch)
origin  https://github.com/Your_Username/Hacktoberfest-2025.git (push)
```

Now, let's add a reference to the original [Hacktoberfest-2025](https://github.com/Open-Source-you/Hackotberfest2022) repository using

```sh
$ git remote add upstream https://github.com/Open-Source-you/Hackotberfest2025.git
```

> This adds a new remote named ***upstream***.
See the changes using

```sh
$ git remote -v
origin    https://github.com/Your_Username/Hacktoberfest-2025.git (fetch)
origin    https://github.com/Your_Username/Hacktoberfest-2025.git (push)
upstream  https://github.com/Remote_Username/Hacktoberfest-2025.git (fetch)
upstream  https://github.com/Remote_Username/Hacktoberfest-2025.git (push)
```
`In your case, you will see`
```sh
$ git remote -V
origin    https://github.com/Your_Username/Hacktoberfest-2025.git (fetch)
origin    https://github.com/Your_Username/Hacktoberfest-2025.git (push)
upstream  https://github.com/kishanrajput23/Hacktoberfest-2025.git (fetch)
upstream  https://github.com/kishanrajput23/Hacktoberfest-2025.git (push)
```

### 5. Sync it :recycle:

Always keep your local copy of the repository updated with the original repository.
Before making any changes and/or in an appropriate interval, run the following commands *carefully* to update your local repository.

```sh
# Fetch all remote repositories and delete any deleted remote branches
$ git fetch --all --prune
# Switch to `main` branch
$ git checkout main
# Reset local `main` branch to match the `upstream` repository's `main` branch
$ git reset --hard upstream/main
# Push changes to your forked `Hacktoberfest-2025` repo
$ git push origin main
```

### 6. Ready Steady Go... :turtle: :rabbit2:

Once you have completed these steps, you are ready to start contributing by checking our `Good First Issue` Issues and creating [pull requests](#).

### 7. Create a new branch :bangbang:

Whenever you are going to contribute. Please create a separate branch using command and keep your `main` branch clean (i.e. synced with remote branch).

```sh
# It will create a new branch with name Branch_Name and switch to branch Folder_Name
$ git checkout -b BranchName
```

Create a separate branch for contribution and try to use the same name of the branch as of folder.

To switch to the desired branch

```sh
# To switch from one folder to other
$ git checkout BranchName
```

To add the changes to the branch. Use

```sh
# To add all files to branch Folder_Name
$ git add .
```

Type in a message relevant for the code reviewer using

```sh
# This message get associated with all files you have changed
$ git commit -m 'relevant message'
```

Now, Push your awesome work to your remote repository using

```sh
# To push your work to your remote repository
$ git push -u origin BranchName
```

Finally, go to your repository in the browser and click on `compare and pull requests`.
Then add a title and description to your pull request that explains your precious effort.




## Help Contributing Guides :crown:

We love to have `articles` and `codes` in different languages and the `betterment` of existing ones.

Please discuss it with us first by creating a new issue.

:tada: :confetti_ball: :smiley: _**Happy Contributing**_ :smiley: :confetti_ball: :tada:

## 🤝 Contributing - Code Quality (Optional)

### For New Contributors

Our CI runs code quality checks but **won't block your PR**. These are informational only:
- ✅ Your PR will be reviewed based on functionality
- ℹ️ Code quality suggestions are helpful but not required
- 🎯 We're gradually improving code quality over time

### Optional: Install Pre-commit Hooks (Recommended)

If you want to automatically format your code:
```bash
# Install pre-commit
pip install pre-commit

# Install the hooks (one-time setup)
pre-commit install

# Now hooks run automatically on commit
git commit -m "your message"


```markdown
---

## 🌟 Contributor Recognition

We love to highlight our amazing contributors!  
Every contribution — whether it’s fixing a typo, improving documentation, or adding a new feature — helps this project grow.

Want to be featured here?  
Contribute by solving an issue, improving the docs, or enhancing the user experience.

| Contributor | Contribution |
|--------------|--------------|
| [@supriya-cybertech](https://github.com/supriya-cybertech) | Documentation improvements: Enhanced community and contribution guidelines |

Thank you for making open source awesome! 🙌
