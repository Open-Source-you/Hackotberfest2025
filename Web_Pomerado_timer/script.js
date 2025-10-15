const state = {
  workDuration: 25 * 60,
  shortBreakDuration: 5 * 60,
  longBreakDuration: 15 * 60,

  currentTime: 25 * 60,
  totalTime: 25 * 60,
  isRunning: false,
  currentSession: "work",

  completedPomodoros: 0,
  currentCycle: 1,
  totalCycles: 4,

  totalFocusTime: 0,

  autoStart: false,
  soundEnabled: true,

  timerInterval: null,
};

const elements = {
  timeDisplay: document.getElementById("time-display"),
  sessionLabel: document.getElementById("session-label"),
  cycleInfo: document.getElementById("cycle-info"),
  startBtn: document.getElementById("start-btn"),
  pauseBtn: document.getElementById("pause-btn"),
  resetBtn: document.getElementById("reset-btn"),
  skipBtn: document.getElementById("skip-btn"),
  sessionBtns: document.querySelectorAll(".session-btn"),
  completedPomodorosEl: document.getElementById("completed-pomodoros"),
  totalTimeEl: document.getElementById("total-time"),
  progressCircle: document.querySelector(".progress-ring-circle"),
  timerDisplayEl: document.querySelector(".timer-display"),
  settingsPanel: document.getElementById("settings-panel"),
  settingsToggle: document.getElementById("settings-toggle"),
  themeToggle: document.getElementById("theme-toggle"),
  workDurationInput: document.getElementById("work-duration"),
  shortBreakInput: document.getElementById("short-break"),
  longBreakInput: document.getElementById("long-break"),
  autoStartInput: document.getElementById("auto-start"),
  soundEnabledInput: document.getElementById("sound-enabled"),
  saveSettingsBtn: document.getElementById("save-settings"),
  notificationSound: document.getElementById("notification-sound"),
};

function init() {
  loadFromLocalStorage();

  updateDisplay();
  updateProgress();
  updateStats();
  updateSessionButtons();
  updateCycleInfo();

  setupEventListeners();

  updateSettingsInputs();
}

function loadFromLocalStorage() {
  const saved = localStorage.getItem("pomodoroData");
  if (saved) {
    const data = JSON.parse(saved);

    const today = new Date().toDateString();
    if (data.date === today) {
      state.completedPomodoros = data.completedPomodoros || 0;
      state.totalFocusTime = data.totalFocusTime || 0;
    }

    if (data.workDuration) state.workDuration = data.workDuration;
    if (data.shortBreakDuration)
      state.shortBreakDuration = data.shortBreakDuration;
    if (data.longBreakDuration)
      state.longBreakDuration = data.longBreakDuration;
    state.autoStart = data.autoStart || false;
    state.soundEnabled =
      data.soundEnabled !== undefined ? data.soundEnabled : true;

    if (data.theme === "dark") {
      document.body.classList.add("dark-theme");
      elements.themeToggle.querySelector(".theme-icon").textContent = "☀️";
    }
  }

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
    theme: document.body.classList.contains("dark-theme") ? "dark" : "light",
  };
  localStorage.setItem("pomodoroData", JSON.stringify(data));
}

function setupEventListeners() {
  elements.startBtn.addEventListener("click", startTimer);
  elements.pauseBtn.addEventListener("click", pauseTimer);
  elements.resetBtn.addEventListener("click", resetTimer);
  elements.skipBtn.addEventListener("click", skipSession);

  elements.sessionBtns.forEach((btn) => {
    btn.addEventListener("click", () => changeSession(btn.dataset.type));
  });

  elements.settingsToggle.addEventListener("click", toggleSettings);
  elements.saveSettingsBtn.addEventListener("click", saveSettings);

  elements.themeToggle.addEventListener("click", toggleTheme);

  if ("Notification" in window && Notification.permission === "default") {
    Notification.requestPermission();
  }
}

