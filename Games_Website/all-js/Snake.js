const gameBoard = document.querySelector("#snakegameBoard");
const ctx = gameBoard.getContext("2d");
const scoreText = document.querySelector("#snakescoreText");
const resetBtn = document.querySelector("#snakeresetBtn");
const backButton = document.querySelector("#snakebackButton");
const startScreen = document.querySelector("#snake-startScreen");
const gameContainer = document.querySelector("#snake-gameContainer");
const gameWidth = gameBoard.width;
const gameHeight = gameBoard.height;
const boardBackground = "white";
const snakeColor = "lightgreen";
const snakeBorder = "black";
const foodColor = "red";
const unitSize = 25;
const personalBestText = document.querySelector("#snake-personalBestText");
let personalBest = localStorage.getItem('personalBest') || 0;
let running = false;
let xVelocity = unitSize;
let yVelocity = 0;
let foodX;
let foodY;
let score = 0;
let snake = [
    {x:unitSize * 4, y:0},
    {x:unitSize * 3, y:0},
    {x:unitSize * 2, y:0},
    {x:unitSize, y:0},
    {x:0, y:0}
];

window.addEventListener("keydown", changeDirection);
resetBtn.addEventListener("click", resetGame);
backButton.addEventListener("click", goBack);

function gameStart() {
    startScreen.classList.add('snake-gameContainer');
    gameContainer.classList.remove('snake-gameContainer');
    running = true;
    score = 0;
    xVelocity = unitSize;
    yVelocity =0;

    const startY = gameHeight / 2;

    snake = [
        {x:unitSize * 4, y:startY},
        {x:unitSize * 3, y:startY},
        {x:unitSize * 2, y:startY},
        {x:unitSize, y:startY},
        {x:0, y:startY}
    ];
    scoreText.textContent = score;
    createFood();
    drawFood();
    nextTick();

    personalBestText.textContent = `Personal Best: ${personalBest}`;
}

function nextTick(){
    if (running) {
        setTimeout(()=> {
            clearBoard();
            drawFood();
            moveSnake();
            drawSnake();
            checkGameOver();
            nextTick();
        }, 75);
    }
    else {
        displayGameOver();
    }
}

function clearBoard(){
    ctx.fillStyle = boardBackground;
    ctx.fillRect(0, 0, gameWidth, gameHeight);
}

function createFood(){
    function randomFood(min, max) {
        const randNum = Math.round((Math.random() * (max - min) + min) / unitSize) * unitSize;
        return randNum;
    }
    foodX = randomFood(0, gameWidth - unitSize);
    foodY = randomFood(0, gameHeight - unitSize);
}

function drawFood(){
    ctx.fillStyle = foodColor;
    ctx.fillRect(foodX, foodY, unitSize, unitSize);
}

function moveSnake(){
    const head = {x: snake[0].x + xVelocity,
        y: snake[0].y + yVelocity};

    snake.unshift(head);
    //if food is eaten
    if(snake[0].x === foodX && snake[0].y === foodY){
        score++;
        scoreText.textContent = score;
        createFood();
    } else {
        snake.pop();
    }
}

function drawSnake(){
    ctx.fillStyle = snakeColor;
    ctx.strokeStyle = snakeBorder;
    snake.forEach(snakePart => {
        ctx.fillRect(snakePart.x, snakePart.y, unitSize, unitSize);
        ctx.strokeRect(snakePart.x, snakePart.y, unitSize, unitSize);
    });
}

function changeDirection(event){
    const keyPressed = event.keyCode;

    const LEFT = 37;
    const RIGHT = 39;
    const UP = 38;
    const DOWN = 40;

    const goingUp = (yVelocity === -unitSize);
    const goingDown = (yVelocity === unitSize);
    const goingRight = (xVelocity === unitSize);
    const goingLeft = (xVelocity === -unitSize);

    switch(true) {
        case(keyPressed === LEFT && !goingRight):
            xVelocity = -unitSize;
            yVelocity = 0;
            break;
        case(keyPressed === UP && !goingDown):
            xVelocity = 0;
            yVelocity = -unitSize;
            break;
        case(keyPressed === RIGHT && !goingLeft):
            xVelocity = unitSize;
            yVelocity = 0;
            break;
        case(keyPressed === DOWN && !goingUp):
            xVelocity = 0;
            yVelocity = unitSize;
            break;
    }
}

function checkGameOver(){
    switch(true) {
        case (snake[0].x < 0): //went over left border
        case (snake[0].x >= gameWidth): //went over right border
        case (snake[0].y < 0): //went over top border
        case (snake[0].y >= gameHeight): //went over bottom border
            running = false;
            break;
    }
    //if snake head touches body part
    for (let i = 1; i < snake.length; i++) { 
        if(snake[i].x === snake[0].x && snake[i].y === snake[0].y) {
            running = false;
        }
    }
}

function displayGameOver(){
    ctx.font = "50px MV Boli";
    ctx.fillStyle = "black";
    ctx.textAlign = "center";
    ctx.fillText("Game Over! ", gameWidth / 2, gameHeight / 2);
    running = false;
    updatePersonalBest();
}

function resetGame(){
    score = 0;
    xVelocity = unitSize;
    yVelocity = 0;
    snake = [
        {x:unitSize * 4, y:0},
        {x:unitSize * 3, y:0},
        {x:unitSize * 2, y:0},
        {x:unitSize, y:0},
        {x:0, y:0}
    ];
    gameStart();
}

function goBack() {
    startScreen.classList.remove('snake-gameContainer');
    gameContainer.classList.add('snake-gameContainer');
    running = false;
}

function updatePersonalBest() {
    if (score > personalBest) {
        personalBest = score;
        localStorage.setItem('personalBest', personalBest);
        personalBestText.textContent = `Personal Best: ${personalBest}`;
    }
}