// GitHub API Configuration
const GITHUB_API_BASE = 'https://api.github.com';
const REPO_OWNER = 'Aditya-Prakash14'; // Replace with actual repo owner
const REPO_NAME = 'Hackotberfest2025'; // Replace with actual repo name

// Application State
let contributors = [];
let currentPage = 1;
let isLoading = false;
let currentFilter = 'all';

// DOM Elements
const elements = {
    loadingScreen: document.getElementById('loadingScreen'),
    navbar: document.getElementById('navbar'),
    navToggle: document.getElementById('navToggle'),
    navMenu: document.getElementById('navMenu'),
    exploreBtn: document.getElementById('exploreBtn'),
    addYourselfBtn: document.getElementById('addYourselfBtn'),
    floatingCards: document.getElementById('floatingCards'),
    contributorsGrid: document.getElementById('contributorsGrid'),
    searchInput: document.getElementById('searchInput'),
    loadMoreBtn: document.getElementById('loadMoreBtn'),
    addContributorModal: document.getElementById('addContributorModal'),
    modalClose: document.getElementById('modalClose'),
    cancelBtn: document.getElementById('cancelBtn'),
    contributorForm: document.getElementById('contributorForm'),
    leaderboardContent: document.getElementById('leaderboardContent')
};

// Initialize GSAP
gsap.registerPlugin(ScrollTrigger);

// Application Initialization
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

async function initializeApp() {
    try {
        // Show loading screen
        showLoadingScreen();

        // Initialize animations
        initializeAnimations();

        // Setup event listeners
        setupEventListeners();

        // Generate floating cards
        generateFloatingCards();

        // Fetch initial data
        await fetchContributors();
        await updateStats();

        // Hide loading screen
        hideLoadingScreen();

        // Initialize scroll animations
        initializeScrollAnimations();

    } catch (error) {
        console.error('Error initializing app:', error);
        hideLoadingScreen();
    }
}

// Loading Screen Functions
function showLoadingScreen() {
    elements.loadingScreen.classList.remove('hidden');
}

function hideLoadingScreen() {
    setTimeout(() => {
        elements.loadingScreen.classList.add('hidden');
    }, 1500);
}

// GSAP Animations
function initializeAnimations() {
    // Hero title animation
    const titleLines = document.querySelectorAll('.title-line');
    gsap.set(titleLines, { opacity: 0, y: 50 });

    gsap.to(titleLines, {
        opacity: 1,
        y: 0,
        duration: 0.8,
        stagger: 0.2,
        ease: 'power3.out',
        delay: 2
    });

    // Hero description and buttons animation
    gsap.set('.hero-description, .hero-buttons', { opacity: 0, y: 30 });
    gsap.to('.hero-description, .hero-buttons', {
        opacity: 1,
        y: 0,
        duration: 0.6,
        stagger: 0.2,
        ease: 'power3.out',
        delay: 2.5
    });
}

function initializeScrollAnimations() {
    // Navbar scroll effect
    ScrollTrigger.create({
        trigger: '.hero',
        start: 'bottom top',
        onUpdate: self => {
            if (self.progress > 0.1) {
                elements.navbar.classList.add('scrolled');
            } else {
                elements.navbar.classList.remove('scrolled');
            }
        }
    });

    // Stats animation
    gsap.fromTo('.stat-card', {
        opacity: 0,
        y: 50
    }, {
        opacity: 1,
        y: 0,
        duration: 0.6,
        stagger: 0.2,
        ease: 'power3.out',
        scrollTrigger: {
            trigger: '.stats-grid',
            start: 'top 80%',
            end: 'bottom 20%'
        }
    });

    // Section titles animation
    gsap.fromTo('.section-title', {
        opacity: 0,
        y: 30
    }, {
        opacity: 1,
        y: 0,
        duration: 0.6,
        ease: 'power3.out',
        scrollTrigger: {
            trigger: '.section-title',
            start: 'top 85%',
            end: 'bottom 15%'
        }
    });
}

