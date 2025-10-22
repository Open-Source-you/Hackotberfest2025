
let board, context;
const boardWidth = 360, boardHeight = 640;
const birdWidth = 34, birdHeight = 24;
let birdX = boardHeight/8, birdY = boardHeight/2;
let birdImg;
const bird = { x: birdX, y: birdY, width: birdWidth, height: birdHeight };
let pipeArray = [];
const pipeWidth = 64, pipeHeight = 512;
let pipeX = boardWidth, pipeY = 0;
let topPipeImg, bottomPipeImg;
let velocityX = -2, velocityY = 0, gravity = 0.4;
let gameOver = false, score = 0;
window.onload = function(){
    board = document.getElementById("board");
    board.height = boardHeight;
    board.width = boardWidth;
    context = board.getContext("2d");

    //context.fillStyle = "green";
    //context.fillRect(bird.x, bird.y, bird.width, bird.height);

    birdImg = new Image();
    birdImg.src = "./Images/flappybird.png";
    birdImg.onload = function(){
        context.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height);
    }
    topPipeImg = new Image();
    topPipeImg.src = "./Images/toppipe.png";
    bottomPipeImg = new Image();
    bottomPipeImg.src = "./Images/bottompipe.png";
    requestAnimationFrame(update);
    setInterval(placePipes, 1500);
    document.addEventListener("keydown", moveBird);
}

function update(){
    requestAnimationFrame(update);
    if(gameOver){
        return;
    }
    context.clearRect(0, 0, board.width, board.height);
    velocityY += gravity;
    bird.y = Math.max(bird.y + velocityY, 0);
    context.drawImage(birdImg, bird.x, bird.y, bird.width, bird.height);

    if(bird.y > board.height){
        gameOver = true;
    }

    for(let i = 0; i<pipeArray.length; i++){
        let pipe = pipeArray[i];
        pipe.x += velocityX;
        context.drawImage(pipe.img, pipe.x, pipe.y, pipe.width, pipe.height)

        if(!pipe.passed && bird.x > pipe.x + pipe.width){
            score += 0.5;
            pipe.passed = true;
        }

        if(detectCollision(bird, pipe)){
            gameOver = true;
        }
    }
    while(pipeArray.length > 0 && pipeArray[0].x < -pipeWidth){
        pipeArray.shift();
    }

    context.fillStyle = "white";
    context.font = "45px sans-serif";
    context.fillText(score, 5, 45);

    if(gameOver){
        context.fillText("GAME OVER", 5, 90);
    }
}

function placePipes(){
    if(gameOver){
        return;
    }
    let randomPipeY = pipeY - pipeHeight/4 - Math.random()*(pipeHeight/2);
    let openingSpace = board.height/4;
    let topPipe = {
        img : topPipeImg,
        x : pipeX,
        y : randomPipeY,
        width : pipeWidth,
        height : pipeHeight,
        passed : false
    }
    pipeArray.push(topPipe);

    let bottompPipe = {
        img : bottomPipeImg,
        x : pipeX,
        y : randomPipeY + pipeHeight + openingSpace,
        width : pipeWidth,
        height : pipeHeight,
        passed : false
    }
    pipeArray.push(bottompPipe);
}

function moveBird(e){
    if(e.code == "space" || e.code == "ArrowUp" || e.code == "keyX"){
        velocityY = -6;
        if(gameOver){
            bird.y = birdY;
            pipeArray = [];
            score = 0;
            gameOver = false;
        }
    }
}

function detectCollision(a, b){
    return a.x < b.x + b.width &&
           a.x + a.width > b.x &&
           a.y < b.y + b.height &&
           a.y + a.height > b.y;
}
