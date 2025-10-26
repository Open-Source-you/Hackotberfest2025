
        const diceEmojis = ['⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];
        let gameState = {
            score1: 0,
            score2: 0,
            round: 1,
            p1Wins: 0,
            p2Wins: 0,
            ties: 0,
            mode: 'bestOf5',
            isRolling: false,
            history: []
        };

        function createParticles() {
            const container = document.getElementById('particles');
            for (let i = 0; i < 30; i++) {
                const particle = document.createElement('div');
                particle.className = 'particle';
                particle.style.width = Math.random() * 5 + 2 + 'px';
                particle.style.height = particle.style.width;
                particle.style.left = Math.random() * 100 + '%';
                particle.style.animationDelay = Math.random() * 15 + 's';
                particle.style.animationDuration = Math.random() * 10 + 10 + 's';
                container.appendChild(particle);
            }
        }

        createParticles();

        function setGameMode(mode) {
            gameState.mode = mode;
            document.querySelectorAll('.mode-btn').forEach(btn => btn.classList.remove('active'));
            event.target.classList.add('active');
            resetGame();
        }

        function rollDice() {
            if (gameState.isRolling) return;
            
            gameState.isRolling = true;
            const rollBtn = document.getElementById('rollBtn');
            rollBtn.disabled = true;

            const dice1 = document.getElementById('dice1');
            const dice2 = document.getElementById('dice2');
            const p1Zone = document.getElementById('player1Zone');
            const p2Zone = document.getElementById('player2Zone');
            
            p1Zone.classList.add('active');
            p2Zone.classList.add('active');
            
            dice1.classList.add('rolling');
            dice2.classList.add('rolling');

            const speed = document.getElementById('speedToggle').value;
            const duration = speed === 'fast' ? 6 : speed === 'slow' ? 18 : 12;
            const interval = speed === 'fast' ? 50 : speed === 'slow' ? 120 : 80;

            let counter = 0;
            const rollInterval = setInterval(() => {
                const temp1 = Math.floor(Math.random() * 6);
                const temp2 = Math.floor(Math.random() * 6);
                dice1.textContent = diceEmojis[temp1];
                dice2.textContent = diceEmojis[temp2];
                counter++;
                
                if (counter >= duration) {
                    clearInterval(rollInterval);
                    finishRoll();
                }
            }, interval);
        }

        function finishRoll() {
            const roll1 = Math.floor(Math.random() * 6) + 1;
            const roll2 = Math.floor(Math.random() * 6) + 1;

            const dice1 = document.getElementById('dice1');
            const dice2 = document.getElementById('dice2');
            
            dice1.textContent = diceEmojis[roll1 - 1];
            dice2.textContent = diceEmojis[roll2 - 1];

            dice1.classList.remove('rolling');
            dice2.classList.remove('rolling');

            const p1Zone = document.getElementById('player1Zone');
            const p2Zone = document.getElementById('player2Zone');
            
            p1Zone.classList.remove('active');
            p2Zone.classList.remove('active');

            gameState.score1 += roll1;
            gameState.score2 += roll2;

            let result = '';
            let historyClass = '';

            if (roll1 > roll2) {
                gameState.p1Wins++;
                p1Zone.classList.add('winner');
                result = document.getElementById('player1Name').textContent + ' wins!';
                historyClass = 'p1-win';
                setTimeout(() => p1Zone.classList.remove('winner'), 1000);
            } else if (roll2 > roll1) {
                gameState.p2Wins++;
                p2Zone.classList.add('winner');
                result = document.getElementById('player2Name').textContent + ' wins!';
                historyClass = 'p2-win';
                setTimeout(() => p2Zone.classList.remove('winner'), 1000);
            } else {
                gameState.ties++;
                result = "It's a tie!";
                historyClass = 'tie';
            }

            updateDisplay();
            addToHistory(roll1, roll2, result, historyClass);

            gameState.round++;
            
            setTimeout(() => {
                const gameOver = checkGameOver();
                gameState.isRolling = false;
                if (!gameOver) {
                    document.getElementById('rollBtn').disabled = false;
                }
            }, 1500);
        }

        function updateDisplay() {
            document.getElementById('score1').textContent = gameState.score1;
            document.getElementById('score2').textContent = gameState.score2;
            document.getElementById('p1Wins').textContent = gameState.p1Wins;
            document.getElementById('p2Wins').textContent = gameState.p2Wins;
            document.getElementById('tieCount').textContent = gameState.ties;
            document.getElementById('roundDisplay').textContent = gameState.round;
        }

        function addToHistory(roll1, roll2, result, cssClass) {
            const historyList = document.getElementById('historyList');
            
            if (historyList.children[0] && historyList.children[0].textContent.includes('No battles')) {
                historyList.innerHTML = '';
            }

            const item = document.createElement('div');
            item.className = `history-item ${cssClass}`;
            item.innerHTML = `
                <span>Round ${gameState.round}: ${roll1} vs ${roll2}</span>
                <span>${result}</span>
            `;
            historyList.insertBefore(item, historyList.firstChild);

                        if (historyList.children.length > 10) {
                historyList.removeChild(historyList.lastChild);
            }
        }

        function checkGameOver() {
            let roundsNeeded = 5;
            if (gameState.mode === 'bestOf3') roundsNeeded = 3;
            else if (gameState.mode === 'bestOf7') roundsNeeded = 7;

            const requiredWins = Math.ceil(roundsNeeded / 2);
            let winner = '';

            if (gameState.p1Wins === requiredWins) {
                winner = document.getElementById('player1Name').textContent;
            } else if (gameState.p2Wins === requiredWins) {
                winner = document.getElementById('player2Name').textContent;
            }

            if (winner) {
                setTimeout(() => {
                    showFinalResult(winner);
                }, 500);
                return true;
            }

            // If all rounds done, but no clear winner (tie case)
            if (gameState.round > roundsNeeded) {
                let finalMsg = '';
                if (gameState.p1Wins > gameState.p2Wins)
                    finalMsg = document.getElementById('player1Name').textContent + ' wins the match!';
                else if (gameState.p2Wins > gameState.p1Wins)
                    finalMsg = document.getElementById('player2Name').textContent + ' wins the match!';
                else
                    finalMsg = "It's a draw!";

                setTimeout(() => {
                    showFinalResult(finalMsg);
                }, 500);
                return true;
            }
            return false;
        }

        function showFinalResult(message) {
            const resultOverlay = document.getElementById('finalResult');
            const resultText = document.getElementById('finalMessage');
            resultText.textContent = message;
            resultOverlay.classList.add('show');
        }

        function resetGame() {
            gameState = {
                score1: 0,
                score2: 0,
                round: 1,
                p1Wins: 0,
                p2Wins: 0,
                ties: 0,
                mode: gameState.mode,
                isRolling: false,
                history: []
            };

            document.getElementById('dice1').textContent = '⚀';
            document.getElementById('dice2').textContent = '⚀';
            document.getElementById('historyList').innerHTML = `<div class="history-item">No battles yet...</div>`;
            document.getElementById('finalResult').classList.remove('show');
            updateDisplay();

            const rollBtn = document.getElementById('rollBtn');
            rollBtn.disabled = false;
        }

        // Hook for Play Again button
        document.getElementById('playAgainBtn').addEventListener('click', resetGame);
