let numberToGuess;
let gameSection = document.getElementById("GTN-game-section");
let feedback = document.getElementById("GTN-feedback");
let playAgainButton = document.getElementById("GTN-play-again");

function startGame() {
    let startRange = parseInt(document.getElementById("GTN-start-range").value);
    let endRange = parseInt(document.getElementById("GTN-end-range").value);

    if (isNaN(startRange) || isNaN(endRange) || startRange >= endRange) {
        alert("Please enter valid numbers for the range.");
        return;
    }

    numberToGuess = Math.floor(Math.random() * (endRange - startRange + 1)) + startRange;
    gameSection.style.display = "block";
    playAgainButton.style.display = "none";
    feedback.textContent = "";
}

function makeGuess() {
    let userGuess = parseInt(document.getElementById("GTN-user-guess").value);

    if (isNaN(userGuess)) {
        feedback.textContent = "Invalid input. Please enter a valid number.";
        return;
    }

    if (userGuess === numberToGuess) {
        feedback.textContent = "You got it!";
        playAgainButton.style.display = "block";
    } else if (userGuess > numberToGuess) {
        feedback.textContent = "The number is Lower than " + document.getElementById("GTN-user-guess").value;
        document.getElementById("GTN-user-guess").value = "";
    } else {
        feedback.textContent = "The number is Higher than " + document.getElementById("GTN-user-guess").value;
        document.getElementById("GTN-user-guess").value = "";
    }
}

function restartGame() {
    document.getElementById("GTN-start-range").value = "";
    document.getElementById("GTN-end-range").value = "";
    document.getElementById("GTN-user-guess").value = "";
    gameSection.style.display = "none";
    playAgainButton.style.display = "none";
    feedback.textContent = "";
}