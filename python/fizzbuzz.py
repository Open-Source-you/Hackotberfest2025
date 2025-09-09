def fizzbuzz(n):
  for num in range(1, n+1):
    if num % 15 == 0:
        print("FizzBuzz")
    elif num % 3 == 0:
        print("Fizz")
    elif num % 5 == 0:
        print("Buzz")
    else:
        print(num)

n = int(input("Enter a number: "))
fizzbuzz(n)