function startTimer() {
  if (state.isRunning) return;

  state.isRunning = true;
  elements.startBtn.disabled = true;
  elements.pauseBtn.disabled = false;
  elements.timerDisplayEl.classList.add("pulse");

  state.timerInterval = setInterval(() => {
    state.currentTime--;

    updateDisplay();
    updateProgress();

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
  elements.timerDisplayEl.classList.remove("pulse");
}

function resetTimer() {
  pauseTimer();

  switch (state.currentSession) {
    case "work":
      state.currentTime = state.workDuration;
      state.totalTime = state.workDuration;
      break;
    case "short":
      state.currentTime = state.shortBreakDuration;
      state.totalTime = state.shortBreakDuration;
      break;
    case "long":
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

  if (state.soundEnabled && !skipped) {
    playNotificationSound();
  }

  if (!skipped) {
    showNotification();
  }

  if (state.currentSession === "work" && !skipped) {
    state.completedPomodoros++;
    state.totalFocusTime += state.workDuration;
    state.currentCycle++;
    updateStats();
    saveToLocalStorage();
  }

  let nextSession = "work";

  if (state.currentSession === "work") {
    if (state.currentCycle > state.totalCycles) {
      nextSession = "long";
      state.currentCycle = 1;
    } else {
      nextSession = "short";
    }
  }

  changeSession(nextSession);

  if (state.autoStart && !skipped) {
    setTimeout(() => startTimer(), 1000);
  }
}

function changeSession(type) {
  pauseTimer();
  state.currentSession = type;

  switch (type) {
    case "work":
      state.currentTime = state.workDuration;
      state.totalTime = state.workDuration;
      elements.sessionLabel.textContent = "Work Session";
      break;
    case "short":
      state.currentTime = state.shortBreakDuration;
      state.totalTime = state.shortBreakDuration;
      elements.sessionLabel.textContent = "Short Break";
      break;
    case "long":
      state.currentTime = state.longBreakDuration;
      state.totalTime = state.longBreakDuration;
      elements.sessionLabel.textContent = "Long Break";
      break;
  }

  updateDisplay();
  updateProgress();
  updateSessionButtons();
  updateCycleInfo();
}

function updateDisplay() {
  const minutes = Math.floor(state.currentTime / 60);
  const seconds = state.currentTime % 60;
  elements.timeDisplay.textContent = `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
}

function updateProgress() {
  const circumference = 2 * Math.PI * 120;
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
  elements.sessionBtns.forEach((btn) => {
    if (btn.dataset.type === state.currentSession) {
      btn.classList.add("active");
    } else {
      btn.classList.remove("active");
    }
  });
}

function updateCycleInfo() {
  if (state.currentSession === "work") {
    elements.cycleInfo.textContent = `Pomodoro ${state.currentCycle}/${state.totalCycles}`;
  } else {
    elements.cycleInfo.textContent = "Break Time";
  }
}

function updateSettingsInputs() {
  elements.workDurationInput.value = state.workDuration / 60;
  elements.shortBreakInput.value = state.shortBreakDuration / 60;
  elements.longBreakInput.value = state.longBreakDuration / 60;
  elements.autoStartInput.checked = state.autoStart;
  elements.soundEnabledInput.checked = state.soundEnabled;
}

function toggleSettings() {
  elements.settingsPanel.classList.toggle("active");
}

function saveSettings() {
  state.workDuration = parseInt(elements.workDurationInput.value) * 60;
  state.shortBreakDuration = parseInt(elements.shortBreakInput.value) * 60;
  state.longBreakDuration = parseInt(elements.longBreakInput.value) * 60;
  state.autoStart = elements.autoStartInput.checked;
  state.soundEnabled = elements.soundEnabledInput.checked;

  if (!state.isRunning) {
    resetTimer();
  }

  saveToLocalStorage();

  elements.saveSettingsBtn.textContent = "✓ Saved!";
  setTimeout(() => {
    elements.saveSettingsBtn.textContent = "Save Settings";
  }, 2000);

  setTimeout(() => {
    elements.settingsPanel.classList.remove("active");
  }, 1500);
}

function toggleTheme() {
  document.body.classList.toggle("dark-theme");
  const themeIcon = elements.themeToggle.querySelector(".theme-icon");

  if (document.body.classList.contains("dark-theme")) {
    themeIcon.textContent = "☀️";
  } else {
    themeIcon.textContent = "🌙";
  }

  saveToLocalStorage();
}

function playNotificationSound() {
  elements.notificationSound.play().catch((err) => {
    console.log("Could not play notification sound:", err);
  });
}

function showNotification() {
  if (!("Notification" in window)) return;

  if (Notification.permission === "granted") {
    let title = "";
    let body = "";

    if (state.currentSession === "work") {
      title = "🎉 Work Session Complete!";
      body = "Great job! Time for a break.";
    } else {
      title = "⏰ Break Time Over!";
      body = "Ready to focus again?";
    }

    new Notification(title, {
      body: body,
      icon: 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="45" fill="%23FF6B6B"/></svg>',
      silent: false,
    });
  }
}

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

document.addEventListener("keydown", (e) => {
  if (e.code === "Space") {
    e.preventDefault();
    if (state.isRunning) {
      pauseTimer();
    } else {
      startTimer();
    }
  }

  if (e.code === "KeyR") {
    e.preventDefault();
    resetTimer();
  }

  if (e.code === "KeyS") {
    e.preventDefault();
    skipSession();
  }
});

document.addEventListener("visibilitychange", () => {
  if (document.hidden && state.isRunning) {
    state.hiddenTime = Date.now();
  } else if (!document.hidden && state.hiddenTime) {
    const elapsed = Math.floor((Date.now() - state.hiddenTime) / 1000);

    if (state.isRunning) {
      state.currentTime = Math.max(0, state.currentTime - elapsed);
      updateDisplay();
      updateProgress();

      if (state.currentTime <= 0) {
        completeSession();
      }
    }

    delete state.hiddenTime;
  }
});

function updatePageTitle() {
  if (state.isRunning) {
    const minutes = Math.floor(state.currentTime / 60);
    const seconds = state.currentTime % 60;
    const emoji = state.currentSession === "work" ? "🍅" : "☕";
    document.title = `${emoji} ${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")} - Pomodoro Timer`;
  } else {
    document.title = "Pomodoro Timer - Stay Focused";
  }
}

setInterval(updatePageTitle, 1000);

function addSVGGradient() {
  const svg = document.querySelector(".progress-ring");
  const defs = document.createElementNS("http://www.w3.org/2000/svg", "defs");
  const gradient = document.createElementNS(
    "http://www.w3.org/2000/svg",
    "linearGradient",
  );

  gradient.setAttribute("id", "gradient");
  gradient.setAttribute("x1", "0%");
  gradient.setAttribute("y1", "0%");
  gradient.setAttribute("x2", "100%");
  gradient.setAttribute("y2", "100%");

  const stop1 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop1.setAttribute("offset", "0%");
  stop1.setAttribute("stop-color", "#FF6B6B");

  const stop2 = document.createElementNS("http://www.w3.org/2000/svg", "stop");
  stop2.setAttribute("offset", "100%");
  stop2.setAttribute("stop-color", "#FFA06B");

  gradient.appendChild(stop1);
  gradient.appendChild(stop2);
  defs.appendChild(gradient);
  svg.insertBefore(defs, svg.firstChild);
}

document.addEventListener("DOMContentLoaded", () => {
  addSVGGradient();
  init();
});

window.addEventListener("beforeunload", (e) => {
  if (state.isRunning) {
    e.preventDefault();
    e.returnValue = "Timer is running. Are you sure you want to leave?";
    return e.returnValue;
  }
});
