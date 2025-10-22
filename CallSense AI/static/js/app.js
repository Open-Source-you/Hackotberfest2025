class CallAnalyzerApp {
    constructor() {
        this.currentSection = 'analyzer';
        this.analysisHistory = JSON.parse(localStorage.getItem('analysisHistory')) || [];
        this.sentimentChart = null;
        this.isAnalyzing = false;
        this.darkMode = localStorage.getItem('darkMode') === 'true';
        
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.updateStats();
        this.renderHistory();
        this.initChart();
        this.setupKeyboardShortcuts();
        this.initTheme();
        this.initProgressBar();
        this.initFloatingActionButton();
        this.initAdvancedAnimations();
    }

    initTheme() {
        const themeToggle = document.getElementById('themeToggle');
        const themeIcon = document.getElementById('themeIcon');
        const body = document.body;

        if (this.darkMode) {
            body.classList.add('dark-mode');
            themeIcon.className = 'fas fa-sun';
        } else {
            body.classList.remove('dark-mode');
            themeIcon.className = 'fas fa-moon';
        }

        themeToggle.addEventListener('click', () => {
            this.darkMode = !this.darkMode;
            localStorage.setItem('darkMode', this.darkMode);
            
            body.classList.toggle('dark-mode', this.darkMode);
            themeIcon.className = this.darkMode ? 'fas fa-sun' : 'fas fa-moon';
            
            themeToggle.style.transform = 'rotate(360deg)';
            setTimeout(() => {
                themeToggle.style.transform = 'rotate(0deg)';
            }, 300);

            this.showToast(
                `${this.darkMode ? 'Dark' : 'Light'} mode activated`,
                'info'
            );
        });
    }

    initProgressBar() {
        this.progressBar = document.getElementById('progressBar');
        
        window.addEventListener('load', () => {
            this.updateProgress(100);
            setTimeout(() => {
                this.progressBar.style.opacity = '0';
            }, 500);
        });
    }

    updateProgress(percentage) {
        this.progressBar.style.width = `${percentage}%`;
        this.progressBar.style.opacity = '1';
    }

    initFloatingActionButton() {
        const fab = document.getElementById('fab');
        let fabTimeout;

        window.addEventListener('scroll', () => {
            clearTimeout(fabTimeout);
            fab.style.opacity = '1';
            fab.style.transform = 'translateY(0)';
            
            fabTimeout = setTimeout(() => {
                if (window.scrollY > 100) {
                    fab.style.opacity = '0.7';
                    fab.style.transform = 'translateY(10px)';
                }
            }, 2000);
        });

        fab.addEventListener('click', () => {
            fab.style.transform = 'scale(0.9)';
            setTimeout(() => {
                fab.style.transform = 'scale(1)';
            }, 150);

            this.showToast('Quick analyze shortcut: Ctrl+Enter', 'info');
        });
    }

    initAdvancedAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);

        document.querySelectorAll('.animate-left, .animate-right, .animate-up').forEach(el => {
            observer.observe(el);
        });

        document.querySelectorAll('.card, .dashboard-card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-5px) scale(1.02)';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'translateY(0) scale(1)';
            });
        });

        document.querySelectorAll('.btn-primary, .btn-secondary').forEach(button => {
            button.addEventListener('click', (e) => {
                this.createRippleEffect(e, button);
            });
        });
    }

    createRippleEffect(event, element) {
        const ripple = document.createElement('span');
        const rect = element.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.6);
            transform: scale(0);
            animation: ripple 0.6s linear;
            left: ${x}px;
            top: ${y}px;
            width: ${size}px;
            height: ${size}px;
            pointer-events: none;
        `;
        
        element.style.position = 'relative';
        element.style.overflow = 'hidden';
        element.appendChild(ripple);
        
        setTimeout(() => {
            ripple.remove();
        }, 600);
    }

    setupEventListeners() {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                const section = link.getAttribute('href').substring(1);
                this.showSection(section);
            });
        });

        document.querySelectorAll('.btn-option').forEach(btn => {
            btn.addEventListener('click', () => {
                this.switchInputMode(btn.dataset.input);
            });
        });

        const transcript = document.getElementById('transcript');
        transcript.addEventListener('input', () => {
            this.updateCharCount();
            this.validateInput();
        });

        const fileInput = document.getElementById('fileInput');
        const fileDropZone = document.getElementById('fileDropZone');
        const fileBrowse = document.querySelector('.file-browse');

        fileBrowse.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', (e) => this.handleFileSelect(e));

        fileDropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileDropZone.classList.add('drag-over');
        });

        fileDropZone.addEventListener('dragleave', () => {
            fileDropZone.classList.remove('drag-over');
        });

        fileDropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            fileDropZone.classList.remove('drag-over');
            this.handleFileSelect(e);
        });

        document.getElementById('analyzeBtn').addEventListener('click', () => this.analyzeTranscript());
        document.getElementById('sampleBtn').addEventListener('click', () => this.loadSample());
        document.getElementById('clearText').addEventListener('click', () => this.clearText());
        document.getElementById('exportBtn').addEventListener('click', () => this.exportResults());
        document.getElementById('shareBtn').addEventListener('click', () => this.shareResults());
        document.getElementById('copySummary').addEventListener('click', () => this.copySummary());

        document.getElementById('sentimentFilter').addEventListener('change', () => this.filterHistory());
        document.getElementById('searchHistory').addEventListener('input', () => this.filterHistory());

        document.getElementById('modalClose').addEventListener('click', () => this.closeModal());
        document.getElementById('detailModal').addEventListener('click', (e) => {
            if (e.target.id === 'detailModal') this.closeModal();
        });
    }

    async analyzeTranscript() {
        if (this.isAnalyzing) return;

        const transcript = document.getElementById('transcript').value.trim();
        if (!transcript) {
            this.showToast('Please enter a transcript to analyze', 'error');
            return;
        }

        this.isAnalyzing = true;
        this.showLoadingState();
        this.updateProgress(10);

        try {
            const progressSteps = [20, 40, 60, 80, 95];
            let stepIndex = 0;
            
            const progressInterval = setInterval(() => {
                if (stepIndex < progressSteps.length) {
                    this.updateProgress(progressSteps[stepIndex]);
                    stepIndex++;
                } else {
                    clearInterval(progressInterval);
                }
            }, 200);

            const response = await fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ transcript })
            });

            clearInterval(progressInterval);
            this.updateProgress(100);

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const result = await response.json();
            
            setTimeout(() => {
                this.updateProgress(0);
                this.progressBar.style.opacity = '0';
            }, 500);

            this.displayResults(result);
            this.saveToHistory(transcript, result);
            this.showToast('Analysis completed successfully!', 'success');

        } catch (error) {
            console.error('Analysis error:', error);
            this.showToast('Analysis failed. Please try again.', 'error');
            this.hideLoadingState();
            this.updateProgress(0);
            this.progressBar.style.opacity = '0';
        } finally {
            this.isAnalyzing = false;
        }
    }

    showLoadingState() {
        document.getElementById('emptyState').style.display = 'none';
        document.getElementById('resultsContent').style.display = 'none';
        document.getElementById('loadingState').style.display = 'block';
        
        const messages = [
            'Processing with AI...',
            'Analyzing sentiment...',
            'Generating insights...',
            'Preparing results...'
        ];
        
        let messageIndex = 0;
        const loadingMessage = document.getElementById('loadingMessage');
        
        this.loadingInterval = setInterval(() => {
            messageIndex = (messageIndex + 1) % messages.length;
            loadingMessage.textContent = messages[messageIndex];
        }, 1000);
    }

    hideLoadingState() {
        if (this.loadingInterval) {
            clearInterval(this.loadingInterval);
        }
        document.getElementById('loadingState').style.display = 'none';
        document.getElementById('emptyState').style.display = 'block';
    }

    showToast(message, type = 'info', duration = 3000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const icon = {
            success: 'fas fa-check-circle',
            error: 'fas fa-exclamation-circle',
            warning: 'fas fa-exclamation-triangle',
            info: 'fas fa-info-circle'
        }[type];

        toast.innerHTML = `
            <i class="${icon}"></i>
            <span>${message}</span>
            <button class="toast-close"><i class="fas fa-times"></i></button>
        `;

        const container = document.getElementById('toastContainer');
        container.appendChild(toast);

        setTimeout(() => toast.classList.add('show'), 10);

        const timeoutId = setTimeout(() => {
            this.removeToast(toast);
        }, duration);

        toast.querySelector('.toast-close').addEventListener('click', () => {
            clearTimeout(timeoutId);
            this.removeToast(toast);
        });

        if ('vibrate' in navigator) {
            navigator.vibrate(type === 'error' ? [100, 50, 100] : 50);
        }
    }

    removeToast(toast) {
        toast.classList.add('removing');
        setTimeout(() => {
            if (toast.parentNode) {
                toast.parentNode.removeChild(toast);
            }
        }, 300);
    }

    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                e.preventDefault();
                this.analyzeTranscript();
            }
            
            if (e.ctrlKey && e.key === 'l') {
                e.preventDefault();
                this.loadSample();
            }
            
            if (e.ctrlKey && e.key === 'd') {
                e.preventDefault();
                document.getElementById('themeToggle').click();
            }
            
            if (e.key === 'Escape') {
                this.closeModal();
            }
            
            if (e.key === 'Tab' && e.altKey) {
                e.preventDefault();
                const sections = ['analyzer', 'dashboard', 'history'];
                const currentIndex = sections.indexOf(this.currentSection);
                const nextIndex = (currentIndex + 1) % sections.length;
                this.showSection(sections[nextIndex]);
            }
        });
    }

    showSection(sectionId) {
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[href="#${sectionId}"]`).classList.add('active');

        document.querySelectorAll('.section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(sectionId).classList.add('active');

        this.currentSection = sectionId;

        if (sectionId === 'dashboard') {
            this.updateDashboard();
        } else if (sectionId === 'history') {
            this.renderHistory();
        }
    }

    switchInputMode(type) {
        document.querySelectorAll('.btn-option').forEach(btn => {
            btn.classList.remove('active');
        });
        document.querySelector(`[data-input="${type}"]`).classList.add('active');

        document.querySelectorAll('.text-input, .file-input').forEach(container => {
            container.classList.remove('active');
        });
        document.querySelector(`.${type}-input`).classList.add('active');
    }

    updateCharCount() {
        const transcript = document.getElementById('transcript');
        const charCount = document.querySelector('.char-count');
        const count = transcript.value.length;
        charCount.textContent = `${count.toLocaleString()} characters`;
        
        if (count > 10000) {
            charCount.style.color = 'var(--error)';
        } else if (count > 5000) {
            charCount.style.color = 'var(--warning)';
        } else {
            charCount.style.color = 'var(--gray-500)';
        }
    }

    validateInput() {
        const transcript = document.getElementById('transcript').value.trim();
        const analyzeBtn = document.getElementById('analyzeBtn');
        
        if (transcript.length > 0) {
            analyzeBtn.disabled = false;
            analyzeBtn.classList.remove('disabled');
        } else {
            analyzeBtn.disabled = true;
            analyzeBtn.classList.add('disabled');
        }
    }

    handleFileSelect(event) {
        const files = event.target?.files || event.dataTransfer?.files;
        if (!files || files.length === 0) return;

        const file = files[0];
        
        if (!file.type.match('text.*') && !file.name.endsWith('.txt') && !file.name.endsWith('.csv')) {
            this.showToast('Please upload a text file (.txt, .csv)', 'error');
            return;
        }

        if (file.size > 1024 * 1024) {
            this.showToast('File size must be less than 1MB', 'error');
            return;
        }

        const reader = new FileReader();
        reader.onload = (e) => {
            document.getElementById('transcript').value = e.target.result;
            this.updateCharCount();
            this.validateInput();
            this.switchInputMode('text');
            this.showToast(`File "${file.name}" uploaded successfully`, 'success');
        };
        reader.onerror = () => {
            this.showToast('Error reading file', 'error');
        };
        reader.readAsText(file);
    }

    loadSample() {
        const samples = [
            "Customer: Hi, I'm calling about my recent order #12345. I placed it three days ago but haven't received any shipping confirmation yet.\n\nAgent: I apologize for the confusion. Let me look that up for you right away. I can see your order here, and it looks like there was a delay in our warehouse. Your order has actually been shipped this morning and you should receive a tracking number within the next hour.\n\nCustomer: Oh, that's great news! Thank you so much for checking on that. I was getting worried.\n\nAgent: No problem at all! Is there anything else I can help you with today?\n\nCustomer: No, that's everything. Thanks again for your help!",
            
            "Customer: I'm extremely frustrated! I've been trying to cancel my subscription for weeks and your website keeps giving me errors. This is completely unacceptable!\n\nAgent: I sincerely apologize for the technical difficulties you've experienced. That must be very frustrating. Let me help you cancel that subscription right now.\n\nCustomer: Finally! I've wasted so much time on this.\n\nAgent: I understand your frustration completely. I've successfully canceled your subscription and you'll receive a confirmation email shortly. I've also noted this technical issue for our IT team to investigate.\n\nCustomer: Well, at least it's finally done. Thank you for actually helping me.",
            
            "Customer: Hello! I just wanted to call and say how amazing your customer service has been. Sarah helped me last week with setting up my new account and she was absolutely wonderful.\n\nAgent: That's so wonderful to hear! I'll make sure to pass along your kind words to Sarah. She'll be thrilled to know how much her help meant to you.\n\nCustomer: Please do! It's rare to find such helpful and patient service these days. You guys are doing something right!\n\nAgent: Thank you so much for taking the time to share this feedback. It really makes our day. Is there anything else I can help you with?\n\nCustomer: No, I just wanted to share the positive feedback. Keep up the great work!"
        ];

        const randomSample = samples[Math.floor(Math.random() * samples.length)];
        document.getElementById('transcript').value = randomSample;
        this.updateCharCount();
        this.validateInput();
        this.switchInputMode('text');
        this.showToast('Sample transcript loaded', 'success');
    }

    clearText() {
        document.getElementById('transcript').value = '';
        this.updateCharCount();
        this.validateInput();
        this.showToast('Text cleared', 'info');
    }

    displayResults(result) {
        const loadingState = document.getElementById('loadingState');
        const resultsContent = document.getElementById('resultsContent');
        const resultsActions = document.querySelector('.results-actions');

        loadingState.style.display = 'none';
        resultsContent.style.display = 'block';
        resultsActions.style.display = 'flex';

        this.updateSentimentDisplay(result.sentiment);

        document.getElementById('summaryContent').textContent = result.summary;

        this.updateInsights(result);

        resultsContent.style.opacity = '0';
        resultsContent.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            resultsContent.style.transition = 'all 0.5s ease-out';
            resultsContent.style.opacity = '1';
            resultsContent.style.transform = 'translateY(0)';
        }, 100);
    }

    updateSentimentDisplay(sentiment) {
        const badge = document.getElementById('sentimentBadge');
        const meter = document.getElementById('sentimentMeter');

        badge.textContent = sentiment;
        badge.className = `sentiment-badge ${sentiment}`;

        let width;
        switch (sentiment) {
            case 'negative':
                width = '25%';
                break;
            case 'neutral':
                width = '50%';
                break;
            case 'positive':
                width = '75%';
                break;
            default:
                width = '50%';
        }

        meter.style.width = width;
        meter.className = `meter-fill ${sentiment}`;
    }

    updateInsights(result) {
        const insightsGrid = document.getElementById('insightsGrid');
        const transcript = document.getElementById('transcript').value;
        const wordCount = transcript.split(/\s+/).filter(word => word.length > 0).length;
        const sentences = transcript.split(/[.!?]+/).filter(s => s.trim().length > 0);
        const avgWordsPerSentence = sentences.length > 0 ? Math.round(wordCount / sentences.length) : 0;
        
        const insights = [
            {
                icon: 'fas fa-file-word',
                value: wordCount.toLocaleString(),
                label: 'Words',
                color: 'var(--info)'
            },
            {
                icon: 'fas fa-paragraph',
                value: sentences.length,
                label: 'Sentences',
                color: 'var(--success)'
            },
            {
                icon: 'fas fa-chart-line',
                value: avgWordsPerSentence,
                label: 'Avg Words/Sentence',
                color: 'var(--warning)'
            },
            {
                icon: 'fas fa-star',
                value: this.getSentimentScore(result.sentiment),
                label: 'Sentiment Score',
                color: this.getSentimentColor(result.sentiment)
            }
        ];

        insightsGrid.innerHTML = insights.map(insight => `
            <div class="insight-item">
                <div class="insight-icon" style="color: ${insight.color}">
                    <i class="${insight.icon}"></i>
                </div>
                <div class="insight-value" style="color: ${insight.color}">${insight.value}</div>
                <div class="insight-label">${insight.label}</div>
            </div>
        `).join('');
    }

    getSentimentScore(sentiment) {
        switch (sentiment) {
            case 'positive': return '8.5/10';
            case 'neutral': return '5.0/10';
            case 'negative': return '2.5/10';
            default: return '5.0/10';
        }
    }

    getSentimentColor(sentiment) {
        switch (sentiment) {
            case 'positive': return 'var(--positive)';
            case 'neutral': return 'var(--neutral)';
            case 'negative': return 'var(--negative)';
            default: return 'var(--neutral)';
        }
    }

    saveToHistory(transcript, result) {
        const analysisResult = {
            id: Date.now(),
            timestamp: new Date(),
            transcript,
            summary: result.summary,
            sentiment: result.sentiment,
            processingTime: Date.now() // Simplified for demo
        };

        this.analysisHistory.unshift(analysisResult);
        
        if (this.analysisHistory.length > 50) {
            this.analysisHistory = this.analysisHistory.slice(0, 50);
        }
        
        localStorage.setItem('analysisHistory', JSON.stringify(this.analysisHistory));
        this.updateStats();
    }

    updateStats() {
        const totalAnalyzed = this.analysisHistory.length;
        const sentimentCounts = this.analysisHistory.reduce((acc, item) => {
            acc[item.sentiment] = (acc[item.sentiment] || 0) + 1;
            return acc;
        }, {});

        document.getElementById('totalAnalyzed').textContent = totalAnalyzed;
        
        if (totalAnalyzed > 0) {
            const avgSentiment = this.calculateAverageSentiment();
            document.getElementById('avgSentiment').textContent = avgSentiment;
        }

        document.getElementById('positiveCount').textContent = sentimentCounts.positive || 0;
        document.getElementById('neutralCount').textContent = sentimentCounts.neutral || 0;
        document.getElementById('negativeCount').textContent = sentimentCounts.negative || 0;
        document.getElementById('totalCount').textContent = totalAnalyzed;
    }

    calculateAverageSentiment() {
        if (this.analysisHistory.length === 0) return '--';

        const sentimentValues = this.analysisHistory.map(item => {
            switch (item.sentiment) {
                case 'positive': return 1;
                case 'neutral': return 0;
                case 'negative': return -1;
                default: return 0;
            }
        });

        const average = sentimentValues.reduce((a, b) => a + b, 0) / sentimentValues.length;
        
        if (average > 0.3) return 'Positive';
        if (average < -0.3) return 'Negative';
        return 'Neutral';
    }

    updateDashboard() {
        this.updateStats();
        this.updateChart();
    }

    initChart() {
        const ctx = document.getElementById('sentimentChart');
        if (!ctx) return;

        this.sentimentChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Positive', 'Neutral', 'Negative'],
                datasets: [{
                    data: [0, 0, 0],
                    backgroundColor: [
                        '#10B981',
                        '#6B7280', 
                        '#EF4444'
                    ],
                    borderColor: [
                        '#059669',
                        '#4B5563',
                        '#DC2626'
                    ],
                    borderWidth: 2,
                    hoverOffset: 15,
                    hoverBorderWidth: 3,
                    hoverBackgroundColor: [
                        '#34D399',
                        '#9CA3AF',
                        '#F87171'
                    ]
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                cutout: '60%',
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            padding: 25,
                            usePointStyle: true,
                            pointStyle: 'circle',
                            font: {
                                size: 14,
                                weight: '500'
                            },
                            color: 'var(--text-primary)',
                            generateLabels: function(chart) {
                                const data = chart.data;
                                if (data.labels.length && data.datasets.length) {
                                    return data.labels.map((label, i) => {
                                        const dataset = data.datasets[0];
                                        const value = dataset.data[i];
                                        const total = dataset.data.reduce((a, b) => a + b, 0);
                                        const percentage = total > 0 ? Math.round((value / total) * 100) : 0;
                                        
                                        return {
                                            text: `${label} (${percentage}%)`,
                                            fillStyle: dataset.backgroundColor[i],
                                            strokeStyle: dataset.borderColor[i],
                                            lineWidth: dataset.borderWidth,
                                            hidden: false,
                                            index: i
                                        };
                                    });
                                }
                                return [];
                            }
                        }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(0, 0, 0, 0.8)',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: '#374151',
                        borderWidth: 1,
                        cornerRadius: 8,
                        displayColors: true,
                        callbacks: {
                            label: function(context) {
                                const total = context.dataset.data.reduce((a, b) => a + b, 0);
                                const percentage = total > 0 ? Math.round((context.parsed / total) * 100) : 0;
                                return `${context.label}: ${context.parsed} (${percentage}%)`;
                            }
                        }
                    }
                },
                animation: {
                    animateRotate: true,
                    animateScale: true,
                    duration: 1000,
                    easing: 'easeOutQuart'
                },
                interaction: {
                    intersect: false,
                    mode: 'point'
                }
            }
        });

        this.updateChart();
    }

    updateChart() {
        if (!this.sentimentChart) return;

        const sentimentCounts = this.analysisHistory.reduce((acc, item) => {
            acc[item.sentiment] = (acc[item.sentiment] || 0) + 1;
            return acc;
        }, {});

        this.sentimentChart.data.datasets[0].data = [
            sentimentCounts.positive || 0,
            sentimentCounts.neutral || 0,
            sentimentCounts.negative || 0
        ];

        this.sentimentChart.update();
    }

    renderHistory() {
        const historyList = document.getElementById('historyList');
        
        if (this.analysisHistory.length === 0) {
            historyList.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-history"></i>
                    <h4>No Analysis History</h4>
                    <p>Your analyzed transcripts will appear here</p>
                </div>
            `;
            return;
        }

        const filteredHistory = this.getFilteredHistory();
        
        historyList.innerHTML = filteredHistory.map(item => `
            <div class="history-item ${item.sentiment}" onclick="app.showHistoryDetail(${item.id})">
                <div class="history-header">
                    <div class="sentiment-badge ${item.sentiment}">${item.sentiment}</div>
                    <div class="history-date">${this.formatDate(item.timestamp)}</div>
                </div>
                <div class="history-summary">${item.summary}</div>
                <div class="history-meta">
                    <span><i class="fas fa-file-word"></i> ${item.transcript.split(/\s+/).length} words</span>
                </div>
            </div>
        `).join('');
    }

    getFilteredHistory() {
        const sentimentFilter = document.getElementById('sentimentFilter').value;
        const searchQuery = document.getElementById('searchHistory').value.toLowerCase();
        
        return this.analysisHistory.filter(item => {
            const matchesSentiment = sentimentFilter === 'all' || item.sentiment === sentimentFilter;
            const matchesSearch = !searchQuery || 
                item.summary.toLowerCase().includes(searchQuery) ||
                item.transcript.toLowerCase().includes(searchQuery);
            
            return matchesSentiment && matchesSearch;
        });
    }

    filterHistory() {
        this.renderHistory();
    }

    showHistoryDetail(id) {
        const item = this.analysisHistory.find(h => h.id === id);
        if (!item) return;

        const modal = document.getElementById('detailModal');
        const modalBody = document.getElementById('modalBody');

        modalBody.innerHTML = `
            <div class="modal-detail">
                <div class="detail-header">
                    <div class="sentiment-badge ${item.sentiment}">${item.sentiment}</div>
                    <div class="detail-date">${this.formatDate(item.timestamp)}</div>
                </div>
                <div class="detail-section">
                    <h4><i class="fas fa-file-alt"></i> Summary</h4>
                    <p>${item.summary}</p>
                </div>
                <div class="detail-section">
                    <h4><i class="fas fa-microphone"></i> Original Transcript</h4>
                    <div class="transcript-preview">${item.transcript}</div>
                </div>
                <div class="detail-stats">
                    <div class="stat">
                        <strong>Word Count:</strong> ${item.transcript.split(/\s+/).length}
                    </div>
                    <div class="stat">
                        <strong>Sentiment Score:</strong> ${this.getSentimentScore(item.sentiment)}
                    </div>
                </div>
            </div>
        `;

        modal.classList.add('active');
    }

    closeModal() {
        document.getElementById('detailModal').classList.remove('active');
    }

    formatDate(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        }).format(new Date(date));
    }

    copySummary() {
        const summaryContent = document.getElementById('summaryContent').textContent;
        if (!summaryContent) {
            this.showToast('No summary to copy', 'warning');
            return;
        }

        navigator.clipboard.writeText(summaryContent).then(() => {
            this.showToast('Summary copied to clipboard', 'success');
        }).catch(() => {
            this.showToast('Failed to copy summary', 'error');
        });
    }

    exportResults() {
        if (this.analysisHistory.length === 0) {
            this.showToast('No results to export', 'warning');
            return;
        }

        const csvContent = this.generateCSV();
        const blob = new Blob([csvContent], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `call-analysis-${new Date().toISOString().split('T')[0]}.csv`;
        a.click();
        window.URL.revokeObjectURL(url);
        
        this.showToast('Results exported successfully', 'success');
    }

    generateCSV() {
        const headers = ['Timestamp', 'Sentiment', 'Summary', 'Word Count'];
        const rows = this.analysisHistory.map(item => [
            new Date(item.timestamp).toISOString(),
            item.sentiment,
            `"${item.summary.replace(/"/g, '""')}"`,
            item.transcript.split(/\s+/).length
        ]);

        return [headers, ...rows].map(row => row.join(',')).join('\n');
    }

    shareResults() {
        if (this.analysisHistory.length === 0) {
            this.showToast('No results to share', 'warning');
            return;
        }

        const latestResult = this.analysisHistory[0];
        const shareText = `CallAnalyzer Pro Results:\n\nSentiment: ${latestResult.sentiment}\nSummary: ${latestResult.summary}`;

        if (navigator.share) {
            navigator.share({
                title: 'Call Analysis Results',
                text: shareText
            }).catch(() => {
                this.copyToClipboard(shareText);
            });
        } else {
            this.copyToClipboard(shareText);
        }
    }

    copyToClipboard(text) {
        navigator.clipboard.writeText(text).then(() => {
            this.showToast('Results copied to clipboard', 'success');
        }).catch(() => {
            this.showToast('Failed to copy results', 'error');
        });
    }
}

