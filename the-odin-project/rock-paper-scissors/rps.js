const choices = ["rock", "paper", "scissors"];
let humanScore = 0;
let computerScore = 0;

const resultDiv = document.getElementById("result");
const humanScoreSpan = document.getElementById("human-score");
const computerScoreSpan = document.getElementById("computer-score");
const winnerDiv = document.getElementById("winner");
const buttons = document.querySelectorAll("#buttons button");

function getComputerChoice() {
    return choices[Math.floor(Math.random() * 3)];
    // Math.random() gives quasi-random floating point 0 - 1
    //Math.floor() rounds result to nearest whole number
}

function updateScoreDisplay() {
    humanScoreSpan.textContent = "Your Score: " + humanScore;
    computerScoreSpan.textContent = "Computer's Score: " + computerScore;
}

function playRound(humanChoice, computerChoice) {
    let message = "";

    if(humanChoice === computerChoice) {
        message = "It's a tie! Both chose " + humanChoice + ".";
    } else if(
        (humanChoice === "rock" && computerChoice === "scissors") || 
        (humanChoice === "paper" && computerChoice === "rock") || 
        (humanChoice === "scissors" && computerChoice === "paper")) {
            message = "You win! " + humanChoice + " beats " + computerChoice + ".";
            humanScore++;
    } else {
        message = "You lose! " + computerChoice + " beats " + humanChoice + ".";
        computerScore++;
    }
    resultDiv.textContent = message;
    updateScoreDisplay();
    checkWinner();
}

function checkWinner() {
    if (humanScore === 5) {
        winnerDiv.textContent = "You won the game!";
        disableButtons();
    }else if (computerScore === 5) {
        winnerDiv.textContent = "You lost the game...";
        disableButtons();
    }
}

function disableButtons() {
    buttons.forEach(button => button.disabled = true);
}

function resetGame() {
    humanScore = 0;
    computerScore = 0;
    updateScoreDisplay();
    resultDiv.textContent = "Please choose rock, paper, or scissors!";
    winnerDiv.textContent = "";
    buttons.forEach(button => button.disabled = false);
}

document.getElementById("reset").addEventListener("click", resetGame);

buttons.forEach((button) => {
    button.addEventListener("click", () => {
        const humanChoice = button.dataset.choice;
        playRound(humanChoice, getComputerChoice());
    });
}); 