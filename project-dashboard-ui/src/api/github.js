// project-dashboard-ui/src/api/github.js

// Replace with the actual repository owner and name if they are different from the repo you are forking
const REPO_OWNER = 'Open-Source-you';
const REPO_NAME = 'Hackotberfest2025';
const BASE_URL = `https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}`;
const GITHUB_TOKEN = import.meta.env.VITE_GITHUB_TOKEN; // Use environment variable for auth

const headers = GITHUB_TOKEN ? { Authorization: `token ${GITHUB_TOKEN}` } : {};

const fetchData = async (path, params = {}) => {
    const query = new URLSearchParams(params).toString();
    const url = `${BASE_URL}${path}${query ? `?${query}` : ''}`;
    const response = await fetch(url, { headers });
    
    if (!response.ok) {
        throw new Error(`GitHub API failed: ${response.status} ${response.statusText}`);
    }
    return response.json();
};

export const fetchContributors = () => {
    // Gets top 10 contributors sorted by commits
    return fetchData('/stats/contributors')
        .then(data => data.sort((a, b) => b.total - a.total).slice(0, 10));
};

export const fetchStatusCounts = async () => {
    // Fetch all open issues and PRs (GitHub API treats PRs as issues)
    const allOpen = await fetchData('/issues', { state: 'open', per_page: 100 });

    const open_issues = allOpen.filter(issue => !issue.pull_request).length;
    const open_prs = allOpen.filter(issue => issue.pull_request).length;
    const total_open = allOpen.length;

    return { open_prs, open_issues, total_open };
};