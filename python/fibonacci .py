def fibonacci(n):
    fib_sequence = [0, 1]
    
    for i in range(2, n):
        next_value = fib_sequence[-1] + fib_sequence[-2]
        fib_sequence.append(next_value)
    
    return fib_sequence[:n]  

n = int(input("Enter the number of Fibonacci numbers to generate: "))

fib_numbers = fibonacci(n)
print(fib_numbers)
