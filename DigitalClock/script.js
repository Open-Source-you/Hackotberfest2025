let alarmTime = null;
let alarmTimeout = null;
let timerInterval = null;
let stopwatchInterval = null;
let timerDuration = 0;
let stopwatchTime = 0;

function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    
    document.getElementById('clock').textContent = `${hours}:${minutes}:${seconds}`;
    document.getElementById('date').textContent = now.toLocaleDateString();
    checkAlarm();
}

function setMood() {
    const mood = document.getElementById('mood').value;
    let bgColor;
    
    switch (mood) {
        case 'happy':
            bgColor = 'yellow';
            break;
        case 'neutral':
            bgColor = 'grey';
            break;
        case 'sad':
            bgColor = 'blue';
            break;
        default:
            bgColor = 'black';
    }
    
    document.body.style.backgroundColor = bgColor;
}

const alarmSound = new Audio('audio.mp3');

function setAlarm() {
    const alarmInput = document.getElementById('alarmTime').value;
    
    if (alarmInput) {
        const [hours, minutes] = alarmInput.split(':');
        const now = new Date();
        alarmTime = new Date(now.getFullYear(), now.getMonth(), now.getDate(), hours, minutes).getTime();
        
        if (alarmTimeout) clearTimeout(alarmTimeout);
        
        alarmTimeout = setTimeout(() => {
            alarmSound.play(); // Play the alarm sound
            alert("Alarm ringing!");
            startMultiplicationGame();
        }, alarmTime - now.getTime());
    }
}

function checkAlarm() {
    const now = new Date().getTime();
    
    if (alarmTime && now >= alarmTime) {
        clearTimeout(alarmTimeout);
        alarmTimeout = null; // Reset alarm timeout
    }
}

function startMultiplicationGame() {
    const num1 = Math.floor(Math.random() * 10);
    const num2 = Math.floor(Math.random() * 10);
    
    document.getElementById('question').textContent = `What is ${num1} x ${num2}?`;
    document.getElementById('multiplicationGame').style.display = 'block';
    
    document.getElementById('submitAnswer').onclick = () => checkAnswer(num1, num2);
}

function checkAnswer(num1, num2) {
    const userAnswer = Number(document.getElementById('answer').value);
    const correctAnswer = num1 * num2;
    
    document.getElementById('feedback').textContent = userAnswer === correctAnswer
        ? "Correct!"
        : `Wrong! The correct answer was ${correctAnswer}.`;
    
    document.getElementById('answer').value = '';
    document.getElementById('multiplicationGame').style.display = 'none'; // Hide after answering
}

function startTimer() {
    if (!timerInterval) {
        timerInterval = setInterval(() => {
            timerDuration++;
            const minutes = String(Math.floor(timerDuration / 60)).padStart(2, '0');
            const seconds = String(timerDuration % 60).padStart(2, '0');
            
            document.getElementById('timer').textContent = `Timer: ${minutes}:${seconds}`;
        }, 1000);
    }
}

function stopTimer() {
    clearInterval(timerInterval);
    timerInterval = null;
}

function resetTimer() {
    stopTimer();
    timerDuration = 0;
    document.getElementById('timer').textContent = 'Timer: 00:00';
}

function startStopwatch() {
    if (!stopwatchInterval) {
        stopwatchInterval = setInterval(() => {
            stopwatchTime++;
            const minutes = String(Math.floor(stopwatchTime / 60)).padStart(2, '0');
            const seconds = String(stopwatchTime % 60).padStart(2, '0');
            
            document.getElementById('stopwatch').textContent = `Stopwatch: ${minutes}:${seconds}`;
        }, 1000);
    }
}

function stopStopwatch() {
    clearInterval(stopwatchInterval);
    stopwatchInterval = null;
}

function resetStopwatch() {
    stopStopwatch();
    stopwatchTime = 0;
    document.getElementById('stopwatch').textContent = 'Stopwatch: 00:00';
}

setInterval(updateClock, 1000);

document.getElementById('setMood').addEventListener('click', setMood);
document.getElementById('setAlarm').addEventListener('click', setAlarm);
document.getElementById('startTimer').addEventListener('click', startTimer);
document.getElementById('stopTimer').addEventListener('click', stopTimer);
document.getElementById('resetTimer').addEventListener('click', resetTimer);
document.getElementById('startStopwatch').addEventListener('click', startStopwatch);
document.getElementById('stopStopwatch').addEventListener('click', stopStopwatch);
document.getElementById('resetStopwatch').addEventListener('click', resetStopwatch);
