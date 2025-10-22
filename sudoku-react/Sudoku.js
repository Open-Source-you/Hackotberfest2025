// Advanced Sudoku Game in JavaScript (Console-based)

const SIZE = 9;
let mistakes = 0;
let startTime = Date.now();

// Generate an empty 9x9 board
function createEmptyBoard() {
    return Array.from({ length: SIZE }, () => Array(SIZE).fill(0));
}

// Sample puzzle generator (simplified random removal)
function generatePuzzle() {
    let board = createEmptyBoard();

    // Fill diagonal 3x3 blocks
    for (let k = 0; k < SIZE; k += 3) {
        fillDiagonalBlock(board, k, k);
    }

    solveSudoku(board); // Fill full solution
    removeNumbers(board, 40); // Remove 40 numbers to make puzzle
    return board;
}

// Fill diagonal 3x3 block randomly
function fillDiagonalBlock(board, row, col) {
    let nums = shuffleArray([...Array(SIZE).keys()].map(n => n + 1));
    for (let i = 0; i < 3; i++)
        for (let j = 0; j < 3; j++)
            board[row + i][col + j] = nums[i * 3 + j];
}

// Shuffle array
function shuffleArray(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}

// Remove 'count' numbers randomly for puzzle
function removeNumbers(board, count) {
    while (count > 0) {
        let i = Math.floor(Math.random() * SIZE);
        let j = Math.floor(Math.random() * SIZE);
        if (board[i][j] !== 0) {
            board[i][j] = 0;
            count--;
        }
    }
}

// Print board
function printBoard(board) {
    console.clear();
    console.log(`Mistakes: ${mistakes} | Time: ${Math.floor((Date.now() - startTime)/1000)}s`);
    for (let i = 0; i < SIZE; i++) {
        let row = '';
        for (let j = 0; j < SIZE; j++) {
            row += board[i][j] === 0 ? '.' : board[i][j];
            row += ' ';
            if ((j + 1) % 3 === 0 && j < SIZE - 1) row += '| ';
        }
        console.log(row);
        if ((i + 1) % 3 === 0 && i < SIZE - 1) console.log('------+-------+------');
    }
}

// Check if placing num at board[row][col] is valid
function isValid(board, row, col, num) {
    for (let x = 0; x < SIZE; x++)
        if (board[row][x] === num || board[x][col] === num) return false;

    let startRow = row - (row % 3), startCol = col - (col % 3);
    for (let i = 0; i < 3; i++)
        for (let j = 0; j < 3; j++)
            if (board[startRow + i][startCol + j] === num) return false;

    return true;
}

// Solve Sudoku (Backtracking)
function solveSudoku(board) {
    for (let row = 0; row < SIZE; row++) {
        for (let col = 0; col < SIZE; col++) {
            if (board[row][col] === 0) {
                for (let num = 1; num <= SIZE; num++) {
                    if (isValid(board, row, col, num)) {
                        board[row][col] = num;
                        if (solveSudoku(board)) return true;
                        board[row][col] = 0;
                    }
                }
                return false;
            }
        }
    }
    return true;
}

// Provide hints (list possible numbers for empty cells)
function getHints(board, row, col) {
    let hints = [];
    for (let num = 1; num <= SIZE; num++)
        if (isValid(board, row, col, num)) hints.push(num);
    return hints;
}

// Main Game Loop
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

let puzzle = generatePuzzle();

function play() {
    printBoard(puzzle);
    readline.question('Enter row(0-8), col(0-8), num(1-9) separated by space (or "hint r c"): ', input => {
        const parts = input.trim().split(' ');

        if (parts[0] === 'hint' && parts.length === 3) {
            let r = parseInt(parts[1]), c = parseInt(parts[2]);
            console.log(`Hints for (${r},${c}): ${getHints(puzzle, r, c).join(', ')}`);
            return play();
        }

        if (parts.length !== 3) return play();

        let row = parseInt(parts[0]), col = parseInt(parts[1]), num = parseInt(parts[2]);

        if (isNaN(row) || isNaN(col) || isNaN(num) || row < 0 || row >= SIZE || col < 0 || col >= SIZE || num < 1 || num > 9) {
            console.log("Invalid input!");
            return play();
        }

        if (puzzle[row][col] !== 0) {
            console.log("Cell already filled!");
            return play();
        }

        if (isValid(puzzle, row, col, num)) {
            puzzle[row][col] = num;
        } else {
            console.log("Wrong number!");
            mistakes++;
        }

        if (puzzle.flat().every(n => n !== 0)) {
            printBoard(puzzle);
            console.log(`Congratulations! You solved the Sudoku in ${Math.floor((Date.now() - startTime)/1000)} seconds with ${mistakes} mistakes.`);
            readline.close();
        } else {
            play();
        }
    });
}

play();
