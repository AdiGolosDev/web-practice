const container = document.getElementById('container');

function generateRandomN(number) {
    return Math.floor(Math.random() * number);
}

function createGrid(size) {
    for(let i = 0; i < size; i++) {
        for(let j = 0; j < size; j++) {
            const gridSquare = document.createElement('div');
            gridSquare.style.width = 960/size + 'px';
            gridSquare.style.height = 960/size + 'px';
            gridSquare.classList.add('grid-square');
            gridSquare.addEventListener('mouseover', () => {
                let hoverCount = parseInt(gridSquare.dataset.hoverCount ?? '0');

                if (hoverCount > 9) return;

                if(hoverCount === 0) {
                    gridSquare.dataset.hue = generateRandomN(360);
                    gridSquare.dataset.saturation = generateRandomN(100);
                    gridSquare.dataset.lightness = 50;
                }
                
                hoverCount++;
                gridSquare.dataset.hoverCount = hoverCount;

                gridSquare.style.backgroundColor = `hsl(${gridSquare.dataset.hue}, ${gridSquare.dataset.saturation}%, ${gridSquare.dataset.lightness - (5 * hoverCount)}%)`;

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
