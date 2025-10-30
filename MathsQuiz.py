import random


def main():
    level = get_level()                  # get difficulty from user
    correct = generate_integer(level)    # run quiz and store returned score
    print(f"Score: {correct}")           # display score


def get_level():
    while True:
        try:
            level = int(input("Level: "))
            if level in {1, 2, 3}:
                return level   # exit loop and return valid level
        except ValueError:
            pass   # if user didn’t enter a number, loop again


def generate_integer(level):
    correct = 0

    # Set range based on level (minimal change)
    if level == 1:
        low, high = 0, 9
    elif level == 2:
        low, high = 10, 99
    else:
        low, high = 100, 999

    for _ in range(10):
        num1 = random.randint(low, high)
        num2 = random.randint(low, high)
        incorrect = 0

        while True:
            try:
                eq = f"{num1} + {num2} = "
                calc = int(input(eq))

                if calc != (num1 + num2):
                    print("EEE")
                    incorrect += 1
                    if incorrect == 3:   # after 3 tries, show answer
                        print(f"{num1} + {num2} = {num1 + num2}")
                        break
                    continue
                else:
                    correct += 1
                    break

            except ValueError:
                print("EEE")
                incorrect += 1
                if incorrect == 3:
                    print(f"{num1} + {num2} = {num1 + num2}")
                    break

    return correct


if __name__ == "__main__":
    main()
