#include <iostream>
#include <cstdlib>
using namespace std;

char board[3][3];
char currentPlayer = 'X';

void initializeBoard() {
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            board[i][j] = ' ';
}

void printBoard() {
    system("cls"); // Clears the screen (works on Windows)
    cout << "\n=============================\n";
    cout << "       🎮 TIC TAC TOE 🎮\n";
    cout << "=============================\n\n";
    cout << "     0   1   2\n";
    for (int i = 0; i < 3; i++) {
        cout << "   ";
        for (int j = 0; j < 3; j++) {
            cout << " " << board[i][j] << " ";
            if (j < 2) cout << "|";
        }
        cout << "\n";
        if (i < 2) cout << "   ---+---+---\n";
    }
    cout << "\n";
}

bool checkWin() {
    for (int i = 0; i < 3; i++) {
        if ((board[i][0] == currentPlayer &&
             board[i][1] == currentPlayer &&
             board[i][2] == currentPlayer) ||
            (board[0][i] == currentPlayer &&
             board[1][i] == currentPlayer &&
             board[2][i] == currentPlayer))
            return true;
    }

    if ((board[0][0] == currentPlayer &&
         board[1][1] == currentPlayer &&
         board[2][2] == currentPlayer) ||
        (board[0][2] == currentPlayer &&
         board[1][1] == currentPlayer &&
         board[2][0] == currentPlayer))
        return true;

    return false;
}

bool isBoardFull() {
    for (int i = 0; i < 3; i++)
        for (int j = 0; j < 3; j++)
            if (board[i][j] == ' ')
                return false;
    return true;
}

void switchPlayer() {
    currentPlayer = (currentPlayer == 'X') ? 'O' : 'X';
}

int main() {
    int row, col;
    initializeBoard();

    cout << "✨ Welcome to the Ultimate Tic Tac Toe Battle! ✨\n";
    cout << "Player X vs Player O — let the best strategist win!\n";
    cout << "Press Enter to begin...";
    cin.ignore();

    while (true) {
        printBoard();
        cout << "👉 Player " << currentPlayer << ", it’s your turn!\n";
        cout << "Enter row and column (0–2): ";
        cin >> row >> col;

        if (cin.fail() || row < 0 || row > 2 || col < 0 || col > 2) {
            cin.clear();
            cin.ignore(1000, '\n');
            cout << "🚫 Invalid input! Enter numbers between 0–2.\n";
            system("pause");
            continue;
        }

        if (board[row][col] != ' ') {
            cout << "❌ That spot is already taken. Try again!\n";
            system("pause");
            continue;
        }

        board[row][col] = currentPlayer;

        if (checkWin()) {
            printBoard();
            cout << "🎉 Player " << currentPlayer << " conquers the board! 🏆\n";
            break;
        }

        if (isBoardFull()) {
            printBoard();
            cout << "🤝 It’s a draw! A battle well fought.\n";
            break;
        }

        switchPlayer();
    }

    cout << "\nThanks for playing! 💫\n";
    return 0;
}