// Event Listeners
function setupEventListeners() {
    // Navigation
    elements.navToggle.addEventListener('click', toggleMobileMenu);

    // Smooth scrolling for navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', handleNavClick);
    });

    // Hero buttons
    elements.exploreBtn.addEventListener('click', () => {
        document.getElementById('contributors').scrollIntoView({ behavior: 'smooth' });
    });

    elements.addYourselfBtn.addEventListener('click', () => {
        openModal();
    });

    // Search functionality
    elements.searchInput.addEventListener('input', debounce(handleSearch, 300));

    // Filter buttons
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.addEventListener('click', handleFilter);
    });

    // Load more button
    elements.loadMoreBtn.addEventListener('click', loadMoreContributors);

    // Modal controls
    elements.modalClose.addEventListener('click', closeModal);
    elements.cancelBtn.addEventListener('click', closeModal);
    elements.addContributorModal.addEventListener('click', (e) => {
        if (e.target === elements.addContributorModal) closeModal();
    });

    // Form submission
    elements.contributorForm.addEventListener('submit', handleFormSubmit);

    // Leaderboard tabs
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.addEventListener('click', handleTabClick);
    });

    // Window events
    window.addEventListener('scroll', handleScroll);
    window.addEventListener('resize', handleResize);
}

// Navigation Functions
function toggleMobileMenu() {
    elements.navMenu.classList.toggle('active');
    elements.navToggle.classList.toggle('active');
}

function handleNavClick(e) {
    e.preventDefault();
    const targetId = e.target.getAttribute('href');
    const targetElement = document.querySelector(targetId);

    if (targetElement) {
        targetElement.scrollIntoView({ behavior: 'smooth' });

        // Close mobile menu if open
        elements.navMenu.classList.remove('active');
        elements.navToggle.classList.remove('active');

        // Update active nav link
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        e.target.classList.add('active');
    }
}

// Floating Cards Generation
function generateFloatingCards() {
    const icons = ['fab fa-github', 'fas fa-code', 'fas fa-star', 'fas fa-code-branch', 'fas fa-users'];
    const container = elements.floatingCards;

    icons.forEach((icon, index) => {
        const card = document.createElement('div');
        card.className = 'floating-card';
        card.innerHTML = `<i class="${icon}"></i>`;

        // Random positioning
        const x = Math.random() * 80;
        const y = Math.random() * 80;
        card.style.left = `${x}%`;
        card.style.top = `${y}%`;

        container.appendChild(card);

        // GSAP animation
        gsap.set(card, { opacity: 0, scale: 0 });
        gsap.to(card, {
            opacity: 1,
            scale: 1,
            duration: 0.6,
            delay: 3 + (index * 0.2),
            ease: 'back.out(1.7)'
        });
    });
}

// GitHub API Functions
async function fetchContributors(page = 1) {
    try {
        isLoading = true;
        updateLoadMoreButton();

        const response = await fetch(`${GITHUB_API_BASE}/repos/${REPO_OWNER}/${REPO_NAME}/contributors?page=${page}&per_page=12`);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        // Fetch additional user data for each contributor
        const enrichedContributors = await Promise.all(
            data.map(async (contributor) => {
                try {
                    const userResponse = await fetch(contributor.url);
                    const userData = userResponse.ok ? await userResponse.json() : {};

                    return {
                        ...contributor,
                        name: userData.name || contributor.login,
                        bio: userData.bio || 'No bio available',
                        location: userData.location || 'Unknown',
                        public_repos: userData.public_repos || 0,
                        followers: userData.followers || 0,
                        created_at: userData.created_at || new Date().toISOString()
                    };
                } catch (error) {
                    console.warn('Error fetching user data for', contributor.login, error);
                    return {
                        ...contributor,
                        name: contributor.login,
                        bio: 'No bio available',
                        location: 'Unknown',
                        public_repos: 0,
                        followers: 0,
                        created_at: new Date().toISOString()
                    };
                }
            })
        );

        if (page === 1) {
            contributors = enrichedContributors;
        } else {
            contributors.push(...enrichedContributors);
        }

        renderContributors();
        currentPage = page;

    } catch (error) {
        console.error('Error fetching contributors:', error);
        showError('Failed to load contributors. Please try again later.');
    } finally {
        isLoading = false;
        updateLoadMoreButton();
    }
}

async function updateStats() {
    try {
        // Fetch repository stats
        const repoResponse = await fetch(`${GITHUB_API_BASE}/repos/${REPO_OWNER}/${REPO_NAME}`);
        const repoData = await repoResponse.json();

        // Fetch pull requests
        const prsResponse = await fetch(`${GITHUB_API_BASE}/repos/${REPO_OWNER}/${REPO_NAME}/pulls?state=all&per_page=100`);
        const prsData = await prsResponse.json();

        // Calculate stats
        const stats = {
            contributors: contributors.length,
            pullRequests: Array.isArray(prsData) ? prsData.length : 0,
            stars: repoData.stargazers_count || 0,
            countries: new Set(contributors.map(c => c.location).filter(l => l !== 'Unknown')).size
        };

        // Animate counter updates
        animateStats(stats);

    } catch (error) {
        console.error('Error updating stats:', error);
    }
}

