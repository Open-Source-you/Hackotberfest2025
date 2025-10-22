# Find Fibonacci Series in Python Using While Loop
# we are taking a number from user as input

# entered value will be converted to int from string
n = int(input("Number of Fibonacci Series to be Printed: "))

# print initial 2 number to start fibonacci series
a, b = 0, 1
print(a, b, end=" ")

i = 0
while i < n - 2:
    c = a + b
    # add the last two numbers and print
    print(c, end=" ")
    a = b
    b = c
    i = i + 1
