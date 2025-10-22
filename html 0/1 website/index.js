

    draw() {
        this.context.fillStyle = 'black';
        this.context.fillRect(0, 0, this.canvas.width, this.canvas.height);

        this.context.fillStyle = 'red';
        this.context.font = '30px Poppins';
        this.context.fillText(this.tailSize - 5, 20, 40);

        this.context.fillStyle = 'green';
        this.trail.forEach(t => {
            this.context.fillRect(t.positionX * this.gridSize, t.positionY * this.gridSize, this.gridSize - 2, this.gridSize - 2);
        });

        this.context.fillStyle = 'pink';
        this.context.fillRect(this.appleX * this.gridSize, this.appleY * this.gridSize, this.gridSize - 2, this.gridSize - 2);
    }

    onKeyPress(e) {
        if (e.keyCode === 37 && this.velocityX !== 1) {
            this.velocityX = -1;
            this.velocityY = 0;
        }
        if (e.keyCode === 38 && this.velocityY !== 1) {
            this.velocityX = 0;
            this.velocityY = -1;
        }
        if (e.keyCode === 39 && this.velocityX !== -1) {
            this.velocityX = 1;
            this.velocityY = 0;
        }
        if (e.keyCode === 40 && this.velocityY !== -1) {
            this.velocityX = 0;
            this.velocityY = 1;
        }
    }
}

const game = new SnakeGame();
window.onload = () => game.init();