function animateStats(stats) {
    const statElements = document.querySelectorAll('.stat-number');

    statElements.forEach((element, index) => {
        const targetValue = Object.values(stats)[index];
        const currentValue = parseInt(element.textContent) || 0;

        gsap.to({ value: currentValue }, {
            value: targetValue,
            duration: 2,
            ease: 'power2.out',
            onUpdate: function() {
                element.textContent = Math.round(this.targets()[0].value);
            }
        });
    });
}

// Rendering Functions
function renderContributors(contributorsToRender = contributors) {
    const grid = elements.contributorsGrid;

    if (currentPage === 1 || currentFilter !== 'all') {
        grid.innerHTML = '';
    }

    contributorsToRender.forEach((contributor, index) => {
        const card = createContributorCard(contributor);
        grid.appendChild(card);

        // Animate card entry
        gsap.set(card, { opacity: 0, y: 30 });
        gsap.to(card, {
            opacity: 1,
            y: 0,
            duration: 0.6,
            delay: index * 0.1,
            ease: 'power3.out'
        });
    });
}

function createContributorCard(contributor) {
    const card = document.createElement('div');
    card.className = 'contributor-card';

    card.innerHTML = `
        <div class="contributor-header">
            <img src="${contributor.avatar_url}" alt="${contributor.name}" class="contributor-avatar">
            <div class="contributor-info">
                <h3>${contributor.name}</h3>
                <div class="contributor-username">@${contributor.login}</div>
            </div>
        </div>
        <div class="contributor-stats">
            <div class="stat">
                <div class="stat-value">${contributor.contributions}</div>
                <div class="stat-label">Commits</div>
            </div>
            <div class="stat">
                <div class="stat-value">${contributor.public_repos}</div>
                <div class="stat-label">Repos</div>
            </div>
            <div class="stat">
                <div class="stat-value">${contributor.followers}</div>
                <div class="stat-label">Followers</div>
            </div>
        </div>
        <div class="contributor-bio">${contributor.bio}</div>
        <div class="contributor-links">
            <a href="${contributor.html_url}" target="_blank" class="link-btn">
                <i class="fab fa-github"></i> Profile
            </a>
            ${contributor.location !== 'Unknown' ? `<span class="link-btn"><i class="fas fa-map-marker-alt"></i> ${contributor.location}</span>` : ''}
        </div>
    `;

    return card;
}

// Search and Filter Functions
function handleSearch(e) {
    const query = e.target.value.toLowerCase().trim();

    if (query === '') {
        renderContributors();
        return;
    }

    const filteredContributors = contributors.filter(contributor =>
        contributor.name.toLowerCase().includes(query) ||
        contributor.login.toLowerCase().includes(query) ||
        contributor.bio.toLowerCase().includes(query)
    );

    renderContributors(filteredContributors);
}

