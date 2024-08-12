const wordList = [
    "cat", "dog", "bat", "pen", "cup", "car", "sun", "box", "run", "hat",
    "tree", "book", "lamp", "fish", "home", "milk", "wolf", "fire", "moon", "frog",
    "apple", "chair", "river", "cloud", "beach", "grape", "bread", "dance", "heart",
    "music", "banana", "window", "yellow", "garden", "laptop", "rocket", "purple",
    "winter", "circle", "silver"
];

let filteredWords;
let randomWord;
let gameSection = document.getElementById("GTW-game-section");
let feedback = document.getElementById("GTW-feedback");
let guessHistory = document.getElementById("GTW-guess-history");
let playAgainButton = document.getElementById("GTW-play-again");
let giveUpMessage = document.getElementById("give-up-message");

function startGame() {
    let numLetters = parseInt(document.getElementById("GTW-num-letters").value);

    if (isNaN(numLetters) || ![3, 4, 5, 6].includes(numLetters)) {
        alert("Please enter a valid number of letters (3, 4, 5, or 6).");
        return;
    }

    filteredWords = wordList.filter(word => word.length === numLetters);

    if (filteredWords.length === 0) {
        alert("No words found with the specified length. Please try again.");
        return;
    }

    randomWord = filteredWords[Math.floor(Math.random() * filteredWords.length)];
    gameSection.style.display = "block";
    playAgainButton.style.display = "none";
    feedback.innerHTML = "";
    guessHistory.innerHTML = "";
    giveUpMessage.style.display = "block";
}

function makeGuess() {
    let userGuess = document.getElementById("GTW-user-guess").value.toLowerCase();

    if (userGuess === "give up") {
        feedback.textContent = `You gave up! The correct word was "${randomWord}".`;
        feedback.classList.remove("correct", "incorrect", "present");
        playAgainButton.style.display = "block";
        giveUpMessage.style.display = "none";
        return;
    }

    if (userGuess === randomWord) {
        feedback.textContent = `You got it! The word was "${randomWord}".`;
        feedback.classList.add("correct");
        feedback.classList.remove("incorrect", "present");
        playAgainButton.style.display = "block";
        giveUpMessage.style.display = "none";
    } else {
        let feedbackText = '';
        let historyText = '';
        for (let i = 0; i < randomWord.length; i++) {
            if (userGuess[i] === randomWord[i]) {
                feedbackText += `<span class="GTW-correct">${userGuess[i]}</span>`;
                historyText += `<span class="GTW-correct">${userGuess[i]}</span>`;
            } else if (randomWord.includes(userGuess[i])) {
                feedbackText += `<span class="GTW-present">${userGuess[i]}</span>`;
                historyText += `<span class="GTW-present">${userGuess[i]}</span>`;
            } else {
                feedbackText += `<span class="GTW-incorrect">_</span>`;
                historyText += `<span class="GTW-incorrect">${userGuess[i]}</span>`;
            }
            document.getElementById("GTW-user-guess").value = "";

        }
        feedback.innerHTML = feedbackText;
        guessHistory.innerHTML += `<p>${historyText}</p>`;
    }
}

function restartGame() {
    document.getElementById("GTW-num-letters").value = "";
    document.getElementById("GTW-user-guess").value = "";
    gameSection.style.display = "none";
    playAgainButton.style.display = "none";
    feedback.innerHTML = "";
    guessHistory.innerHTML = "";
    giveUpMessage.style.display = "none";
}
