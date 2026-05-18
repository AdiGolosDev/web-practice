const choices = ["rock", "paper", "scissors"];
let humanScore = 0;
let computerScore = 0;

function getComputerChoice() {
    return choices[Math.floor(Math.random() * 3)];
    // Math.random() gives quasi-random floating point 0 - 1
    //Math.floor() rounds result to nearest whole number
}

function getHumanChoice() {
    let humanChoice = prompt("Please choose one of the following: rock, paper, scissors");
    return humanChoice?.toLowerCase().trim();
    //only call toLowerCase() if humanChoice is not null/undefined
}

function playRound(humanChoice, computerChoice) {
    if(humanChoice === computerChoice) {
        console.log("It's a tie!");
    }

    if((humanChoice === "rock" && computerChoice === "scissors") || 
    (humanChoice === "paper" && computerChoice === "rock") || 
    (humanChoice === "scissors" && computerChoice === "paper")) {
        console.log("You win! \n" + humanChoice + " beats " + computerChoice);
        humanScore++;
    } else {
        console.log("You lose! \n" + computerChoice + " beats " + humanChoice);
        computerScore++;
    }
}

function resetScore() {
    humanScore = 0;
    computerScore = 0;
}

function playGame() {
    resetScore();
    for (let index = 0; index < 5; index++) {
       playRound(getHumanChoice(), getComputerChoice());
    }
    
    if(humanScore === computerScore) {
        console.log("The game ends in a Draw!");
    }

    if(humanScore > computerScore) {
        console.log("You won the Game!");
    } else {
        console.log("You lost the game...");
    }

    console.log("Final score:\n" + "HumanScore: " + humanScore + "\nComputerScore: " + computerScore);
    
    resetScore();
}

playGame();