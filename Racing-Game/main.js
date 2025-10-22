var scores, roundScore, activePlayer, dice, gamePlaying, lastDice;
init();


document.querySelector('.btn-roll').addEventListener('click', function(){
	if (gamePlaying){
		let dice = Math.floor(Math.random() * 6) + 1;
		let diceDOM = document.querySelector('.dice');

		// Display result
		diceDOM.style.display = 'block';
		diceDOM.src = 'dice-' + dice + '.png';

		// Update round score if rolled num !== 1
		if (dice === 6 && lastDice === 6){
			// player looses score
			scores[activePlayer] = 0;
			document.querySelector('#score-' + activePlayer).textContent = scores[activePlayer];
			nextPlayer();
		} else if(dice !== 1){
			// Add score
			roundScore += dice;
			document.querySelector('#current-' + activePlayer).textContent = roundScore;
		} else {
			// Next player
			nextPlayer();
		}

	  lastDice = dice;
	}
});

document.querySelector('.btn-hold').addEventListener('click', function(){
	if (gamePlaying){
		// Add current score to global score
		scores[activePlayer] += roundScore;
		// Update UI
		document.querySelector('#score-' + activePlayer).textContent = scores[activePlayer];

		let input = document.querySelector('.final-score').value;
		let winningScore;

		if(input){
			winningScore = input;
		} else {
			winningScore = 100;
		}

		// Check if player won the game
		if (scores[activePlayer] >= input){
			document.querySelector('#name-' + activePlayer).textContent = 'WINNER!...';
			document.querySelector('.dice').style.display = 'none';
			document.querySelector('.player-' + activePlayer + '-panel').classList.add('winner');
			document.	querySelector('.player-' + activePlayer + '-panel').classList.remove('active');
			gamePlaying = false;
		} else {
			nextPlayer();
		}
	}

});

function nextPlayer(){
	activePlayer === 0 ? activePlayer = 1 : activePlayer = 0;
	roundScore = 0;

	document.getElementById('current-0').textContent = '0';
	document.getElementById('current-1').textContent = '0';

	document.querySelector('.player-0-panel').classList.toggle('active');
	document.querySelector('.player-1-panel').classList.toggle('active');

	document.querySelector('.dice').style.display = 'none';
};

document.querySelector('.btn-new').addEventListener('click', init);

function init(){
	scores = [0, 0];
	activePlayer = 0;
	roundScore = 0;
	gamePlaying = true;

	document.querySelector('.dice').style.display = 'none';

	document.getElementById('score-0').textContent = '0';
	document.getElementById('score-1').textContent = '0';

	document.getElementById('current-0').textContent = '0';
	document.getElementById('current-1').textContent = '0';

	document.getElementById('name-0').textContent = 'Player 1';
	document.getElementById('name-1').textContent = 'Player 2';

	document.querySelector('.player-0-panel').classList.remove('winner');
	document.querySelector('.player-1-panel').classList.remove('winner');
	document.querySelector('.player-0-panel').classList.remove('active');
	document.querySelector('.player-1-panel').classList.remove('active');

	document.querySelector('.player-0-panel').classList.add('active');
}
