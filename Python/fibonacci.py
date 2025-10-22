# Problem Statement: Fibonacci Sequence

## Description
Write a Python program to generate the Fibonacci sequence up to a specified number of terms `n`. The Fibonacci sequence is a series of numbers where each number is the sum of the two preceding ones, usually starting with 0 and 1.

## Examples
- `fibonacci(0)` should return `[]`
- `fibonacci(1)` should return `[0]`
- `fibonacci(5)` should return `[0, 1, 1, 2, 3]`
- `fibonacci(10)` should return `[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]`

## Input
A single non-negative integer `n` representing the number of terms to generate.

## Output
A list of integers representing the Fibonacci sequence up to `n` terms.

## Constraints
- `n` will be a non-negative integer.

## Time and Space Complexity
- **Time Complexity**: O(n) - The function generates `n` terms, performing a constant number of operations for each term.
- **Space Complexity**: O(n) - The function stores `n` terms in a list.

```python
def fibonacci(n):
    """
    Generates the Fibonacci sequence up to n terms.

    Args:
        n (int): The number of terms to generate.

    Returns:
        list: A list of integers representing the Fibonacci sequence.
    """
    if n <= 0:
        return []
    elif n == 1:
        return [0]
    else:
        sequence = [0, 1]
        while len(sequence) < n:
            next_num = sequence[-1] + sequence[-2]
            sequence.append(next_num)
        return sequence

# Example Usage:
if __name__ == "__main__":
    num_terms = 5
    print(f"Fibonacci sequence up to {num_terms} terms: {fibonacci(num_terms)}") # Expected: [0, 1, 1, 2, 3]

    num_terms = 0
    print(f"Fibonacci sequence up to {num_terms} terms: {fibonacci(num_terms)}") # Expected: []

    num_terms = 10
    print(f"Fibonacci sequence up to {num_terms} terms: {fibonacci(num_terms)}") # Expected: [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```