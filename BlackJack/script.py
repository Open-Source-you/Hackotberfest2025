import os

# Recreate blackjack_game folder and files with interactive cards display
os.makedirs('blackjack_game', exist_ok=True)

html_code = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Blackjack</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div class="game-container">
        <h1>Blackjack</h1>
        <div id="dealer" class="hand">
            <h2>Dealer's Hand</h2>
            <div id="dealer-cards" class="cards"></div>
            <p id="dealer-score"></p>
        </div>

        <div id="player" class="hand">
            <h2>Your Hand</h2>
            <div id="player-cards" class="cards"></div>
            <p id="player-score"></p>
        </div>

        <div class="controls">
            <button id="deal">Deal</button>
            <button id="hit">Hit</button>
            <button id="stand">Stand</button>
        </div>

        <p id="result"></p>
    </div>

    <script src="script.js"></script>
</body>
</html>'''

css_code = '''body {
    font-family: Arial, sans-serif;
    background-color: #0b3d02;
    color: white;
    text-align: center;
    margin: 0;
    padding: 0;
}

.game-container {
    margin-top: 50px;
}

.hand {
    margin: 20px;
    border: 1px solid #fff;
    border-radius: 8px;
    padding: 10px;
    display: inline-block;
    width: 250px;
    background-color: #145214;
}

.cards {
    min-height: 80px;
    display: flex;
    justify-content: center;
}

button {
    margin: 10px;
    padding: 10px 20px;
    background-color: #228b22;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #2e8b57;
}

.card {
    display: inline-block;
    border: 1px solid white;
    border-radius: 8px;
    width: 50px;
    height: 70px;
    line-height: 70px;
    margin: 5px;
    font-size: 24px;
    background-color: #ffffff33;
    color: white;
    text-align: center;
    user-select: none;
}
'''

js_code = '''const suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades'];
const suitsSymbols = {'Hearts': '♥', 'Diamonds': '♦', 'Clubs': '♣', 'Spades': '♠'};
const values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'];
let deck = [];
let playerHand = [];
let dealerHand = [];
let isGameOver = false;

function createDeck() {
    deck = [];
    for (let s of suits) {
        for (let v of values) {
            deck.push({suit: s, value: v});
        }
    }
}

function getCardValue(card) {
    if (['J','Q','K'].includes(card.value)) return 10;
    if (card.value === 'A') return 11;
    return parseInt(card.value);
}

function calculateScore(hand) {
    let score = 0;
    let aces = 0;
    for (let card of hand) {
        score += getCardValue(card);
        if (card.value === 'A') aces++;
    }
    while (score > 21 && aces > 0) {
        score -= 10;
        aces--;
    }
    return score;
}

function dealCard(player) {
    const card = deck.pop();
    player.push(card);
}

function renderHand(playerId, hand) {
    const cardsDiv = document.getElementById(playerId + '-cards');
    cardsDiv.innerHTML = hand.map(card => `<div class=\"card\">${card.value}${suitsSymbols[card.suit]}</div>`).join('');
    document.getElementById(playerId + '-score').textContent = 'Score: ' + calculateScore(hand);
}

function startGame() {
    isGameOver = false;
    createDeck();
    deck.sort(() => Math.random() - 0.5);
    playerHand = [];
    dealerHand = [];
    for (let i = 0; i < 2; i++) {
        dealCard(playerHand);
        dealCard(dealerHand);
    }
    renderGame();
    document.getElementById('result').textContent = '';
}

function renderGame() {
    renderHand('player', playerHand);
    renderHand('dealer', dealerHand);

    const playerScore = calculateScore(playerHand);
    if (playerScore > 21) {
        endGame('You busted! Dealer wins.');
    }
}

function hit() {
    if (isGameOver) return;
    dealCard(playerHand);
    renderGame();
}

function stand() {
    if (isGameOver) return;
    const dealerPlay = setInterval(() => {
        if (calculateScore(dealerHand) < 17) {
            dealCard(dealerHand);
            renderHand('dealer', dealerHand);
        } else {
            clearInterval(dealerPlay);
            checkWinner();
        }
    }, 500);
}

function checkWinner() {
    const playerScore = calculateScore(playerHand);
    const dealerScore = calculateScore(dealerHand);

    if (dealerScore > 21 || playerScore > dealerScore) {
        endGame('You win!');
    } else if (dealerScore === playerScore) {
        endGame('Push!');
    } else {
        endGame('Dealer wins!');
    }
}

function endGame(message) {
    isGameOver = true;
    document.getElementById('result').textContent = message;
}

document.getElementById('deal').addEventListener('click', startGame);
document.getElementById('hit').addEventListener('click', hit);
document.getElementById('stand').addEventListener('click', stand);'''

with open('blackjack_game/index.html', 'w') as f:
    f.write(html_code)
with open('blackjack_game/style.css', 'w') as f:
    f.write(css_code)
with open('blackjack_game/script.js', 'w') as f:
    f.write(js_code)

'Updated interactive Blackjack game created'