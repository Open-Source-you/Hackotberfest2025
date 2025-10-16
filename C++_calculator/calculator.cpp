#include <iostream>
#include <iomanip>  // for std::setprecision
#include <limits>   // for input validation

using namespace std;

int main() {
    char operation;
    double num1, num2;
    char choice;

    cout << "=========================================\n";
    cout << "        🧮 Simple Calculator App          \n";
    cout << "=========================================\n";

    do {
        cout << "\nChoose an operation (+, -, *, /): ";
        cin >> operation;

        // Input two numbers
        cout << "Enter first number: ";
        cin >> num1;

        cout << "Enter second number: ";
        cin >> num2;

        cout << fixed << setprecision(2);  // Show results with 2 decimal places

        switch (operation) {
            case '+':
                cout << "\n✅ Sum: " << num1 + num2 << endl;
                break;
            case '-':
                cout << "\n✅ Difference: " << num1 - num2 << endl;
                break;
            case '*':
                cout << "\n✅ Product: " << num1 * num2 << endl;
                break;
            case '/':
                if (num2 == 0)
                    cout << "\n⚠️ Error: Division by zero is not allowed!" << endl;
                else
                    cout << "\n✅ Quotient: " << num1 / num2 << endl;
                break;
            default:
                cout << "\n❌ Invalid operation! Please use +, -, *, or /." << endl;
                break;
        }

        cout << "\nWould you like to perform another calculation? (y/n): ";
        cin >> choice;

        // Clear input buffer if invalid input
        if (cin.fail()) {
            cin.clear();
            cin.ignore(numeric_limits<streamsize>::max(), '\n');
            choice = 'n';
        }

    } while (choice == 'y' || choice == 'Y');

    cout << "\n=========================================\n";
    cout << "    👋 Thank you for using the calculator! \n";
    cout << "=========================================\n";

    return 0;
}
