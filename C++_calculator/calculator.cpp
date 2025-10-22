```cpp
#include <iostream>
#include <string>

using namespace std;

int main() {
  char operation;
  float num1, num2;

  cout << "Enter an operation (+, -, /, *): ";
  cin >> operation;

  cout << "Enter two numbers: ";
  cin >> num1 >> num2:num

  switch (operation) {
    case '+':
      cout << "Sum: " << num1 + num2 << endl;
      break;
    case '-':
      cout << "Difference: " << num1 - num2 << endl;
      break;
    case '*':
      cout << "Product: " << num1 * num2 << endl;
      break;
    case '/':
      cout << "Quotient: " << num1 / num2 << endl;
      break;
    default:
      cout << "Invalid operation" << endl;
      break;
  }

  return 0;
}
```
