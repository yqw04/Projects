const RPSchoices = ["rock", "paper", "scissors"];
const RPSplayerDisplay = document.getElementById("RPSplayerDisplay");
const RPScomputerDisplay = document.getElementById("RPScomputerDisplay");
const playerEmoji = document.getElementById("playerEmoji");
const computerEmoji = document.getElementById("computerEmoji");
const RPSresultDisplay = document.getElementById("RPSresultDisplay");
const RPSplayerScoreDisplay = document.getElementById("RPSplayerScoreDisplay");
const RPScomputerScoreDisplay = document.getElementById("RPScomputerScoreDisplay");
let playAgainButton = document.getElementById("RPSplay-again");
let playerScore = 0;
let computerScore = 0;

function playGame(playerChoice) {
    const computerChoice = RPSchoices[Math.floor(Math.random() * 3)];
    let result = "";

    const emojiMap = {
        rock: '👊',
        paper: '✋',
        scissors: '✌️'
    };

    if (playerChoice === computerChoice) {
        result = "It's a Tie";
    } else {
        switch (playerChoice) {
            case "rock":
                result = (computerChoice === "scissors") ? "You win" : "You lose";
                break;
            case "paper":
                result = (computerChoice === "rock") ? "You win" : "You lose";
                break;
            case "scissors":
                result = (computerChoice === "paper") ? "You win" : "You lose";
                break;
        }
    }

    RPSplayerDisplay.innerHTML = `PLAYER: <span id="playerEmoji">${emojiMap[playerChoice]}</span>`;
    RPScomputerDisplay.innerHTML = `COMPUTER: <span id="computerEmoji">${emojiMap[computerChoice]}</span>`;
    RPSresultDisplay.textContent = result;

    RPSresultDisplay.classList.remove("greenText", "redText");
    switch (result) {
        case "You win":
            RPSresultDisplay.classList.add("greenText");
            playerScore++;
            RPSplayerScoreDisplay.textContent = playerScore;
            break;
        case "You lose":
            RPSresultDisplay.classList.add("redText");
            computerScore++;
            RPScomputerScoreDisplay.textContent = computerScore;
            break;
    }
    playAgainButton.style.display = "block";
}

function restartGame() {
    RPSplayerScoreDisplay.textContent = 0;
    RPScomputerScoreDisplay.textContent = 0;
    RPSresultDisplay.textContent = "";
    RPSplayerDisplay.innerHTML = 'PLAYER: <span id="playerEmoji"></span>';
    RPScomputerDisplay.innerHTML = 'COMPUTER: <span id="computerEmoji"></span>';
}
