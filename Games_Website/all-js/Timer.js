document.addEventListener('DOMContentLoaded', (event) => {
    let targetTime;
    let acceptableRange;
    let currentTime = 0.00;
    let timerInterval;
    const currentTimeDisplay = document.getElementById('timer-currentTime');
    const startButton = document.getElementById('timer-startButton');
    const stopButton = document.getElementById('timer-stopButton');
    const backButton = document.getElementById('timer-backButton');
    const difficultyButtons = document.querySelectorAll('.timer-difficulty-button'); 
    const difficultySelection = document.getElementById('timer-difficulty-selection');
    const gameSection = document.querySelector('.timer-game-section');
    const feedback = document.getElementById('timer-feedback');
    const restartBtn = document.querySelector("#timer-restartButton");
    const targetTimeDisplay = document.querySelector('.timer-target-time');

    difficultyButtons.forEach(button => {
        const proceedButton = button.querySelector('.timer-proceedButton'); // Get the specific proceed button for this difficulty
        button.addEventListener('click', (event) => {
            event.stopPropagation(); // Prevent event from propagating to document
            difficultyButtons.forEach(btn => {
                btn.classList.remove('active');
                btn.querySelector('.timer-difficulty-info').classList.remove('visible');
            });
            selectedDifficulty = event.currentTarget.dataset.difficulty;
            showDifficultyInfo(selectedDifficulty, event.currentTarget);
            proceedButton.classList.remove('timer-hidden');
        });

        proceedButton.addEventListener('click', () => {
            startGame(); // Start the game when the specific proceed button is clicked
        });
    });

    // Listen for clicks outside the active difficulty button
    document.addEventListener('click', (event) => {
        if (!event.target.closest('.difficulty-button')) {
            difficultyButtons.forEach(button => {
                button.classList.remove('active');
                button.querySelector('.timer-difficulty-info').classList.remove('visible');
                button.querySelector('.timer-proceedButton').classList.add('timer-hidden'); // Hide the proceed button when clicking outside
            });
        }
    });

    startButton.addEventListener('click', startTimer);
    stopButton.addEventListener('click', stopTimer);
    backButton.addEventListener('click', goBack);
    restartBtn.addEventListener("click", restartGame);

    function showDifficultyInfo(difficulty, button) {
        const descriptionElement = button.querySelector('.timer-difficulty-info');
        descriptionElement.classList.add('visible');
        button.classList.add('active');
        // Set acceptable range based on difficulty
        switch (difficulty) {
            case 'easy':
                acceptableRange = 1.00; // +/- 1 second
                break;
            case 'medium':
                acceptableRange = 0.50; // +/- 0.5 seconds
                break;
            case 'hard':
                acceptableRange = 0.25; // +/- 0.25 seconds
                break;
            case 'extreme':
                acceptableRange = 0.10; // +/- 0.10 seconds
                break;
        }
    }

    function startGame() {
        targetTime = Math.floor(Math.random() * (6 - 3 + 1)) + 3; // Generate random target time between 7 and 30
        targetTimeDisplay.textContent = targetTime.toFixed(2);
        
        difficultySelection.classList.add('timer-hidden');
        gameSection.classList.remove('timer-hidden');
    }

    function startTimer() {
        startButton.disabled = true;
        stopButton.disabled = false;
        currentTime = 0;
        currentTimeDisplay.style.opacity = 1;
        currentTimeDisplay.textContent = currentTime.toFixed(2);
        timerInterval = setInterval(() => {
            currentTime += 0.01;
            currentTimeDisplay.textContent = currentTime.toFixed(2);
            if (currentTime >= 5.00) {
                currentTimeDisplay.style.opacity = 0;
            }
        }, 10);
    }

    function stopTimer() {
        clearInterval(timerInterval);
        currentTimeDisplay.style.opacity = 1;
        startButton.disabled = false;
        stopButton.disabled = true;

        const lowerBound = targetTime - acceptableRange;
        const upperBound = targetTime + acceptableRange;

        if (currentTime >= lowerBound && currentTime <= upperBound) {
            feedback.textContent = `You win! You stopped the timer at ${currentTime.toFixed(2)} seconds! The target was ${targetTime.toFixed(2)} seconds.`;
        } else {
            feedback.textContent = `You lose! You stopped the timer at ${currentTime.toFixed(2)} seconds! The target was ${targetTime.toFixed(2)} seconds.`;
        }
    }

    function goBack() {
        gameSection.classList.add('timer-hidden');
        difficultySelection.classList.remove('timer-hidden');
    }

    function restartGame() {
        // Reset the game
        currentTimeDisplay.textContent = "0.00";
        feedback.textContent = "";
        startButton.disabled = false;
        stopButton.disabled = true;

        // Re-select difficulty if needed (optional)
        if (selectedDifficulty) {
            showDifficultyInfo(selectedDifficulty, document.querySelector(`.difficulty-button[data-difficulty="${selectedDifficulty}"]`));
        }

        // Generate a new target time and update the display
        targetTime = Math.floor(Math.random() * (6 - 3 + 1)) + 3; // Generate random target time between 7 and 30
        targetTimeDisplay.textContent = targetTime.toFixed(2);
    }
});