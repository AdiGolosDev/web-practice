const choices = ["rock", "paper", "scissors"]

function getComputerChoice() {
    return choices[Math.floor(Math.random() * 3)]
    // Math.random() gives quasi-random floating point 0 - 1
    //Math.floor() rounds result to nearest whole number
}


