// -
// POMODORO TIMER - MAIN JAVASCRIPT
// -

// -
// STATE MANAGEMENT
// -
const state = {
    // Timer settings (in seconds for easier calculation)
    workDuration: 25 * 60,
    shortBreakDuration: 5 * 60,
    longBreakDuration: 15 * 60,
    
    // Current timer state
    currentTime: 25 * 60,
    totalTime: 25 * 60,
    isRunning: false,
    currentSession: 'work', // 'work', 'short', 'long'
    
    // Pomodoro tracking
    completedPomodoros: 0,
    currentCycle: 1,
    totalCycles: 4,
    
    // Statistics
    totalFocusTime: 0, // in seconds
    
    // Settings
    autoStart: false,
    soundEnabled: true,
    
    // Timer interval
    timerInterval: null
};

// -
// DOM ELEMENTS
// -
const elements = {
    timeDisplay: document.getElementById('time-display'),
    sessionLabel: document.getElementById('session-label'),
    cycleInfo: document.getElementById('cycle-info'),
    startBtn: document.getElementById('start-btn'),
    pauseBtn: document.getElementById('pause-btn'),
    resetBtn: document.getElementById('reset-btn'),
    skipBtn: document.getElementById('skip-btn'),
    sessionBtns: document.querySelectorAll('.session-btn'),
    completedPomodorosEl: document.getElementById('completed-pomodoros'),
    totalTimeEl: document.getElementById('total-time'),
    progressCircle: document.querySelector('.progress-ring-circle'),
    timerDisplayEl: document.querySelector('.timer-display'),
    settingsPanel: document.getElementById('settings-panel'),
    settingsToggle: document.getElementById('settings-toggle'),
    themeToggle: document.getElementById('theme-toggle'),
    workDurationInput: document.getElementById('work-duration'),
    shortBreakInput: document.getElementById('short-break'),
    longBreakInput: document.getElementById('long-break'),
    autoStartInput: document.getElementById('auto-start'),
    soundEnabledInput: document.getElementById('sound-enabled'),
    saveSettingsBtn: document.getElementById('save-settings'),
    notificationSound: document.getElementById('notification-sound')
};

// -
// INITIALIZATION
// -
function init() {
    // Load saved data from localStorage
    loadFromLocalStorage();
    
    // Update UI
    updateDisplay();
    updateProgress();
    updateStats();
    updateSessionButtons();
    updateCycleInfo();
    
    // Setup event listeners
    setupEventListeners();
    
    // Update settings inputs to reflect current state
    updateSettingsInputs();
}

// -
// LOCAL STORAGE FUNCTIONS
// -
function loadFromLocalStorage() {
    const saved = localStorage.getItem('pomodoroData');
    if (saved) {
        const data = JSON.parse(saved);
        
        // Check if it's the same day
        const today = new Date().toDateString();
        if (data.date === today) {
            state.completedPomodoros = data.completedPomodoros || 0;
            state.totalFocusTime = data.totalFocusTime || 0;
        }
        
        // Load settings regardless of date
        if (data.workDuration) state.workDuration = data.workDuration;
        if (data.shortBreakDuration) state.shortBreakDuration = data.shortBreakDuration;
        if (data.longBreakDuration) state.longBreakDuration = data.longBreakDuration;
        state.autoStart = data.autoStart || false;
        state.soundEnabled = data.soundEnabled !== undefined ? data.soundEnabled : true;
        
        // Load theme
        if (data.theme === 'dark') {
            document.body.classList.add('dark-theme');
            elements.themeToggle.querySelector('.theme-icon').textContent = '☀️';
        }
    }
    
    // Reset current time to work duration
    state.currentTime = state.workDuration;
    state.totalTime = state.workDuration;
}

