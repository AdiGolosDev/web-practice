function add(a, b) {
    return a + b;
}

function subtract(a, b) {
    return a - b;
}

function multiply(a, b) {
    return a * b;
}

function divide(a, b) {
    if (b === 0) {
        throw new Error("Cannot divide by zero");
    }
    return a / b;
}

function operate(operator, a, b) {
    switch (operator) {
        case '+':
            return add(a, b);
        case '-':
            return subtract(a, b);
        case '*':
            return multiply(a, b);
        case '/':
            return divide(a, b);
        default:
            throw new Error("Invalid operator");
    }
}

let a, b = null;
let operator, currentInput = '';

const display = document.querySelector('.display');

document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', () => {
        const value = button.textContent;

        if (!isNaN(value) || value === '.') {
            currentInput += value;
            display.textContent = currentInput;
        } else if (['+', '-', '*', '/'].includes(value)) {
            a = parseFloat(currentInput);
            operator = value;
            currentInput = '';
        } else if (value === '=') {
            b = parseFloat(currentInput);
            const result = operate(operator, a, b);
            display.textContent = result;
            currentInput = String(result);
            a = null;
            operator = '';
        }
    });

});

document.querySelector('.clear').addEventListener('click', () => {
    a = null;
    b = null;
    operator = '';
    currentInput = '';
    display.textContent = '0';
});
