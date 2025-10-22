#include <iostream>
#include <vector>
#include <string>
#include <limits>

#ifdef _WIN32
#include <cstdlib>
#endif

using
bool isRunning = true;
vector<vector<char>> board(3, vector<char>(3, ' '));

// --- Helper Functions ---
void clearScreen() {
#ifdef _WIN32
    system("cls");
#else
    system("clear");
#endif
}

void lineBreak() {
    cout << "\n-----------------------------------------\n";
}

void pause() {
    cout << "\n(Press Enter to continue...)";
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
    cin.get();
}

// --- Game Logic ---
void drawBoard() {
    clearScreen();
    cout << "=============================\n";
    cout << "        TIC TAC TOE 🎮       \n";
    cout << "=============================\n\n";
    cout << "      1   2   3\n";
    for (int i = 0; i < 3; i++) {
        cout << "   " << i + 1 << " ";
        for (int j = 0; j < 3; j++) {
            cout << " " << board[i][j] << " ";
            if (j < 2) cout << "|";
        }
        cout << "\n";
        if (i < 2) cout << "     ---+---+---\n";
    }
    cout << "\n";
}

bool checkWin(char symbol) {
    for (int i = 0; i < 3; i++) {
        if (board[i][0] == symbol && board[i][1] == symbol && board[i][2] == symbol) return true;
        if (board[0][i] == symbol && board[1][i] == symbol && board[2][i] == symbol) return true;
    }
    if (board[0][0] == symbol && board[1][1] == symbol && board[2][2] == symbol) return true;
    if (board[0][2] == symbol && board[1][1] == symbol && board[2][0] == symbol) return true;
    return false;
}

bool checkDraw() {
    for (auto &row : board)
        for (auto cell : row)
            if (cell == ' ') return false;
    return true;
}

void resetBoard() {
    for (auto &row : board)
        for (auto &cell : row)
            cell = ' ';
}

void playGame(string player1, string player2) {
    char currentSymbol = 'X';
    string currentPlayer = player1;

    while (true) {
        drawBoard();
        cout << "Current Turn: " << currentPlayer << " (" << currentSymbol << ")\n";

        int row, col;
        cout << "Enter Row (1-3): ";
        cin >> row;
        cout << "Enter Column (1-3): ";
        cin >> col;

        if (cin.fail() || row < 1 || row > 3 || col < 1 || col > 3) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            cout << "Invalid input! Try again.\n";
            pause();
            continue;
        }

        if (board[row - 1][col - 1] != ' ') {
            cout << "That spot is already taken! Choose another.\n";
            pause();
            continue;
        }

        board[row - 1][col - 1] = currentSymbol;

        if (checkWin(currentSymbol)) {
            drawBoard();
            cout << "Congratulations " << currentPlayer << "! You win!\n";
            break;
        }

        if (checkDraw()) {
            drawBoard();
            cout << "It's a draw! Both players fought well.\n";
            break;
        }

        // Switch player
        currentSymbol = (currentSymbol == 'X') ? 'O' : 'X';
        currentPlayer = (currentPlayer == player1) ? player2 : player1;
    }

    lineBreak();
    cout << "Do you want to play again? (y/n): ";
    char again;
    cin >> again;
    if (again == 'y' || again == 'Y') {
        resetBoard();
        playGame(player1, player2);
    } else {
        cout << "\nThanks for playing Tic Tac Toe!\n";
        isRunning = false;
    }
}

// --- Main Menu ---
void showMenu() {
    clearScreen();
    cout << "=================================\n";
    cout << "     WELCOME TO TIC TAC TOE 🎮   \n";
    cout << "=================================\n\n";
    cout << "1. Start New Game\n";
    cout << "2. Exit\n";
    cout << "\n> ";
}

int main() {
    string p1, p2;
    while (isRunning) {
        showMenu();
        string choice;
        cin >> choice;
        cin.ignore(); // flush newline

        if (choice == "1") {
            clearScreen();
            cout << "Enter name for Player 1 (X): ";
            getline(cin, p1);
            cout << "Enter name for Player 2 (O): ";
            getline(cin, p2);
            resetBoard();
            playGame(p1, p2);
        } else if (choice == "2") {
            cout << "\nGoodbye! See you next time 👋\n";
            break;
        } else {
            cout << "Invalid choice. Try again.\n";
            pause();
        }
    }
    return 0;
}