function saveToLocalStorage() {
    const data = {
        date: new Date().toDateString(),
        completedPomodoros: state.completedPomodoros,
        totalFocusTime: state.totalFocusTime,
        workDuration: state.workDuration,
        shortBreakDuration: state.shortBreakDuration,
        longBreakDuration: state.longBreakDuration,
        autoStart: state.autoStart,
        soundEnabled: state.soundEnabled,
        theme: document.body.classList.contains('dark-theme') ? 'dark' : 'light'
    };
    localStorage.setItem('pomodoroData', JSON.stringify(data));
}

// -
// EVENT LISTENERS
// -
function setupEventListeners() {
    // Timer controls
    elements.startBtn.addEventListener('click', startTimer);
    elements.pauseBtn.addEventListener('click', pauseTimer);
    elements.resetBtn.addEventListener('click', resetTimer);
    elements.skipBtn.addEventListener('click', skipSession);
    
    // Session type buttons
    elements.sessionBtns.forEach(btn => {
        btn.addEventListener('click', () => changeSession(btn.dataset.type));
    });
    
    // Settings
    elements.settingsToggle.addEventListener('click', toggleSettings);
    elements.saveSettingsBtn.addEventListener('click', saveSettings);
    
    // Theme toggle
    elements.themeToggle.addEventListener('click', toggleTheme);
    
    // Browser notification permission
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
}

// -
// TIMER FUNCTIONS
// -
function startTimer() {
    if (state.isRunning) return;
    
    state.isRunning = true;
    elements.startBtn.disabled = true;
    elements.pauseBtn.disabled = false;
    elements.timerDisplayEl.classList.add('pulse');
    
    // Start countdown
    state.timerInterval = setInterval(() => {
        state.currentTime--;
        
        // Update display
        updateDisplay();
        updateProgress();
        
        // Check if timer is complete
        if (state.currentTime <= 0) {
            completeSession();
        }
    }, 1000);
}

function pauseTimer() {
    state.isRunning = false;
    clearInterval(state.timerInterval);
    elements.startBtn.disabled = false;
    elements.pauseBtn.disabled = true;
    elements.timerDisplayEl.classList.remove('pulse');
}

function resetTimer() {
    pauseTimer();
    
    // Reset to current session duration
    switch(state.currentSession) {
        case 'work':
            state.currentTime = state.workDuration;
            state.totalTime = state.workDuration;
            break;
        case 'short':
            state.currentTime = state.shortBreakDuration;
            state.totalTime = state.shortBreakDuration;
            break;
        case 'long':
            state.currentTime = state.longBreakDuration;
            state.totalTime = state.longBreakDuration;
            break;
    }
    
    updateDisplay();
    updateProgress();
}

function skipSession() {
    pauseTimer();
    completeSession(true);
}

function completeSession(skipped = false) {
    pauseTimer();
    
    // Play notification sound
    if (state.soundEnabled && !skipped) {
        playNotificationSound();
    }
    
    // Show browser notification
    if (!skipped) {
        showNotification();
    }
    
    // Update stats if work session completed
    if (state.currentSession === 'work' && !skipped) {
        state.completedPomodoros++;
        state.totalFocusTime += state.workDuration;
        state.currentCycle++;
        updateStats();
        saveToLocalStorage();
    }
    
    // Determine next session
    let nextSession = 'work';
    
    if (state.currentSession === 'work') {
        // After work, decide between short and long break
        if (state.currentCycle > state.totalCycles) {
            nextSession = 'long';
            state.currentCycle = 1; // Reset cycle
        } else {
            nextSession = 'short';
        }
    }
    // If current session is a break, next is work
    
    // Change to next session
    changeSession(nextSession);
    
    // Auto-start if enabled
    if (state.autoStart && !skipped) {
        setTimeout(() => startTimer(), 1000);
    }
}

