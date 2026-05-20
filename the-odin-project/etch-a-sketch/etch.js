const container = document.getElementById('container');

function createGrid(size) {
    for(let i = 0; i < size; i++) {
        for(let j = 0; j < size; j++) {
            const gridSquare = document.createElement('div');
            gridSquare.style.width = 960/size + 'px';
            gridSquare.style.height = 960/size + 'px';
            gridSquare.classList.add('grid-square');
            gridSquare.addEventListener('mouseover', () => {
                gridSquare.style.backgroundColor = 'black';
            });
            container.appendChild(gridSquare);
        }
    }
}

createGrid(16);

const resetButton = document.getElementById('reset-button');
resetButton.addEventListener('click', () => {
    container.replaceChildren();
    createGrid(16);
})

const changeGridSizeButton = document.getElementById('change-grid-size');
changeGridSizeButton.addEventListener('click', () => {
    let newSize = Number(prompt('Please enter a new grid size: eg: 16 for a 16x16 grid(default)')) || 16;
    if (newSize > 100) {
        newSize = 100;
        alert('Grid size cannot be larger than 100. Setting grid size to 100...');
    } else if (newSize < 1) {
        newSize = 1;
        alert('Grid size cannot be smaller than 1. Setting grid size to 1...');
    }
    container.replaceChildren();
    createGrid(newSize);
})