const additionalStyles = `
    @keyframes slideOut {
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }

    .transcript-preview {
        background: var(--gray-50);
        padding: var(--space-md);
        border-radius: var(--radius-md);
        max-height: 200px;
        overflow-y: auto;
        white-space: pre-wrap;
        font-family: monospace;
        font-size: var(--font-size-sm);
        line-height: 1.5;
    }

    .detail-section {
        margin-bottom: var(--space-lg);
    }

    .detail-section h4 {
        margin-bottom: var(--space-sm);
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        color: var(--gray-800);
    }

    .detail-stats {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: var(--space-md);
        padding-top: var(--space-md);
        border-top: 1px solid var(--gray-200);
    }

    .stat {
        font-size: var(--font-size-sm);
        color: var(--gray-600);
    }

    .detail-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: var(--space-lg);
        padding-bottom: var(--space-md);
        border-bottom: 1px solid var(--gray-200);
    }

    .detail-date {
        color: var(--gray-500);
        font-size: var(--font-size-sm);
    }
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = additionalStyles;
document.head.appendChild(styleSheet);

document.addEventListener('DOMContentLoaded', () => {
    window.app = new CallAnalyzerApp();
});

const style = document.createElement('style');
style.textContent = `
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    @keyframes animate-in {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-in {
        animation: animate-in 0.6s ease-out forwards;
    }
`;
document.head.appendChild(style);
