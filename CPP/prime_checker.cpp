#include <iostream>

bool isPrime(int n) {
    if (n <= 1) {
        return false;
    }
    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) {
            return false;
        }
    }
    return true;
}

int main() {
    int num;
    std::cout << "Enter a positive integer: ";
    std::cin >> num;

    if (isPrime(num)) {
        std::cout << num << " is a prime number." << std::endl;
    }
    else {
        std::cout << num << " is not a prime number." << std::endl;
    }

    return 0;
}