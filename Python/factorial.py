# Problem Statement: Factorial of a Number

## Description
Write a Python program to calculate the factorial of a non-negative integer. The factorial of a non-negative integer `n`, denoted by `n!`, is the product of all positive integers less than or equal to `n`. The factorial of 0 is 1.

## Examples
- `factorial(0)` should return `1`
- `factorial(1)` should return `1`
- `factorial(5)` should return `120` (since 5 * 4 * 3 * 2 * 1 = 120)

## Input
A single non-negative integer `n`.

## Output
The factorial of `n`.

## Constraints
- `n` will be a non-negative integer.

## Time and Space Complexity
- **Time Complexity**: O(n) - The function performs `n` multiplications in the iterative approach.
- **Space Complexity**: O(1) - The function uses a constant amount of extra space.

```python
def factorial(n):
    """
    Calculates the factorial of a non-negative integer.

    Args:
        n (int): The non-negative integer.

    Returns:
        int: The factorial of n.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    elif n == 0:
        return 1
    else:
        result = 1
        for i in range(1, n + 1):
            result *= i
        return result

# Example Usage:
if __name__ == "__main__":
    num = 5
    print(f"The factorial of {num} is: {factorial(num)}") # Expected: 120

    num = 0
    print(f"The factorial of {num} is: {factorial(num)}") # Expected: 1

    num = 7
    print(f"The factorial of {num} is: {factorial(num)}") # Expected: 5040
```