// -
// SESSION MANAGEMENT
// -
function changeSession(type) {
    pauseTimer();
    state.currentSession = type;
    
    // Set duration based on session type
    switch(type) {
        case 'work':
            state.currentTime = state.workDuration;
            state.totalTime = state.workDuration;
            elements.sessionLabel.textContent = 'Work Session';
            break;
        case 'short':
            state.currentTime = state.shortBreakDuration;
            state.totalTime = state.shortBreakDuration;
            elements.sessionLabel.textContent = 'Short Break';
            break;
        case 'long':
            state.currentTime = state.longBreakDuration;
            state.totalTime = state.longBreakDuration;
            elements.sessionLabel.textContent = 'Long Break';
            break;
    }
    
    updateDisplay();
    updateProgress();
    updateSessionButtons();
    updateCycleInfo();
}

// -
// UI UPDATE FUNCTIONS
// -
function updateDisplay() {
    const minutes = Math.floor(state.currentTime / 60);
    const seconds = state.currentTime % 60;
    elements.timeDisplay.textContent = `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
}

function updateProgress() {
    const circumference = 2 * Math.PI * 120; // radius is 120
    const progress = (state.currentTime / state.totalTime) * circumference;
    const offset = circumference - progress;
    
    elements.progressCircle.style.strokeDashoffset = offset;
}

function updateStats() {
    elements.completedPomodorosEl.textContent = state.completedPomodoros;
    
    const hours = Math.floor(state.totalFocusTime / 3600);
    const minutes = Math.floor((state.totalFocusTime % 3600) / 60);
    elements.totalTimeEl.textContent = `${hours}h ${minutes}m`;
}

function updateSessionButtons() {
    elements.sessionBtns.forEach(btn => {
        if (btn.dataset.type === state.currentSession) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });
}

function updateCycleInfo() {
    if (state.currentSession === 'work') {
        elements.cycleInfo.textContent = `Pomodoro ${state.currentCycle}/${state.totalCycles}`;
    } else {
        elements.cycleInfo.textContent = 'Break Time';
    }
}

function updateSettingsInputs() {
    elements.workDurationInput.value = state.workDuration / 60;
    elements.shortBreakInput.value = state.shortBreakDuration / 60;
    elements.longBreakInput.value = state.longBreakDuration / 60;
    elements.autoStartInput.checked = state.autoStart;
    elements.soundEnabledInput.checked = state.soundEnabled;
}

// -
// SETTINGS FUNCTIONS
// -
function toggleSettings() {
    elements.settingsPanel.classList.toggle('active');
}

function saveSettings() {
    // Get values and convert to seconds
    state.workDuration = parseInt(elements.workDurationInput.value) * 60;
    state.shortBreakDuration = parseInt(elements.shortBreakInput.value) * 60;
    state.longBreakDuration = parseInt(elements.longBreakInput.value) * 60;
    state.autoStart = elements.autoStartInput.checked;
    state.soundEnabled = elements.soundEnabledInput.checked;
    
    // Reset current timer if not running
    if (!state.isRunning) {
        resetTimer();
    }
    
    // Save to localStorage
    saveToLocalStorage();
    
    // Show confirmation
    elements.saveSettingsBtn.textContent = '✓ Saved!';
    setTimeout(() => {
        elements.saveSettingsBtn.textContent = 'Save Settings';
    }, 2000);
    
    // Close settings panel
    setTimeout(() => {
        elements.settingsPanel.classList.remove('active');
    }, 1500);
}

// -
// THEME TOGGLE
// -
function toggleTheme() {
    document.body.classList.toggle('dark-theme');
    const themeIcon = elements.themeToggle.querySelector('.theme-icon');
    
    if (document.body.classList.contains('dark-theme')) {
        themeIcon.textContent = '☀️';
    } else {
        themeIcon.textContent = '🌙';
    }
    
    saveToLocalStorage();
}

// -
// NOTIFICATION FUNCTIONS
// -
function playNotificationSound() {
    // Try to play the notification sound
    elements.notificationSound.play().catch(err => {
        console.log('Could not play notification sound:', err);
    });
}

function showNotification() {
    // Check if browser supports notifications
    if (!('Notification' in window)) return;
    
    // Check permission
    if (Notification.permission === 'granted') {
        let title = '';
        let body = '';
        
        if (state.currentSession === 'work') {
            title = '🎉 Work Session Complete!';
            body = 'Great job! Time for a break.';
        } else {
            title = '⏰ Break Time Over!';
            body = 'Ready to focus again?';
        }
        
        new Notification(title, {
            body: body,
            icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="%23FF6B6B"/></svg>',
            silent: false
        });
    }
}

// -
// UTILITY FUNCTIONS
// -
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}h ${minutes}m ${secs}s`;
    } else if (minutes > 0) {
        return `${minutes}m ${secs}s`;
    } else {
        return `${secs}s`;
    }
}

