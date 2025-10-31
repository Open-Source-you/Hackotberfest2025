#include <iostream>
#include <stdexcept>
using namespace std;

// One-word logic summary: Encapsulation
class Calculator {
public:
    double add(double a, double b) { return a + b; }           // Addition
    double subtract(double a, double b) { return a - b; }      // Subtraction
    double multiply(double a, double b) { return a * b; }      // Multiplication
    double divide(double a, double b) {                        // Division with zero check
        if (b == 0) throw runtime_error("Division by zero");
        return a / b;
    }
};

int main() {
    Calculator calc;           // Object creation
    double num1, num2, result; // Input and result variables
    char op, choice;           // Operator and loop control

    cout << "=== SmartCalcCPP ===" << endl;

    do {
        // INPUT BLOCK
        cout << "\nEnter first number: ";
        cin >> num1;
        cout << "Enter operator (+ - * /): ";
        cin >> op;
        cout << "Enter second number: ";
        cin >> num2;

        // OPERATION BLOCK
        try {
            switch (op) {
                case '+': result = calc.add(num1, num2); break;       // ADD
                case '-': result = calc.subtract(num1, num2); break;  // SUBTRACT
                case '*': result = calc.multiply(num1, num2); break;  // MULTIPLY
                case '/': result = calc.divide(num1, num2); break;    // DIVIDE
                default: throw invalid_argument("Invalid operator");
            }
            cout << "Result: " << result << endl;
        } catch (exception& e) {
            cout << "Error: " << e.what() << endl;
        }

        // LOOP CONTROL
        cout << "\nDo another calculation? (y/n): ";
        cin >> choice;
    } while (choice == 'y' || choice == 'Y');

    cout << "\nThank you for using SmartCalcCPP!" << endl;
    return 0;
}
