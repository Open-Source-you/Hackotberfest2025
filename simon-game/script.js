// Simple Simon Game Logic

let buttonColors = ["red", "blue", "green", "yellow"];
let gamePattern = [];
let userClickedPattern = [];
let started = false;
let level = 0;

// Detect keypress to start
document.addEventListener("keydown", function() {
  if (!started) {
    document.getElementById("level-title").textContent = "Level " + level;
    nextSequence();
    started = true;
  }
});

// Detect user button clicks
let buttons = document.querySelectorAll(".btn");
buttons.forEach(btn => {
  btn.addEventListener("click", function() {
    let userChosenColor = this.id;
    userClickedPattern.push(userChosenColor);
    playSound(userChosenColor);
    animatePress(userChosenColor);
    checkAnswer(userClickedPattern.length - 1);
  });
});

// Function to check user's answer
function checkAnswer(currentLevel) {
  if (gamePattern[currentLevel] === userClickedPattern[currentLevel]) {
    if (userClickedPattern.length === gamePattern.length) {
      setTimeout(nextSequence, 1000);
    }
  } else {
    playSound("wrong");
    document.body.style.backgroundColor = "red";
    setTimeout(() => document.body.style.backgroundColor = "#011F3F", 200);
    document.getElementById("level-title").textContent = "Game Over, Press Any Key to Restart";
    startOver();
  }
}

// Generate next color in the sequence
function nextSequence() {
  userClickedPattern = [];
  level++;
  document.getElementById("level-title").textContent = "Level " + level;

  let randomNumber = Math.floor(Math.random() * 4);
  let randomChosenColor = buttonColors[randomNumber];
  gamePattern.push(randomChosenColor);

  let button = document.getElementById(randomChosenColor);
  button.classList.add("pressed");
  playSound(randomChosenColor);
  setTimeout(() => button.classList.remove("pressed"), 300);
}

// Play sound for each button
function playSound(name) {
  let audio = new Audio("https://s3.amazonaws.com/freecodecamp/simonSound" + (buttonColors.indexOf(name) + 1) + ".mp3");
  if (name === "wrong") audio = new Audio("https://s3.amazonaws.com/adam-recvlohe-sounds/error.mp3");
  audio.play();
}

// Animate button press
function animatePress(color) {
  let activeButton = document.getElementById(color);
  activeButton.classList.add("pressed");
  setTimeout(() => activeButton.classList.remove("pressed"), 100);
}

// Restart game
function startOver() {
  level = 0;
  gamePattern = [];
  started = false;
}