// -
// KEYBOARD SHORTCUTS
// -
document.addEventListener('keydown', (e) => {
    // Space bar to start/pause
    if (e.code === 'Space') {
        e.preventDefault();
        if (state.isRunning) {
            pauseTimer();
        } else {
            startTimer();
        }
    }
    
    // R key to reset
    if (e.code === 'KeyR') {
        e.preventDefault();
        resetTimer();
    }
    
    // S key to skip
    if (e.code === 'KeyS') {
        e.preventDefault();
        skipSession();
    }
});

// -
// PAGE VISIBILITY API
// Handle tab switching - pause timer when tab is not visible
// -
document.addEventListener('visibilitychange', () => {
    if (document.hidden && state.isRunning) {
        // Store the time when tab became hidden
        state.hiddenTime = Date.now();
    } else if (!document.hidden && state.hiddenTime) {
        // Calculate elapsed time while tab was hidden
        const elapsed = Math.floor((Date.now() - state.hiddenTime) / 1000);
        
        if (state.isRunning) {
            // Subtract elapsed time from current time
            state.currentTime = Math.max(0, state.currentTime - elapsed);
            updateDisplay();
            updateProgress();
            
            // Check if session completed while away
            if (state.currentTime <= 0) {
                completeSession();
            }
        }
        
        delete state.hiddenTime;
    }
});

// -
// UPDATE PAGE TITLE WITH TIMER
// -
function updatePageTitle() {
    if (state.isRunning) {
        const minutes = Math.floor(state.currentTime / 60);
        const seconds = state.currentTime % 60;
        const emoji = state.currentSession === 'work' ? '🍅' : '☕';
        document.title = `${emoji} ${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')} - Pomodoro Timer`;
    } else {
        document.title = 'Pomodoro Timer - Stay Focused';
    }
}

// Update title every second
setInterval(updatePageTitle, 1000);

// -
// ADD SVG GRADIENT FOR PROGRESS CIRCLE
// -
function addSVGGradient() {
    const svg = document.querySelector('.progress-ring');
    const defs = document.createElementNS('http://www.w3.org/2000/svg', 'defs');
    const gradient = document.createElementNS('http://www.w3.org/2000/svg', 'linearGradient');
    
    gradient.setAttribute('id', 'gradient');
    gradient.setAttribute('x1', '0%');
    gradient.setAttribute('y1', '0%');
    gradient.setAttribute('x2', '100%');
    gradient.setAttribute('y2', '100%');
    
    const stop1 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
    stop1.setAttribute('offset', '0%');
    stop1.setAttribute('stop-color', '#FF6B6B');
    
    const stop2 = document.createElementNS('http://www.w3.org/2000/svg', 'stop');
    stop2.setAttribute('offset', '100%');
    stop2.setAttribute('stop-color', '#FFA06B');
    
    gradient.appendChild(stop1);
    gradient.appendChild(stop2);
    defs.appendChild(gradient);
    svg.insertBefore(defs, svg.firstChild);
}

// -
// INITIALIZE APP ON PAGE LOAD
// -
document.addEventListener('DOMContentLoaded', () => {
    addSVGGradient();
    init();
});

// -
// PREVENT PAGE UNLOAD DURING ACTIVE TIMER
// -
window.addEventListener('beforeunload', (e) => {
    if (state.isRunning) {
        e.preventDefault();
        e.returnValue = 'Timer is running. Are you sure you want to leave?';
        return e.returnValue;
    }
});