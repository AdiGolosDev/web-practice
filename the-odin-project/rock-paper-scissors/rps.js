const choices = ["rock", "paper", "scissors"];

function getComputerChoice() {
    return choices[Math.floor(Math.random() * 3)];
    // Math.random() gives quasi-random floating point 0 - 1
    //Math.floor() rounds result to nearest whole number
}

function getHumanChoice() {
    let humanChoice = prompt("Please choose one of the following: rock, paper, scissors");
    return humanChoice?.toLowerCase().trim();
}

console.log(getHumanChoice());