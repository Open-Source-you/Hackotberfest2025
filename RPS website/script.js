const game = () => {
    let playerScore = 0;
    let computerScore = 0;
    let moves = 0;

    const playGame = () => {
        const rockBtn = document.querySelector('.rock');
        const paperBtn = document.querySelector('.paper');
        const scissorBtn = document.querySelector('.scissor');
        const playerOptions = [rockBtn, paperBtn, scissorBtn];
        const computerOptions = ['rock', 'paper', 'scissors'];

        playerOptions.forEach(option => {
            option.addEventListener('click', function () {
                const movesLeft = document.querySelector('.moves-count');
                moves++;
                movesLeft.innerText = 10 - moves;

                const choiceNumber = Math.floor(Math.random() * 3);
                const computerChoice = computerOptions[choiceNumber];

                winner(this.className, computerChoice);

                if (moves === 10) {
                    gameOver(playerOptions, movesLeft.parentElement);
                }
            });
        });
    };

    const winner = (player, computer) => {
        const result = document.querySelector('.result');
        const playerScoreBoard = document.querySelector('.p-count');
        const computerScoreBoard = document.querySelector('.c-count');
        player = player.toLowerCase();
        computer = computer.toLowerCase();

        result.style.opacity = '0';
        setTimeout(() => {
            if (player === computer) {
                result.textContent = `It's a Tie! 🤝`;
                result.style.color = 'grey';
            } else if (player === 'rock') {
                if (computer === 'paper') {
                    result.textContent = 'Computer Won! 📄 beats 🪨';
                    result.style.color = 'red';
                    computerScore++;
                    computerScoreBoard.textContent = computerScore;
                } else {
                    result.textContent = 'You Won! 🪨 beats ✂️';
                    result.style.color = '#28a745';
                    playerScore++;
                    playerScoreBoard.textContent = playerScore;
                }
            } else if (player === 'paper') {
                if (computer === 'scissors') {
                    result.textContent = 'Computer Won! ✂️ beats 📄';
                    result.style.color = 'red';
                    computerScore++;
                    computerScoreBoard.textContent = computerScore;
                } else {
                    result.textContent = 'You Won! 📄 beats 🪨';
                    result.style.color = '#28a745';
                    playerScore++;
                    playerScoreBoard.textContent = playerScore;
                }
            } else if (player === 'scissor') {
                if (computer === 'rock') {
                    result.textContent = 'Computer Won! 🪨 beats ✂️';
                    result.style.color = 'red';
                    computerScore++;
                    computerScoreBoard.textContent = computerScore;
                } else {
                    result.textContent = 'You Won! ✂️ beats 📄';
                    result.style.color = '#28a745';
                    playerScore++;
                    playerScoreBoard.textContent = playerScore;
                }
            }
            result.style.opacity = '1';
        }, 300);
    };

    const gameOver = (playerOptions, movesLeft) => {
        const chooseMove = document.querySelector('.move');
        const result = document.querySelector('.result');
        const reloadBtn = document.querySelector('.reload');

        playerOptions.forEach(option => {
            option.style.display = 'none';
        });

        chooseMove.innerText = 'Game Over!';
        movesLeft.style.display = 'none';

        result.style.fontSize = '2rem';
        if (playerScore > computerScore) {
            result.innerText = 'You Won The Game! 🎉';
            result.style.color = '#28a745';
        } else if (playerScore < computerScore) {
            result.innerText = 'You Lost The Game 😔';
            result.style.color = 'red';
        } else {
            result.innerText = 'It’s a Tie! 🤝';
            result.style.color = 'grey';
        }

        reloadBtn.style.display = 'block';
        reloadBtn.addEventListener('click', () => {
            window.location.reload();
        });
    };

    playGame();
};

game();
