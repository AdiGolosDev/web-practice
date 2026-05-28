function add(a, b) { return a + b;}

function subtract(a, b) { return a - b; }

function multiply(a, b) { return a * b; }

function divide(a, b) {
    if (b === 0) return null;
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

function roundResult(num) {
    return parseFloat(num.toPrecision(8)); //rounds to 7 (lucky number)
}

function newDigit(digit) {
    if (justCalculated) {
        operator = '';
        currentInput = '';
        a = null;
        justCalculated = false;
    }
    if (digit === '.' && currentInput.includes('.')) return;
    if (digit === '0' && currentInput === '0') return;

    currentInput += digit;
    display.textContent = currentInput;
}

function newOperator(op) {
    justCalculated = false;

    if (currentInput === '' && a === null) return;

    if (currentInput === '' && a !== null) {
        operator = op;
        return;
    }

    if (a !== null && currentInput !== '') {
        const result = operate(operator, a, parseFloat(currentInput));

        if (result === null) {
            display.textContent = "Nuh-uh!";
            a = null;
            operator = '';
            currentInput = '';
            justCalculated = false;
            return;
        }

        a = roundResult(result);
        display.textContent = a;
        currentInput = '';
    } else {
        a = parseFloat(currentInput);
        currentInput = '';
    }
    operator = op;
}

function newEquals() {
    if (a === null || operator === '' || currentInput === '') return;
    
    const result = operate(operator, a, parseFloat(currentInput));

    if (result === null) {
        display.textContent = "Nuh-uh!";
        a = null;
        operator = '';
        currentInput = '';
        justCalculated = false;
        return;
    }

    a = roundResult(result);
    operator = '';
    currentInput = '';
    justCalculated = true;
    display.textContent = a;
}

function clear() {
    a = null;
    operator = '';
    currentInput = '';
    justCalculated = false;
    display.textContent = '0';
}

let a = null;
let b = null;
let operator = '';
let currentInput = '';
let justCalculated = false;

const display = document.querySelector('.display');

document.querySelectorAll('.btn').forEach(button => {
    button.addEventListener('click', () => {
        const value = button.textContent;

        if (!isNaN(value) || value === '.') {
            newDigit(value);
        } else if (['+', '-', '*', '/'].includes(value)) {
            newOperator(value);
        } else if (value === '=') {
            newEquals();
        }
    });
});

document.querySelector('.clear').addEventListener('click', clear);