function handleFilter(e) {
    const filter = e.target.getAttribute('data-filter');
    currentFilter = filter;

    // Update active filter button
    document.querySelectorAll('.filter-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    e.target.classList.add('active');

    let filteredContributors = [...contributors];

    switch (filter) {
        case 'top':
            filteredContributors = contributors
                .sort((a, b) => b.contributions - a.contributions)
                .slice(0, 12);
            break;
        case 'recent':
            filteredContributors = contributors
                .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
                .slice(0, 12);
            break;
        default:
            filteredContributors = contributors;
    }

    renderContributors(filteredContributors);
}

// Load More Functionality
async function loadMoreContributors() {
    if (!isLoading) {
        await fetchContributors(currentPage + 1);
    }
}

function updateLoadMoreButton() {
    if (isLoading) {
        elements.loadMoreBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
        elements.loadMoreBtn.disabled = true;
    } else {
        elements.loadMoreBtn.innerHTML = '<i class="fas fa-plus"></i> Load More Contributors';
        elements.loadMoreBtn.disabled = false;
    }
}

// Modal Functions
function openModal() {
    elements.addContributorModal.classList.add('active');
    document.body.style.overflow = 'hidden';

    // Focus first input
    setTimeout(() => {
        document.getElementById('githubUsername').focus();
    }, 300);
}

function closeModal() {
    elements.addContributorModal.classList.remove('active');
    document.body.style.overflow = '';
    elements.contributorForm.reset();
}

async function handleFormSubmit(e) {
    e.preventDefault();

    const formData = new FormData(e.target);
    const username = formData.get('githubUsername') || document.getElementById('githubUsername').value;
    const name = formData.get('contributorName') || document.getElementById('contributorName').value;
    const bio = formData.get('contributorBio') || document.getElementById('contributorBio').value;

    if (!username || !name) {
        showError('Please fill in all required fields.');
        return;
    }

    try {
        // Simulate adding contributor (in real app, this would be a POST request)
        const newContributor = {
            login: username,
            name: name,
            bio: bio || 'No bio available',
            avatar_url: `https://github.com/${username}.png`,
            html_url: `https://github.com/${username}`,
            contributions: 1,
            public_repos: 0,
            followers: 0,
            location: 'Unknown',
            created_at: new Date().toISOString()
        };

        contributors.unshift(newContributor);
        renderContributors();
        closeModal();
        showSuccess('Contributor added successfully!');

    } catch (error) {
        console.error('Error adding contributor:', error);
        showError('Failed to add contributor. Please try again.');
    }
}

// Leaderboard Functions
function handleTabClick(e) {
    const tab = e.target.getAttribute('data-tab');

    // Update active tab
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    e.target.classList.add('active');

    renderLeaderboard(tab);
}

function renderLeaderboard(type = 'commits') {
    const container = elements.leaderboardContent;
    let sortedContributors = [...contributors];

    switch (type) {
        case 'commits':
            sortedContributors.sort((a, b) => b.contributions - a.contributions);
            break;
        case 'prs':
            sortedContributors.sort((a, b) => b.contributions - a.contributions); // Assuming contributions = PRs
            break;
        case 'stars':
            sortedContributors.sort((a, b) => b.public_repos - a.public_repos);
            break;
    }

    const top10 = sortedContributors.slice(0, 10);

    container.innerHTML = top10.map((contributor, index) => {
        const rank = index + 1;
        let rankClass = '';
        if (rank === 1) rankClass = 'gold';
        else if (rank === 2) rankClass = 'silver';
        else if (rank === 3) rankClass = 'bronze';

        let scoreValue = contributor.contributions;
        if (type === 'stars') scoreValue = contributor.public_repos;

        return `
            <div class="leaderboard-item">
                <div class="rank ${rankClass}">${rank}</div>
                <img src="${contributor.avatar_url}" alt="${contributor.name}" class="leader-avatar">
                <div class="leader-info">
                    <h4>${contributor.name}</h4>
                    <div class="leader-username">@${contributor.login}</div>
                </div>
                <div class="leader-score">${scoreValue}</div>
            </div>
        `;
    }).join('');

    // Animate leaderboard items
    const items = container.querySelectorAll('.leaderboard-item');
    gsap.set(items, { opacity: 0, x: -30 });
    gsap.to(items, {
        opacity: 1,
        x: 0,
        duration: 0.6,
        stagger: 0.1,
        ease: 'power3.out'
    });
}

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function showError(message) {
    // Create and show error notification
    const notification = createNotification(message, 'error');
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 5000);
}

function showSuccess(message) {
    // Create and show success notification
    const notification = createNotification(message, 'success');
    document.body.appendChild(notification);
    setTimeout(() => notification.remove(), 5000);
}

function createNotification(message, type) {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'error' ? '#ff4757' : '#2ed573'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        z-index: 10001;
        font-weight: 500;
        transform: translateX(400px);
        transition: transform 0.3s ease;
    `;
    notification.textContent = message;

    // Animate in
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);

    return notification;
}

function handleScroll() {
    // Update active navigation link based on scroll position
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-link');

    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop - 100;
        const sectionHeight = section.clientHeight;
        if (window.scrollY >= sectionTop && window.scrollY < sectionTop + sectionHeight) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
}

function handleResize() {
    // Close mobile menu on resize to desktop
    if (window.innerWidth > 768) {
        elements.navMenu.classList.remove('active');
        elements.navToggle.classList.remove('active');
    }
}

// Initialize leaderboard on load
setTimeout(() => {
    renderLeaderboard('commits');
}, 3000);
