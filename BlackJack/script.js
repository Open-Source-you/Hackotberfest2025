const suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades'];
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

function renderHand(playerId, hand, hideSecondCard = false) {
    const cardsDiv = document.getElementById(playerId + '-cards');
    if (hideSecondCard) {
        cardsDiv.innerHTML = `<div class="card">${hand[0].value}${suitsSymbols[hand[0].suit]}</div><div class="card card-back"></div>`;
        document.getElementById(playerId + '-score').textContent = 'Score: ' + getCardValue(hand[0]);
    } else {
        cardsDiv.innerHTML = hand.map(card => `<div class="card">${card.value}${suitsSymbols[card.suit]}</div>`).join('');
        document.getElementById(playerId + '-score').textContent = 'Score: ' + calculateScore(hand);
    }
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
    renderHand('player', playerHand);
    renderHand('dealer', dealerHand, true);
    document.getElementById('result').textContent = '';

    if (calculateScore(playerHand) === 21) {
        endGame('Blackjack! You win!');
    }
}

function hit() {
    if (isGameOver) return;
    dealCard(playerHand);
    renderHand('player', playerHand);
    if (calculateScore(playerHand) > 21) {
        endGame('You busted! Dealer wins.');
    }
}

function stand() {
    if (isGameOver) return;
    renderHand('dealer', dealerHand);
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
    renderHand('dealer', dealerHand);
    document.getElementById('result').textContent = message;
}

document.getElementById('deal').addEventListener('click', startGame);
document.getElementById('hit').addEventListener('click', hit);
document.getElementById('stand').addEventListener('click', stand);