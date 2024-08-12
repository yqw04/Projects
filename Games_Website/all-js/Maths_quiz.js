let numberOne;
let numberTwo;
let solution;
let gameSection = document.getElementById("MathsQ-game-section");
let problemText = document.getElementById("problem");
let feedback = document.getElementById("feedback");
let submitButton = document.getElementById("submit-button");
let playAgainButton = document.getElementById("MathsQ-play-again");
let tryAgainButton = document.getElementById("MathsQ-try-again");
let exitButton = document.getElementById("MathsQ-exit");
let userAnswerInput = document.getElementById("user-answer");

function startGame() {
    let startRange = parseInt(document.getElementById("MathsQ-start-range").value);
    let endRange = parseInt(document.getElementById("MathsQ-end-range").value);
    let questionType = document.getElementById("MathsQ-question-type").value;

    if (isNaN(startRange) || isNaN(endRange) || startRange >= endRange) {
        alert("Please enter valid numbers for the range.");
        return;
    }

    numberOne = Math.floor(Math.random() * (endRange - startRange + 1)) + startRange;
    numberTwo = Math.floor(Math.random() * (endRange - startRange + 1)) + startRange;

    switch (questionType) {
        case "Addition":
            problemText.textContent = `${numberOne} + ${numberTwo} = `;
            solution = numberOne + numberTwo;
            break;
        case "Subtraction":
            problemText.textContent = `${numberOne} - ${numberTwo} = `;
            solution = numberOne - numberTwo;
            break;
        case "Division":
            problemText.textContent = `${numberOne} / ${numberTwo} = `;
            solution = numberOne / numberTwo;
            break;
        case "Multiplication":
            problemText.textContent = `${numberOne} * ${numberTwo} = `;
            solution = numberOne * numberTwo;
            break;
        default:
            alert("Invalid option. Please choose Addition, Subtraction, Division, or Multiplication.");
            return;
    }

    gameSection.style.display = "block";
    playAgainButton.style.display = "none";
    tryAgainButton.style.display = "none";
    exitButton.style.display = "none";
    feedback.textContent = "";
    submitButton.style.display = "inline";
    userAnswerInput.disabled = false;
    userAnswerInput.value = "";
}

function submitAnswer() {
    let userAnswer = parseFloat(userAnswerInput.value);

    if (isNaN(userAnswer)) {
        feedback.textContent = "Invalid input. Please enter a valid number.";
        return;
    }

    if (userAnswer === solution) {
        feedback.textContent = "Correct!";
        submitButton.style.display = "none";
        playAgainButton.style.display = "block";
        userAnswerInput.disabled = true;
    } else {
        feedback.textContent = `Incorrect, try again or exit?`;
        tryAgainButton.style.display = "block";
        exitButton.style.display = "block";
        userAnswerInput.disabled = true;
    }
}

function tryAgain() {
    userAnswerInput.value = "";
    feedback.textContent = "";
    tryAgainButton.style.display = "none";
    exitButton.style.display = "none";
    userAnswerInput.disabled = false;
}

function restartGame() {
    document.getElementById("MathsQ-start-range").value = "";
    document.getElementById("MathsQ-end-range").value = "";
    userAnswerInput.value = "";
    gameSection.style.display = "none";
    playAgainButton.style.display = "none";
    feedback.textContent = "";
    tryAgainButton.style.display = "none";
    exitButton.style.display = "none";
    submitButton.style.display = "inline";
    userAnswerInput.disabled = false;
}
