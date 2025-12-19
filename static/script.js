document.addEventListener('DOMContentLoaded', () => {
    const gridElement = document.getElementById('sudoku-grid');
    const generateBtn = document.getElementById('generate-btn');
    const solveBtn = document.getElementById('solve-btn');
    const statusText = document.getElementById('status-text');

    let cells = [];

    // Initialize Grid
    function createGrid() {
        gridElement.innerHTML = '';
        cells = [];
        for (let i = 0; i < 81; i++) {
            const cell = document.createElement('div');
            cell.classList.add('cell');

            const input = document.createElement('input');
            input.type = 'text';
            input.maxLength = 1;
            input.dataset.index = i;

            // Input validation
            input.addEventListener('input', (e) => {
                const val = e.target.value;
                if (!/^[1-9]$/.test(val)) {
                    e.target.value = '';
                }
            });

            cell.appendChild(input);
            gridElement.appendChild(cell);
            cells.push(input);
        }
    }

    // Generate a new puzzle from server
    async function generatePuzzle() {
        const difficulty = document.getElementById('difficulty-select').value;
        statusText.textContent = `Generating ${difficulty} puzzle...`;
        try {
            const response = await fetch(`/api/generate?difficulty=${difficulty}`);
            const data = await response.json();
            const puzzle = data.grid;

            resetGrid();

            cells.forEach((input, index) => {
                const row = Math.floor(index / 9);
                const col = index % 9;
                const val = puzzle[row][col];
                if (val !== 0) {
                    input.value = val;
                    input.disabled = true;
                    input.parentElement.classList.add('fixed');
                }
            });
            statusText.textContent = "New puzzle generated.";
        } catch (error) {
            console.error(error);
            statusText.textContent = "Error generating puzzle.";
        }
    }

    function resetGrid() {
        cells.forEach(cell => {
            cell.value = '';
            cell.disabled = false;
            cell.parentElement.classList.remove('fixed');
        });
    }

    function getGridValues() {
        const grid = [];
        for (let i = 0; i < 9; i++) {
            const row = [];
            for (let j = 0; j < 9; j++) {
                const val = cells[i * 9 + j].value;
                row.push(val === '' ? 0 : parseInt(val));
            }
            grid.push(row);
        }
        return grid;
    }

    async function solveGame() {
        statusText.textContent = "Solving...";
        const grid = getGridValues();

        try {
            const response = await fetch('/api/solve', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ grid })
            });

            const data = await response.json();

            if (data.solved) {
                // Fill in the solved grid
                data.grid.forEach((row, i) => {
                    row.forEach((val, j) => {
                        const index = i * 9 + j;
                        cells[index].value = val;
                    });
                });
                statusText.textContent = "Solved!";
            } else {
                statusText.textContent = "No solution found.";
            }
        } catch (error) {
            console.error(error);
            statusText.textContent = "Error connecting to server.";
        }
    }

    // Event Listeners
    generateBtn.addEventListener('click', generatePuzzle);
    solveBtn.addEventListener('click', solveGame);

    // Init
    createGrid();
    generatePuzzle();
});
